import hashlib
import json
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker


# CONFIG
JSON_DIR = "src/database/matchesjson"
DB_PATH = "rocket_league.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
metadata = MetaData()
Session = sessionmaker(bind=engine)

# DEF TABLES
platforms = Table(
    "platforms",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, unique=True),
)

ranks = Table(
    "ranks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tier", Integer),
    Column("division", Integer),
    Column("name", String, unique=True),
)

players = Table(
    "players",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("platform_id", Integer, ForeignKey("platforms.id")),
    Column("platform_user_id", String, unique=True),
    Column("name", String),
)

matches = Table(
    "matches",
    metadata,
    Column("id", String(64), primary_key=True),
    Column("playlist_id", String),
    Column("season", Integer),
    Column("duration", Integer),
    Column("overtime", Boolean),
    Column("date_upload", String),
)

match_teams = Table(
    "match_teams",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("match_id", String, ForeignKey("matches.id")),
    Column("color", String),
    Column("score", Integer),
    Column("possession_time", Float),
    Column("time_in_side", Float),
)

match_participation = Table(
    "match_participation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("match_team_id", Integer, ForeignKey("match_teams.id")),
    Column("player_id", Integer, ForeignKey("players.id")),
    Column("rank_id", Integer, ForeignKey("ranks.id")),
    Column("car_id", Integer),
    Column("car_name", String),
    Column("mvp", Boolean),
    Column("start_time", Float),
    Column("end_time", Float),
)

stats_core = Table(
    "stats_core",
    metadata,
    Column(
        "participation_id",
        Integer,
        ForeignKey("match_participation.id"),
        primary_key=True,
    ),
    Column("shots", Integer),
    Column("goals", Integer),
    Column("saves", Integer),
    Column("assists", Integer),
    Column("score", Integer),
    Column("shooting_percentage", Float),
    Column("demo_inflicted", Integer),
    Column("demo_taken", Integer),
)

stats_boost = Table(
    "stats_boost",
    metadata,
    Column(
        "participation_id",
        Integer,
        ForeignKey("match_participation.id"),
        primary_key=True,
    ),
    Column("boost_per_minute", Float),
    Column("boost_consumed_per_minute", Float),
    Column("average_amount", Float),
    Column("amount_collected", Integer),
    Column("amount_stolen", Integer),
    Column("amount_collected_big", Integer),
    Column("amount_stolen_big", Integer),
    Column("amount_collected_small", Integer),
    Column("amount_stolen_small", Integer),
    Column("count_collected_big", Integer),
    Column("count_stolen_big", Integer),
    Column("count_collected_small", Integer),
    Column("count_stolen_small", Integer),
    Column("amount_overfill", Integer),
    Column("amount_overfill_stolen", Integer),
    Column("amount_used_while_supersonic", Integer),
    Column("time_zero_boost", Float),
    Column("percent_zero_boost", Float),
    Column("time_full_boost", Float),
    Column("percent_full_boost", Float),
    Column("time_boost_0_25", Float),
    Column("time_boost_25_50", Float),
    Column("time_boost_50_75", Float),
    Column("time_boost_75_100", Float),
    Column("percent_boost_0_25", Float),
    Column("percent_boost_25_50", Float),
    Column("percent_boost_50_75", Float),
    Column("percent_boost_75_100", Float),
)

stats_movement = Table(
    "stats_movement",
    metadata,
    Column(
        "participation_id",
        Integer,
        ForeignKey("match_participation.id"),
        primary_key=True,
    ),
    Column("avg_speed", Integer),
    Column("total_distance", Integer),
    Column("time_supersonic_speed", Float),
    Column("time_boost_speed", Float),
    Column("time_slow_speed", Float),
    Column("time_ground", Float),
    Column("time_low_air", Float),
    Column("time_high_air", Float),
    Column("time_powerslide", Float),
    Column("count_powerslide", Integer),
    Column("avg_powerslide_duration", Float),
    Column("avg_speed_percentage", Float),
    Column("percent_slow_speed", Float),
    Column("percent_boost_speed", Float),
    Column("percent_supersonic_speed", Float),
    Column("percent_ground", Float),
    Column("percent_low_air", Float),
    Column("percent_high_air", Float),
)

stats_positioning = Table(
    "stats_positioning",
    metadata,
    Column(
        "participation_id",
        Integer,
        ForeignKey("match_participation.id"),
        primary_key=True,
    ),
    Column("average_distance_to_ball", Integer),
    Column("average_distance_to_mates", Integer),
    Column("time_defensive_third", Float),
    Column("time_neutral_third", Float),
    Column("time_offensive_third", Float),
    Column("time_behind_ball", Float),
    Column("time_infront_ball", Float),
    Column("time_most_back", Float),
    Column("time_most_forward", Float),
    Column("goals_against_while_last_defender", Integer),
    Column("time_closest_to_ball", Float),
    Column("time_farthest_to_ball", Float),
    Column("percent_defensive_third", Float),
    Column("percent_neutral_third", Float),
    Column("percent_offensive_third", Float),
    Column("percent_defensive_half", Float),
    Column("percent_offensive_half", Float),
    Column("percent_behind_ball", Float),
    Column("percent_infront_ball", Float),
    Column("percent_most_back", Float),
    Column("percent_most_forward", Float),
    Column("percent_closest_to_ball", Float),
    Column("percent_farthest_from_ball", Float),
)

# FUNCTIONS


def generate_match_hash(data):
    p_ids = []
    for side in ["blue", "orange"]:
        for p in data.get(side, {}).get("players", []):
            uid = p.get("id", {}).get("id")
            if uid:
                p_ids.append(str(uid))
    p_ids.sort()
    blue_score = data.get("blue", {}).get("stats", {}).get("core", {}).get("goals", 0)
    orange_score = (
        data.get("orange", {}).get("stats", {}).get("core", {}).get("goals", 0)
    )
    duration = data.get("duration", 0)
    raw_str = f"{''.join(p_ids)}_{duration}_{blue_score}_{orange_score}"
    return hashlib.sha256(raw_str.encode()).hexdigest()


platform_cache = {}
rank_cache = {}
player_cache = {}


def get_player_id(session, p_data):
    plat_info = p_data.get("id", {})
    plat_name, plat_uid = (
        plat_info.get("platform", "unknown"),
        plat_info.get("id", "unknown"),
    )
    key = f"{plat_name}_{plat_uid}"
    if key not in player_cache:
        res = session.execute(
            text("SELECT id FROM players WHERE platform_user_id = :u"), {"u": plat_uid}
        ).fetchone()
        if res:
            player_cache[key] = res[0]
        else:
            if plat_name not in platform_cache:
                p_res = session.execute(
                    text("SELECT id FROM platforms WHERE name = :n"), {"n": plat_name}
                ).fetchone()
                platform_cache[plat_name] = (
                    p_res[0]
                    if p_res
                    else session.execute(
                        platforms.insert().values(name=plat_name)
                    ).inserted_primary_key[0]
                )
            ins = session.execute(
                players.insert().values(
                    platform_id=platform_cache[plat_name],
                    platform_user_id=plat_uid,
                    name=p_data.get("name", "Unknown"),
                )
            )
            player_cache[key] = ins.inserted_primary_key[0]
    return player_cache[key]


# IMPORT
def run_import():
    print("Initialisation de la base...")
    metadata.create_all(engine)
    session = Session()
    files = list(Path(JSON_DIR).glob("*.json"))

    # ORDERED RANKS
    print("Étape 1 : Collecte des rangs...")
    found_ranks = {}
    for file_path in files:
        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                for side in ["blue", "orange"]:
                    for p in data.get(side, {}).get("players", []):
                        r = p.get("rank")
                        if r and r.get("name") and r["name"] not in found_ranks:
                            found_ranks[r["name"]] = {
                                "tier": r.get("tier", 0),
                                "division": r.get("division", 0),
                                "name": r["name"],
                            }
        except Exception:
            continue

    sorted_ranks = sorted(
        found_ranks.values(), key=lambda x: (x["tier"], x["division"])
    )
    for r_data in sorted_ranks:
        ins = session.execute(ranks.insert().values(**r_data))
        rank_cache[r_data["name"]] = ins.inserted_primary_key[0]
    session.commit()

    # MATCHS & STATS

    print(f"Étape 2 : Importation de {len(files)} fichiers...")
    stats_counters = {"matches": 0, "skipped": 0, "errors": 0}

    for i, file_path in enumerate(files):
        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            m_id = generate_match_hash(data)
            if session.execute(
                text("SELECT 1 FROM matches WHERE id = :id"), {"id": m_id}
            ).fetchone():
                stats_counters["skipped"] += 1
                continue

            session.execute(
                matches.insert().values(
                    id=m_id,
                    playlist_id=data.get("playlist_id"),
                    season=data.get("season", 0),
                    duration=data.get("duration", 0),
                    overtime=data.get("overtime", False),
                    date_upload="2024-01-01",
                )
            )

            for color in ["blue", "orange"]:
                team = data.get(color, {})
                ball = team.get("stats", {}).get("ball", {})
                res_team = session.execute(
                    match_teams.insert().values(
                        match_id=m_id,
                        color=color,
                        score=team.get("stats", {}).get("core", {}).get("goals", 0),
                        possession_time=ball.get("possession_time", 0),
                        time_in_side=ball.get("time_in_side", 0),
                    )
                )
                t_id = res_team.inserted_primary_key[0]

                for p in team.get("players", []):
                    p_id = get_player_id(session, p)
                    r_id = rank_cache.get(p.get("rank", {}).get("name", "Unranked"))

                    res_part = session.execute(
                        match_participation.insert().values(
                            match_team_id=t_id,
                            player_id=p_id,
                            rank_id=r_id,
                            car_id=p.get("car_id"),
                            car_name=p.get("car_name", "Unknown"),
                            mvp=p.get("mvp", False),
                            start_time=p.get("start_time", 0),
                            end_time=p.get("end_time", 0),
                        )
                    )
                    part_id = res_part.inserted_primary_key[0]

                    st = p.get("stats", {})

                    # CORE
                    c = st.get("core", {})
                    session.execute(
                        stats_core.insert().values(
                            participation_id=part_id,
                            shots=c.get("shots", 0),
                            goals=c.get("goals", 0),
                            saves=c.get("saves", 0),
                            assists=c.get("assists", 0),
                            score=c.get("score", 0),
                            shooting_percentage=c.get("shooting_percentage", 0),
                            demo_inflicted=st.get("demo", {}).get("inflicted", 0),
                            demo_taken=st.get("demo", {}).get("taken", 0),
                        )
                    )

                    # BOOOOOOST
                    b = st.get("boost", {})
                    session.execute(
                        stats_boost.insert().values(
                            participation_id=part_id,
                            boost_per_minute=b.get("bpm", 0),
                            boost_consumed_per_minute=b.get("bcpm", 0),
                            average_amount=b.get("avg_amount", 0),
                            amount_collected=b.get("amount_collected", 0),
                            amount_stolen=b.get("amount_stolen", 0),
                            amount_collected_big=b.get("amount_collected_big", 0),
                            amount_stolen_big=b.get("amount_stolen_big", 0),
                            amount_collected_small=b.get("amount_collected_small", 0),
                            amount_stolen_small=b.get("amount_stolen_small", 0),
                            count_collected_big=b.get("count_collected_big", 0),
                            count_stolen_big=b.get("count_stolen_big", 0),
                            count_collected_small=b.get("count_collected_small", 0),
                            count_stolen_small=b.get("count_stolen_small", 0),
                            amount_overfill=b.get("amount_overfill", 0),
                            amount_overfill_stolen=b.get("amount_overfill_stolen", 0),
                            amount_used_while_supersonic=b.get(
                                "amount_used_while_supersonic", 0
                            ),
                            time_zero_boost=b.get("time_zero_boost", 0),
                            percent_zero_boost=b.get("percent_zero_boost", 0),
                            time_full_boost=b.get("time_full_boost", 0),
                            percent_full_boost=b.get("percent_full_boost", 0),
                            time_boost_0_25=b.get("time_boost_0_25", 0),
                            time_boost_25_50=b.get("time_boost_25_50", 0),
                            time_boost_50_75=b.get("time_boost_50_75", 0),
                            time_boost_75_100=b.get("time_boost_75_100", 0),
                            percent_boost_0_25=b.get("percent_boost_0_25", 0),
                            percent_boost_25_50=b.get("percent_boost_25_50", 0),
                            percent_boost_50_75=b.get("percent_boost_50_75", 0),
                            percent_boost_75_100=b.get("percent_boost_75_100", 0),
                        )
                    )

                    # SCHMOVEMENT
                    m = st.get("movement", {})
                    session.execute(
                        stats_movement.insert().values(
                            participation_id=part_id,
                            avg_speed=m.get("avg_speed", 0),
                            total_distance=m.get("total_distance", 0),
                            time_supersonic_speed=m.get("time_supersonic_speed", 0),
                            time_boost_speed=m.get("time_boost_speed", 0),
                            time_slow_speed=m.get("time_slow_speed", 0),
                            time_ground=m.get("time_ground", 0),
                            time_low_air=m.get("time_low_air", 0),
                            time_high_air=m.get("time_high_air", 0),
                            time_powerslide=m.get("time_powerslide", 0),
                            count_powerslide=m.get("count_powerslide", 0),
                            avg_powerslide_duration=m.get("avg_powerslide_duration", 0),
                            avg_speed_percentage=m.get("avg_speed_percentage", 0),
                            percent_slow_speed=m.get("percent_slow_speed", 0),
                            percent_boost_speed=m.get("percent_boost_speed", 0),
                            percent_supersonic_speed=m.get(
                                "percent_supersonic_speed", 0
                            ),
                            percent_ground=m.get("percent_ground", 0),
                            percent_low_air=m.get("percent_low_air", 0),
                            percent_high_air=m.get("percent_high_air", 0),
                        )
                    )

                    # POS
                    po = st.get("positioning", {})
                    session.execute(
                        stats_positioning.insert().values(
                            participation_id=part_id,
                            average_distance_to_ball=po.get("avg_distance_to_ball", 0),
                            average_distance_to_mates=po.get(
                                "avg_distance_to_mates", 0
                            ),
                            time_defensive_third=po.get("time_defensive_third", 0),
                            time_neutral_third=po.get("time_neutral_third", 0),
                            time_offensive_third=po.get("time_offensive_third", 0),
                            time_behind_ball=po.get("time_behind_ball", 0),
                            time_infront_ball=po.get("time_infront_ball", 0),
                            time_most_back=po.get("time_most_back", 0),
                            time_most_forward=po.get("time_most_forward", 0),
                            goals_against_while_last_defender=po.get(
                                "goals_against_while_last_defender", 0
                            ),
                            time_closest_to_ball=po.get("time_closest_to_ball", 0),
                            time_farthest_to_ball=po.get("time_farthest_to_ball", 0),
                            percent_defensive_third=po.get(
                                "percent_defensive_third", 0
                            ),
                            percent_neutral_third=po.get("percent_neutral_third", 0),
                            percent_offensive_third=po.get(
                                "percent_offensive_third", 0
                            ),
                            percent_defensive_half=po.get("percent_defensive_half", 0),
                            percent_offensive_half=po.get("percent_offensive_half", 0),
                            percent_behind_ball=po.get("percent_behind_ball", 0),
                            percent_infront_ball=po.get("percent_infront_ball", 0),
                            percent_most_back=po.get("percent_most_back", 0),
                            percent_most_forward=po.get("percent_most_forward", 0),
                            percent_closest_to_ball=po.get(
                                "percent_closest_to_ball", 0
                            ),
                            percent_farthest_from_ball=po.get(
                                "percent_farthest_from_ball", 0
                            ),
                        )
                    )

            stats_counters["matches"] += 1
            if i % 1000 == 0:
                session.commit()
                print(
                    f"[{i}/{len(files)}] Imported: {stats_counters['matches']} | duplicated: {stats_counters['skipped']}"
                )

        except Exception as e:
            session.rollback()
            stats_counters["errors"] += 1
            print(f"Erreur sur {file_path.name}: {e}")

    session.commit()
    print(
        f"\nUniques matches: {stats_counters['matches']}, Ignored duplicated: {stats_counters['skipped']}, Errors: {stats_counters['errors']}"
    )


if __name__ == "__main__":
    run_import()
