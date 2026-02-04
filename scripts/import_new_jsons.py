import hashlib
import json
from pathlib import Path
import sys

from sqlalchemy import (
    MetaData,
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker


# CONFIG
DB_PATH = "src/database/rocket_league.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
metadata = MetaData()
Session = sessionmaker(bind=engine)


metadata.reflect(bind=engine)


try:
    matches = metadata.tables["matches"]
    match_teams = metadata.tables["match_teams"]
    match_participation = metadata.tables["match_participation"]
    players = metadata.tables["players"]
    ranks = metadata.tables["ranks"]
    platforms = metadata.tables["platforms"]
    stats_core = metadata.tables["stats_core"]
    stats_boost = metadata.tables["stats_boost"]
    stats_movement = metadata.tables["stats_movement"]
    stats_positioning = metadata.tables["stats_positioning"]
except KeyError as e:
    print(f"Erreur critique: La table {e} n'existe pas dans la base de données.")
    sys.exit(1)


# FUNCTIONS


def generate_match_hash(data):
    """Génère un ID unique basé sur les joueurs, la durée et le score."""
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


def get_rank_id(session, r_data):
    """Récupère ou crée un rang."""
    if not r_data:
        return None

    # Gestion du nom pour éviter les erreurs si manquant
    name = r_data.get("name")
    if not name:
        return None

    # On cherche d'abord en base
    res = session.execute(
        text("SELECT id FROM ranks WHERE name = :n"), {"n": name}
    ).fetchone()

    if res:
        return res[0]

    # Sinon on crée (Attention: cela suppose que les rangs sont déjà peuplés/ordonnés,
    # sinon il sera ajouté à la fin)
    ins = session.execute(
        ranks.insert().values(
            tier=r_data.get("tier", 0), division=r_data.get("division", 0), name=name
        )
    )
    return ins.inserted_primary_key[0]


def get_player_id(session, p_data):
    """Récupère ou crée un joueur et sa plateforme."""
    plat_info = p_data.get("id", {})
    plat_name = plat_info.get("platform", "unknown")
    plat_uid = plat_info.get("id", "unknown")

    # 1. Chercher le joueur
    res = session.execute(
        text("SELECT id FROM players WHERE platform_user_id = :u"), {"u": plat_uid}
    ).fetchone()

    if res:
        return res[0]

    # 2. Si pas trouvé, gérer la plateforme
    p_res = session.execute(
        text("SELECT id FROM platforms WHERE name = :n"), {"n": plat_name}
    ).fetchone()

    if p_res:
        plat_id = p_res[0]
    else:
        plat_id = session.execute(
            platforms.insert().values(name=plat_name)
        ).inserted_primary_key[0]

    # 3. Créer le joueur
    ins = session.execute(
        players.insert().values(
            platform_id=plat_id,
            platform_user_id=plat_uid,
            name=p_data.get("name", "Unknown"),
        )
    )
    return ins.inserted_primary_key[0]


# --- FONCTION PRINCIPALE ---


def add_single_match(json_path):
    path = Path(json_path)
    if not path.exists():
        print(f"Erreur : Le fichier {json_path} est introuvable.")
        return

    print(f"Traitement du fichier : {path.name}")
    session = Session()

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        # 1. Génération et Vérification du Hash
        m_id = generate_match_hash(data)

        exists = session.execute(
            text("SELECT 1 FROM matches WHERE id = :id"), {"id": m_id}
        ).fetchone()

        if exists:
            print(f"⚠️ Le match {m_id} existe déjà en base. Ajout ignoré.")
            return

        # 2. Insertion du Match
        session.execute(
            matches.insert().values(
                id=m_id,
                playlist_id=data.get("playlist_id"),
                season=data.get("season", 0),
                duration=data.get("duration", 0),
                overtime=data.get("overtime", False),
                date_upload="2024-01-01",  # Tu peux rendre ça dynamique si le JSON a une date
            )
        )

        # 3. Insertion Équipes & Joueurs
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
                r_id = get_rank_id(session, p.get("rank"))

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

                # 4. Insertion des Stats
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

                # BOOST
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

                # MOVEMENT
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
                        percent_supersonic_speed=m.get("percent_supersonic_speed", 0),
                        percent_ground=m.get("percent_ground", 0),
                        percent_low_air=m.get("percent_low_air", 0),
                        percent_high_air=m.get("percent_high_air", 0),
                    )
                )

                # POSITIONING
                po = st.get("positioning", {})
                session.execute(
                    stats_positioning.insert().values(
                        participation_id=part_id,
                        average_distance_to_ball=po.get("avg_distance_to_ball", 0),
                        average_distance_to_mates=po.get("avg_distance_to_mates", 0),
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
                        percent_defensive_third=po.get("percent_defensive_third", 0),
                        percent_neutral_third=po.get("percent_neutral_third", 0),
                        percent_offensive_third=po.get("percent_offensive_third", 0),
                        percent_defensive_half=po.get("percent_defensive_half", 0),
                        percent_offensive_half=po.get("percent_offensive_half", 0),
                        percent_behind_ball=po.get("percent_behind_ball", 0),
                        percent_infront_ball=po.get("percent_infront_ball", 0),
                        percent_most_back=po.get("percent_most_back", 0),
                        percent_most_forward=po.get("percent_most_forward", 0),
                        percent_closest_to_ball=po.get("percent_closest_to_ball", 0),
                        percent_farthest_from_ball=po.get(
                            "percent_farthest_from_ball", 0
                        ),
                    )
                )

        session.commit()
        print(f"Match {m_id} ajouté avec succès !")

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'ajout du match : {e}")
    finally:
        session.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python add_match.py <chemin_vers_le_fichier.json>")
    else:
        add_single_match(sys.argv[1])
