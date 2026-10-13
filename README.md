# BGMI Esports Roster & Match Intelligence Hub

An autonomous agentic intelligence system built with the Google Agent Development Kit (ADK) and Gemini, designed for competitive BGMI / Battlegrounds esports organizations, analysts, and coaches.

![Esports Hub Demo](assets/demo.gif)

---

## What It Actually Does

The Esports Hub agent manages competitive player rosters, computes head-to-head performance comparisons, tracks tournament match records, retrieves live gaming industry intelligence, and generates cinematic video highlights using Google's multimodal models.

### Implemented Capabilities & Tools

1. **Roster Profiles & Performance Metrics (`Firestore`)**
   - **`list_roster_players`**: Queries the Firestore `players` collection for active roster members, roles, total kills, damage, and matches played.
   - **`get_player_details`**: Retrieves comprehensive statistics for an in-game name (IGN), including K/D ratio, headshot percentage, average survival time, and recent tournament form.
   - **`record_player`**: Adds or updates player profiles directly in Firestore.

2. **Head-to-Head Player Analytics**
   - **`compare_roster_players`**: Fetches two player profiles from Firestore and performs automated comparative calculations across K/D ratio, survival minutes, total damage, and tournament MVPs.

3. **Tournament Match Tracking (`Firestore`)**
   - **`record_match_stats`**: Stores tournament match records (tournament name, map, team placement, total team kills, strategic notes).
   - **`list_matches`**: Queries historical recorded matches and placements.

4. **Gaming Industry Intelligence (`Public API`)**
   - **`get_gaming_industry_intel`**: Queries the live FreeToGame ecosystem database via HTTPS to retrieve current battle royale, shooter, and competitive game metadata, publishers, and platforms.

5. **Cinematic Highlight Video Generation (`Gemini Omni` + `Cloud Storage`)**
   - **`generate_esports_highlight_video`**: Calls Google's Omni model (`gemini-omni-flash-preview`) in Vertex AI (`location="global"`) using the Interactions API. Saves the video bytes to the session artifact store via `tool_context.save_artifact` (visible in the ADK Playground) and uploads the MP4 directly to a public Google Cloud Storage bucket (`esports-hub-media-*`), returning a public HTTPS URL.

6. **Agent-to-UI Rendering (`A2UI v0.8`)**
   - Uses `A2uiSchemaManager` with the Basic Catalog and an `after_model_callback` (`a2ui_callback`) to emit native A2UI surface components (`Card`, `Column`, `Row`, `Text`, `Image`).
   - The frontend renders these cards directly in the browser chat bubble without heavy UI frameworks.

### Cloud Architecture & Services Wired

| Service | Role in Project | Implementation Detail |
| :--- | :--- | :--- |
| **Google Cloud Firestore** | NoSQL database | Stores player profiles (`players`) and match results (`matches`). Configured with explicit project ID string. |
| **Google Cloud Storage** | Media asset storage | Public bucket hosting generated video highlights and media artifacts. |
| **Vertex AI Interactions API** | Multimodal video generation | Runs `gemini-omni-flash-preview` in the `global` region for video rendering. |
| **Vertex AI Agent Engine** | Agent runtime | Deployed ADK agent serving over the A2A protocol. |
| **Google Cloud Run** | Frontend proxy hosting | Runs the FastAPI proxy and vanilla HTML/JS chat interface. |

> **Planned, Not Yet Implemented:** Multimodal scoreboard image OCR parsing (extracting player kills and damage from uploaded match screenshots) and Vertex AI Memory Bank integration.

---

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── agent.py          # Root ADK agent, tools, Firestore queries, Omni video tool, A2UI setup
│   └── a2ui_utils.py     # A2UI after_model_callback parser
├── frontend/
│   ├── main.py           # FastAPI proxy forwarding client chat requests to the agent via A2A
│   ├── static/
│   │   └── index.html    # Rebranded tactical dark-mode chat UI with native A2UI card renderer
│   ├── Dockerfile        # Container definition for Cloud Run
│   └── requirements.txt
├── assets/
│   └── demo.gif          # Looping demo recording of live agent interactions
├── seed_firestore.py     # Script to populate initial BGMI player roster and match history
├── pyproject.toml        # Dependencies and project definition
└── agents-cli-manifest.yaml
```

---

## Local Setup & Run Instructions

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Cloud CLI (`gcloud`) authenticated with access to Firestore, Cloud Storage, and Vertex AI

### 1. Install Dependencies
```bash
# In the project root
uv sync
```

### 2. Seed Initial Firestore Data
```bash
uv run python seed_firestore.py
```

### 3. Run Agent in Development Mode
You can test the agent directly in your terminal using the ADK CLI:
```bash
agents-cli run "Show me the profile card for DynamiteXX"
```

Or run the interactive ADK Web playground:
```bash
agents-cli web
```

### 4. Run the Chat Frontend Locally
The frontend includes a lightweight FastAPI proxy that communicates with your agent via A2A:

```bash
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the local server (listens on port 8080)
python main.py
```
Open a browser and navigate to the local server port to interact with the UI and prompt chips.
