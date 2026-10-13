"""Seed script for Esports Hub Firestore collections.

Initializes sample players, extended match history, and historical tournament performance.
"""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-a1e17004d2d8"

SEED_PLAYERS = [
    {
        "player_id": "dynamitexx",
        "ign": "DynamiteXX",
        "real_name": "Deepak Sharma",
        "role": "Assaulter / IGL",
        "matches_played": 28,
        "total_kills": 94,
        "total_damage": 17450,
        "avg_survival_mins": 25.1,
        "mvp_count": 9,
        "kd_ratio": 3.36,
        "headshot_percentage": 24.8,
        "status": "Active Roster",
        "recent_form": "Excellent (MVP in 3 of last 5 matches)",
    },
    {
        "player_id": "royal_charan",
        "ign": "ROYAL Charan",
        "real_name": "Charan Kumar",
        "role": "Support / Medic",
        "matches_played": 28,
        "total_kills": 44,
        "total_damage": 14220,
        "avg_survival_mins": 23.4,
        "mvp_count": 4,
        "kd_ratio": 1.57,
        "headshot_percentage": 18.2,
        "status": "Active Roster",
        "recent_form": "Consistent support, high revive count (42 total revives)",
    },
    {
        "player_id": "kiranplays",
        "ign": "kiranplays",
        "real_name": "Kiran Patel",
        "role": "Flanker",
        "matches_played": 25,
        "total_kills": 59,
        "total_damage": 13350,
        "avg_survival_mins": 21.8,
        "mvp_count": 3,
        "kd_ratio": 2.36,
        "headshot_percentage": 29.5,
        "status": "Active Roster",
        "recent_form": "Aggressive entries, top fragging on Miramar",
    },
    {
        "player_id": "chin222222",
        "ign": "ChiN222222",
        "real_name": "Chirag Nair",
        "role": "Sniper",
        "matches_played": 28,
        "total_kills": 72,
        "total_damage": 16180,
        "avg_survival_mins": 27.0,
        "mvp_count": 6,
        "kd_ratio": 2.57,
        "headshot_percentage": 38.4,
        "status": "Active Roster",
        "recent_form": "Long range specialist, highest average survival time",
    },
    {
        "player_id": "shadowvortex",
        "ign": "ShadowVortex",
        "real_name": "Vikram Sen",
        "role": "Substitute / Assaulter",
        "matches_played": 8,
        "total_kills": 16,
        "total_damage": 3850,
        "avg_survival_mins": 19.5,
        "mvp_count": 1,
        "kd_ratio": 2.00,
        "headshot_percentage": 21.0,
        "status": "Reserve / Bench",
        "recent_form": "Scored 5 kills in Miramar sub appearance",
    },
]

SEED_MATCHES = [
    {
        "match_id": "bms-match-01",
        "tournament_name": "Battlegrounds Masters Series 2026",
        "stage": "Grand Finals - Day 1",
        "match_number": 1,
        "map": "Erangel",
        "team_rank": 2,
        "total_teams": 26,
        "total_team_kills": 10,
        "team_points": 22,
        "players": [
            {"ign": "DynamiteXX", "kills": 4, "damage": 875, "survived_mins": 26.9, "revives": 2, "rating": 92.8, "is_mvp": True},
            {"ign": "ROYAL Charan", "kills": 2, "damage": 842, "survived_mins": 23.7, "revives": 1, "rating": 84.5, "is_mvp": False},
            {"ign": "kiranplays", "kills": 1, "damage": 489, "survived_mins": 23.9, "revives": 2, "rating": 75.2, "is_mvp": False},
            {"ign": "ChiN222222", "kills": 3, "damage": 318, "survived_mins": 31.1, "revives": 2, "rating": 81.2, "is_mvp": False},
        ],
        "notes": "Solid #2 placement in Erangel, good rotation into Pochinki hills.",
    },
    {
        "match_id": "bms-match-02",
        "tournament_name": "Battlegrounds Masters Series 2026",
        "stage": "Grand Finals - Day 1",
        "match_number": 2,
        "map": "Miramar",
        "team_rank": 1,
        "total_teams": 26,
        "total_team_kills": 14,
        "team_points": 29,
        "players": [
            {"ign": "DynamiteXX", "kills": 5, "damage": 980, "survived_mins": 32.4, "revives": 1, "rating": 96.4, "is_mvp": True},
            {"ign": "ChiN222222", "kills": 5, "damage": 1020, "survived_mins": 32.4, "revives": 0, "rating": 95.1, "is_mvp": False},
            {"ign": "kiranplays", "kills": 3, "damage": 610, "survived_mins": 28.1, "revives": 1, "rating": 82.0, "is_mvp": False},
            {"ign": "ROYAL Charan", "kills": 1, "damage": 430, "survived_mins": 32.4, "revives": 3, "rating": 83.5, "is_mvp": False},
        ],
        "notes": "Winner Winner Chicken Dinner! High ground control near Pecado.",
    },
    {
        "match_id": "bms-match-03",
        "tournament_name": "Battlegrounds Masters Series 2026",
        "stage": "Grand Finals - Day 1",
        "match_number": 3,
        "map": "Sanhok",
        "team_rank": 5,
        "total_teams": 26,
        "total_team_kills": 7,
        "team_points": 13,
        "players": [
            {"ign": "kiranplays", "kills": 4, "damage": 720, "survived_mins": 19.8, "revives": 1, "rating": 89.2, "is_mvp": True},
            {"ign": "DynamiteXX", "kills": 2, "damage": 450, "survived_mins": 18.2, "revives": 1, "rating": 78.0, "is_mvp": False},
            {"ign": "ChiN222222", "kills": 1, "damage": 290, "survived_mins": 19.8, "revives": 0, "rating": 71.5, "is_mvp": False},
            {"ign": "ROYAL Charan", "kills": 0, "damage": 310, "survived_mins": 16.4, "revives": 2, "rating": 68.0, "is_mvp": False},
        ],
        "notes": "Close combat skirmish in Bootcamp, caught in crossfire zone 4.",
    },
    {
        "match_id": "bms-match-04",
        "tournament_name": "Battlegrounds Masters Series 2026",
        "stage": "Grand Finals - Day 2",
        "match_number": 4,
        "map": "Erangel",
        "team_rank": 1,
        "total_teams": 26,
        "total_team_kills": 12,
        "team_points": 27,
        "players": [
            {"ign": "ChiN222222", "kills": 6, "damage": 1150, "survived_mins": 31.8, "revives": 1, "rating": 98.0, "is_mvp": True},
            {"ign": "DynamiteXX", "kills": 3, "damage": 710, "survived_mins": 31.8, "revives": 1, "rating": 88.5, "is_mvp": False},
            {"ign": "ROYAL Charan", "kills": 2, "damage": 590, "survived_mins": 31.8, "revives": 2, "rating": 85.0, "is_mvp": False},
            {"ign": "kiranplays", "kills": 1, "damage": 380, "survived_mins": 25.0, "revives": 0, "rating": 72.4, "is_mvp": False},
        ],
        "notes": "Chicken Dinner! ChiN222222 had an insane AWM performance on Military Base bridge.",
    },
    {
        "match_id": "bms-match-05",
        "tournament_name": "Battlegrounds Masters Series 2026",
        "stage": "Grand Finals - Day 2",
        "match_number": 5,
        "map": "Miramar",
        "team_rank": 3,
        "total_teams": 26,
        "total_team_kills": 9,
        "team_points": 18,
        "players": [
            {"ign": "DynamiteXX", "kills": 4, "damage": 820, "survived_mins": 27.5, "revives": 2, "rating": 91.0, "is_mvp": True},
            {"ign": "kiranplays", "kills": 3, "damage": 640, "survived_mins": 27.5, "revives": 1, "rating": 86.4, "is_mvp": False},
            {"ign": "ROYAL Charan", "kills": 1, "damage": 410, "survived_mins": 25.2, "revives": 3, "rating": 80.5, "is_mvp": False},
            {"ign": "ChiN222222", "kills": 1, "damage": 330, "survived_mins": 27.5, "revives": 0, "rating": 76.0, "is_mvp": False},
        ],
        "notes": "Top 3 finish with strong defensive play around Hacienda.",
    },
    {
        "match_id": "bms-match-06",
        "tournament_name": "Battlegrounds Masters Series 2026",
        "stage": "Grand Finals - Day 2",
        "match_number": 6,
        "map": "Erangel",
        "team_rank": 4,
        "total_teams": 26,
        "total_team_kills": 8,
        "team_points": 15,
        "players": [
            {"ign": "DynamiteXX", "kills": 3, "damage": 690, "survived_mins": 24.1, "revives": 1, "rating": 85.0, "is_mvp": False},
            {"ign": "ChiN222222", "kills": 3, "damage": 650, "survived_mins": 24.1, "revives": 0, "rating": 84.2, "is_mvp": False},
            {"ign": "ROYAL Charan", "kills": 1, "damage": 480, "survived_mins": 24.1, "revives": 2, "rating": 79.5, "is_mvp": False},
            {"ign": "kiranplays", "kills": 1, "damage": 310, "survived_mins": 20.3, "revives": 1, "rating": 72.0, "is_mvp": False},
        ],
        "notes": "Finished 4th in final game, secured 2nd place overall on tournament podium.",
    },
]


def seed_database():
    print(f"Connecting to Firestore with project ID: {PROJECT_ID}")
    db = firestore.Client(project=PROJECT_ID)

    # Seed Players
    players_col = db.collection("players")
    for player in SEED_PLAYERS:
        doc_ref = players_col.document(player["player_id"])
        doc_ref.set(player)
        print(f"Seeded player: {player['ign']} ({player['player_id']}) - {player['matches_played']} matches")

    # Seed Matches
    matches_col = db.collection("matches")
    for match in SEED_MATCHES:
        doc_ref = matches_col.document(match["match_id"])
        doc_ref.set(match)
        print(f"Seeded match: {match['match_id']} | {match['map']} | Rank #{match['team_rank']} ({match['total_team_kills']} kills)")

    print("Firestore extended history seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
