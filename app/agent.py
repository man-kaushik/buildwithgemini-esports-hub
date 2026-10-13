# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import datetime
import json
from typing import Any, Dict, List, Optional
import urllib.request
import uuid
from zoneinfo import ZoneInfo

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google import genai
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.cloud import firestore, storage
from google.genai import types

from .a2ui_utils import a2ui_callback

MODEL = "gemini-3.6-flash"

# Hardcoded project ID as string — avoids Agent Platform project number issue
FIRESTORE_PROJECT = "qwiklabs-gcp-04-a1e17004d2d8"
GCS_BUCKET_NAME = "esports-hub-media-qwiklabs-gcp-04-a1e17004d2d8"

_db: Optional[firestore.Client] = None
_storage_client: Optional[storage.Client] = None


def get_firestore_client() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client(project=FIRESTORE_PROJECT)
    return _db


def list_roster_players() -> List[Dict[str, Any]]:
    """List all registered esports players in the organization roster with summary stats.

    Returns:
        A list of player dictionaries containing IGN, role, matches, kills, damage, and status.
    """
    db = get_firestore_client()
    docs = db.collection("players").stream()
    players = []
    for doc in docs:
        data = doc.to_dict()
        players.append(data)
    return players


def get_player_details(ign_or_id: str) -> Dict[str, Any]:
    """Retrieve detailed stats for a specific player by in-game name (IGN) or player ID.

    Args:
        ign_or_id: The player's IGN (e.g. 'DynamiteXX') or player_id (e.g. 'dynamitexx').

    Returns:
        A dictionary with the player's full profile and stats, or an error message.
    """
    db = get_firestore_client()
    needle = ign_or_id.strip().lower()

    # Try direct ID lookup first
    doc = db.collection("players").document(needle).get()
    if doc.exists:
        return doc.to_dict()

    # Query by IGN
    docs = db.collection("players").stream()
    for d in docs:
        val = d.to_dict()
        if val.get("ign", "").lower() == needle:
            return val

    return {"error": f"Player '{ign_or_id}' not found in the roster."}


def record_player(
    ign: str,
    role: str,
    real_name: str = "",
    matches_played: int = 0,
    total_kills: int = 0,
    total_damage: int = 0,
    status: str = "Active Roster",
) -> Dict[str, Any]:
    """Add or update an esports player in the roster.

    Args:
        ign: In-game name of the player (e.g., 'DynamiteXX').
        role: Primary role (e.g., 'Assaulter / IGL', 'Support', 'Sniper').
        real_name: Optional real name of the player.
        matches_played: Total matches played.
        total_kills: Total tournament kills.
        total_damage: Total damage dealt.
        status: Player status (e.g. 'Active Roster', 'Bench').

    Returns:
        Confirmation dictionary with the saved player profile.
    """
    db = get_firestore_client()
    player_id = ign.strip().lower().replace(" ", "_")
    player_data = {
        "player_id": player_id,
        "ign": ign,
        "real_name": real_name,
        "role": role,
        "matches_played": matches_played,
        "total_kills": total_kills,
        "total_damage": total_damage,
        "status": status,
        "updated_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat(),
    }
    db.collection("players").document(player_id).set(player_data, merge=True)
    return {"message": f"Player '{ign}' saved successfully.", "player": player_data}


def record_match_stats(
    tournament_name: str,
    map_name: str,
    team_rank: int,
    total_team_kills: int,
    notes: str = "",
) -> Dict[str, Any]:
    """Record summary match results for the esports team in a tournament.

    Args:
        tournament_name: Name of the tournament (e.g., 'Battlegrounds Masters Series 2026').
        map_name: Map played (e.g., 'Erangel', 'Miramar').
        team_rank: Overall team placement in the match (e.g., 1, 2).
        total_team_kills: Total kills achieved by the team.
        notes: Strategic notes or match observations.

    Returns:
        Confirmation dictionary with the saved match details.
    """
    db = get_firestore_client()
    match_id = f"match-{datetime.datetime.now(ZoneInfo('UTC')).strftime('%Y%m%d%H%M%S')}"
    match_data = {
        "match_id": match_id,
        "tournament_name": tournament_name,
        "map": map_name,
        "team_rank": team_rank,
        "total_team_kills": total_team_kills,
        "notes": notes,
        "created_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat(),
    }
    db.collection("matches").document(match_id).set(match_data)
    return {"message": f"Match recorded successfully with ID: {match_id}", "match": match_data}


def list_matches() -> List[Dict[str, Any]]:
    """List recent recorded tournament matches and placements.

    Returns:
        A list of recorded match summaries.
    """
    db = get_firestore_client()
    docs = db.collection("matches").stream()
    return [doc.to_dict() for doc in docs]


def compare_roster_players(player_a_ign: str, player_b_ign: str) -> Dict[str, Any]:
    """Compare two esports roster players head-to-head on key metrics (K/D, damage, survival, MVPs).

    Args:
        player_a_ign: First player's IGN or ID (e.g. 'DynamiteXX').
        player_b_ign: Second player's IGN or ID (e.g. 'ChiN222222').

    Returns:
        A comparison dictionary containing player profiles, key metrics comparison, and highlights.
    """
    p1 = get_player_details(player_a_ign)
    p2 = get_player_details(player_b_ign)

    if "error" in p1:
        return {"error": p1["error"]}
    if "error" in p2:
        return {"error": p2["error"]}

    p1_matches = max(p1.get("matches_played", 1), 1)
    p2_matches = max(p2.get("matches_played", 1), 1)

    p1_avg_dmg = round(p1.get("total_damage", 0) / p1_matches, 1)
    p2_avg_dmg = round(p2.get("total_damage", 0) / p2_matches, 1)

    return {
        "player_a": {
            "ign": p1.get("ign"),
            "role": p1.get("role"),
            "matches": p1_matches,
            "kd_ratio": p1.get("kd_ratio", round(p1.get("total_kills", 0) / p1_matches, 2)),
            "avg_damage": p1_avg_dmg,
            "avg_survival_mins": p1.get("avg_survival_mins", 0),
            "headshot_pct": p1.get("headshot_percentage", 0),
            "mvp_count": p1.get("mvp_count", 0),
        },
        "player_b": {
            "ign": p2.get("ign"),
            "role": p2.get("role"),
            "matches": p2_matches,
            "kd_ratio": p2.get("kd_ratio", round(p2.get("total_kills", 0) / p2_matches, 2)),
            "avg_damage": p2_avg_dmg,
            "avg_survival_mins": p2.get("avg_survival_mins", 0),
            "headshot_pct": p2.get("headshot_percentage", 0),
            "mvp_count": p2.get("mvp_count", 0),
        },
        "highlights": {
            "higher_kd": p1.get("ign") if p1.get("kd_ratio", 0) >= p2.get("kd_ratio", 0) else p2.get("ign"),
            "higher_avg_damage": p1.get("ign") if p1_avg_dmg >= p2_avg_dmg else p2.get("ign"),
            "longer_survival": p1.get("ign") if p1.get("avg_survival_mins", 0) >= p2.get("avg_survival_mins", 0) else p2.get("ign"),
            "more_mvps": p1.get("ign") if p1.get("mvp_count", 0) >= p2.get("mvp_count", 0) else p2.get("ign"),
        },
    }


def get_gaming_industry_intel(category_or_tag: str = "battle-royale") -> List[Dict[str, Any]]:
    """Fetch live public title data and ecosystem metadata from the public FreeToGame API.

    Args:
        category_or_tag: Gaming category or genre to inspect (e.g., 'battle-royale', 'shooter', 'pvp').

    Returns:
        A list of matching game titles with publisher, developer, platform, and game details.
    """
    clean_cat = category_or_tag.strip().lower().replace(" ", "-")
    url = f"https://www.freetogame.com/api/games?category={clean_cat}"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "EsportsHubAgent/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                results = []
                for item in data[:6]:  # Return top 6 relevant titles
                    results.append({
                        "title": item.get("title"),
                        "genre": item.get("genre"),
                        "platform": item.get("platform"),
                        "publisher": item.get("publisher"),
                        "developer": item.get("developer"),
                        "short_description": item.get("short_description"),
                        "game_url": item.get("game_url"),
                    })
                return results
    except Exception as e:
        return [{"error": f"Failed to query gaming database: {str(e)}"}]
    return []


def generate_esports_highlight_video(
    prompt: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """Generate a short cinematic esports highlight or victory ceremony teaser video.

    Generates the video with Google's Omni model (gemini-omni-flash-preview) in the global region,
    persists it to the session artifacts, uploads it to the public Cloud Storage bucket,
    and returns its public https URL.

    Args:
        prompt: Description of the esports highlight, trophy celebration, or cinematic play.
        tool_context: ToolContext used to save the video as an artifact for the Playground.

    Returns:
        A dictionary with the public video URL, artifact status, and confirmation.
    """
    global _storage_client
    try:
        genai_client = genai.Client(
            vertexai=True,
            project=FIRESTORE_PROJECT,
            location="global",
        )

        interaction = genai_client.interactions.create(
            model="gemini-omni-flash-preview",
            input=prompt,
        )

        if not hasattr(interaction, "output_video") or not interaction.output_video:
            return {"error": "The Omni model did not return video output."}

        raw_data = getattr(interaction.output_video, "data", None)
        if not raw_data:
            return {"error": "No video data received in model response."}

        if isinstance(raw_data, str):
            video_bytes = base64.b64decode(raw_data)
        elif isinstance(raw_data, (bytes, bytearray)):
            video_bytes = bytes(raw_data)
        else:
            return {"error": f"Unexpected video data format: {type(raw_data)}"}

        video_filename = f"esports_highlight_{uuid.uuid4().hex[:8]}.mp4"

        # 1. Save with tool_context.save_artifact so it appears in Playground's Artifacts panel
        tool_context.save_artifact(
            filename=video_filename,
            artifact=video_bytes,
            mime_type="video/mp4",
        )

        # 2. Upload video bytes to public Cloud Storage bucket
        if _storage_client is None:
            _storage_client = storage.Client(project=FIRESTORE_PROJECT)

        bucket = _storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(video_filename)
        blob.upload_from_string(video_bytes, content_type="video/mp4")

        public_url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{video_filename}"

        return {
            "status": "success",
            "video_url": public_url,
            "filename": video_filename,
            "message": "Esports highlight video generated and published successfully.",
        }
    except Exception as e:
        return {"error": f"Failed to generate video: {str(e)}"}


schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are the Esports Roster & Match Intelligence Hub Assistant for competitive BGMI / Battlegrounds. "
        "You help coaches, managers, and analysts query roster profiles, review match statistics, compare player metrics, "
        "generate cinematic highlight teaser videos for matches or players, "
        "and fetch gaming industry ecosystem intel using live public game data. "
        "Use your tools accurately to provide insightful answers."
    ),
    workflow_description="Analyze the user request, call necessary tools, and return structured UI when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        list_roster_players,
        get_player_details,
        compare_roster_players,
        record_player,
        record_match_stats,
        list_matches,
        get_gaming_industry_intel,
        generate_esports_highlight_video,
    ],
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
