/* ==========================================
   1. TABLES DE RÉFÉRENCE (GLOBALES)
   ========================================== */

CREATE TABLE "platforms"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE "platforms" ADD PRIMARY KEY("id");

CREATE TABLE "ranks"(
    "id" BIGINT NOT NULL,
    "tier" INTEGER NOT NULL,
    "division" INTEGER NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE "ranks" ADD PRIMARY KEY("id");

CREATE TABLE "players"(
    "id" BIGINT NOT NULL,
    "platform_id" BIGINT NOT NULL,
    "platform_user_id" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE "players" ADD PRIMARY KEY("id");

CREATE TABLE "users"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "date_creation" DATE NOT NULL,
    "ingame_account_id" BIGINT,
    CONSTRAINT "unique_ingame_link" UNIQUE ("ingame_account_id")
);
ALTER TABLE "users" ADD PRIMARY KEY("id");

/* ==========================================
   2. TABLES DE MATCHS & STRUCTURE
   ========================================== */

CREATE TABLE "matches"(
    "id" UUID NOT NULL,
    "playlist_id" VARCHAR(255) NOT NULL,
    "season" INTEGER NOT NULL,
    "duration" INTEGER NOT NULL,
    "overtime" BOOLEAN NOT NULL,
    "date_upload" DATE NOT NULL
);
ALTER TABLE "matches" ADD PRIMARY KEY("id");

CREATE TABLE "match_teams"(
    "id" BIGINT NOT NULL,
    "match_id" BIGINT NOT NULL,
    "color" VARCHAR(10) NOT NULL,
    "score" INTEGER NOT NULL,
    "possession_time" FLOAT(53) NOT NULL,
    "time_in_side" FLOAT(53) NOT NULL
);
ALTER TABLE "match_teams" ADD PRIMARY KEY("id");

CREATE TABLE "match_participation"(
    "id" BIGINT NOT NULL,
    "match_team_id" BIGINT NOT NULL,
    "player_id" BIGINT NOT NULL,
    "rank_id" BIGINT NOT NULL,
    "car_id" INTEGER NOT NULL,
    "car_name" VARCHAR(255) NOT NULL,
    "mvp" BOOLEAN NOT NULL,
    "start_time" FLOAT(53) NOT NULL,
    "end_time" FLOAT(53) NOT NULL
);
ALTER TABLE "match_participation" ADD PRIMARY KEY("id");

/* ==========================================
   3. TABLES DE STATISTIQUES
   ========================================== */

CREATE TABLE "stats_core"(
    "participation_id" BIGINT NOT NULL,
    "shots" INTEGER NOT NULL,
    "goals" INTEGER NOT NULL,
    "saves" INTEGER NOT NULL,
    "assists" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    "shooting_percentage" FLOAT(53) NOT NULL,
    "demo_inflicted" INTEGER NOT NULL,
    "demo_taken" INTEGER NOT NULL
);
ALTER TABLE "stats_core" ADD PRIMARY KEY("participation_id");

CREATE TABLE "stats_boost"(
    "participation_id" BIGINT NOT NULL,
    "boost_per_minute" FLOAT(53) NOT NULL,
    "boost_consumed_per_minute" FLOAT(53) NOT NULL,
    "average_amount" FLOAT(53) NOT NULL,
    "amount_collected" BIGINT NOT NULL,
    "amount_stolen" BIGINT NOT NULL,
    "amount_collected_big" BIGINT NOT NULL,
    "amount_stolen_big" BIGINT NOT NULL,
    "amount_collected_small" BIGINT NOT NULL,
    "amount_stolen_small" BIGINT NOT NULL,
    "count_collected_big" BIGINT NOT NULL,
    "count_stolen_big" BIGINT NOT NULL,
    "count_collected_small" BIGINT NOT NULL,
    "count_stolen_small" BIGINT NOT NULL,
    "amount_overfill" BIGINT NOT NULL,
    "amount_overfill_stolen" BIGINT NOT NULL,
    "amount_used_while_supersonic" BIGINT NOT NULL,
    "time_zero_boost" FLOAT(53) NOT NULL,
    "percent_zero_boost" FLOAT(53) NOT NULL,
    "time_full_boost" FLOAT(53) NOT NULL,
    "percent_full_boost" FLOAT(53) NOT NULL,
    "time_boost_0_25" FLOAT(53) NOT NULL,
    "time_boost_25_50" FLOAT(53) NOT NULL,
    "time_boost_50_75" FLOAT(53) NOT NULL,
    "time_boost_75_100" FLOAT(53) NOT NULL,
    "percent_boost_0_25" FLOAT(53) NOT NULL,
    "percent_boost_25_50" FLOAT(53) NOT NULL,
    "percent_boost_50_75" FLOAT(53) NOT NULL,
    "percent_boost_75_100" FLOAT(53) NOT NULL
);
ALTER TABLE "stats_boost" ADD PRIMARY KEY("participation_id");

CREATE TABLE "stats_movement"(
    "participation_id" BIGINT NOT NULL,
    "avg_speed" BIGINT NOT NULL,
    "total_distance" BIGINT NOT NULL,
    "time_supersonic_speed" FLOAT(53) NOT NULL,
    "time_boost_speed" FLOAT(53) NOT NULL,
    "time_slow_speed" FLOAT(53) NOT NULL,
    "time_ground" FLOAT(53) NOT NULL,
    "time_low_air" FLOAT(53) NOT NULL,
    "time_high_air" FLOAT(53) NOT NULL,
    "time_powerslide" FLOAT(53) NOT NULL,
    "count_powerslide" BIGINT NOT NULL,
    "average_powerslide_duration" FLOAT(53) NOT NULL,
    "average_speed_percentage" FLOAT(53) NOT NULL,
    "percent_slow_speed" FLOAT(53) NOT NULL,
    "percent_boost_speed" FLOAT(53) NOT NULL,
    "percent_supersonic_speed" FLOAT(53) NOT NULL,
    "percent_ground" FLOAT(53) NOT NULL,
    "percent_low_air" FLOAT(53) NOT NULL,
    "percent_high_air" FLOAT(53) NOT NULL
);
ALTER TABLE "stats_movement" ADD PRIMARY KEY("participation_id");

CREATE TABLE "stats_positioning"(
    "participation_id" BIGINT NOT NULL,
    "average_distance_to_ball" INTEGER NOT NULL,
    "average_distance_to_ball_possession" INTEGER NOT NULL,
    "average_distance_to_ball_no_possession" INTEGER NOT NULL,
    "average_distance_to_mates" INTEGER NOT NULL,
    "time_defensive_third" FLOAT(53) NOT NULL,
    "time_neutral_third" FLOAT(53) NOT NULL,
    "time_offensive_third" FLOAT(53) NOT NULL,
    "time_defensive_half" FLOAT(53) NOT NULL,
    "time_offensive_half" FLOAT(53) NOT NULL,
    "time_behind_ball" FLOAT(53) NOT NULL,
    "time_infront_ball" FLOAT(53) NOT NULL,
    "time_most_back" FLOAT(53) NOT NULL,
    "time_most_forward" FLOAT(53) NOT NULL,
    "goals_against_while_last_defender" INTEGER NOT NULL,
    "time_closest_to_ball" FLOAT(53) NOT NULL,
    "time_farthest_to_ball" FLOAT(53) NOT NULL,
    "percent_defensive_third" FLOAT(53) NOT NULL,
    "percent_offensive_third" FLOAT(53) NOT NULL,
    "percent_neutral_third" FLOAT(53) NOT NULL,
    "percent_defensive_half" FLOAT(53) NOT NULL,
    "percent_offensive_half" FLOAT(53) NOT NULL,
    "percent_behind_ball" FLOAT(53) NOT NULL,
    "percent_infront_ball" FLOAT(53) NOT NULL,
    "percent_most_back" FLOAT(53) NOT NULL,
    "percent_most_forward" FLOAT(53) NOT NULL,
    "percent_closest_to_ball" FLOAT(53) NOT NULL,
    "percent_farthest_from_ball" FLOAT(53) NOT NULL
);
ALTER TABLE "stats_positioning" ADD PRIMARY KEY("participation_id");

/* ==========================================
   4. FONCTION DE HASH PASSWORD
   ========================================== */

CREATE OR REPLACE FUNCTION hash_password(password TEXT, sel TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN encode(sha256((password || sel)::bytea), 'hex');
END;
$$ LANGUAGE plpgsql
;

/* ==========================================
   5. RELATIONS ET CLÉS ÉTRANGÈRES
   ========================================== */

/* Link Player -> Plateform */
ALTER TABLE "players"
ADD CONSTRAINT "fk_players_platform" FOREIGN KEY("platform_id") REFERENCES "platforms"("id");

/* Link User -> Player */
ALTER TABLE "users"
ADD CONSTRAINT "fk_users_players" FOREIGN KEY("ingame_account_id") REFERENCES "players"("id");

/* Link Match -> Teams */
ALTER TABLE "match_teams"
ADD CONSTRAINT "fk_match_teams_match" FOREIGN KEY("match_id") REFERENCES "matches"("id") ON DELETE CASCADE;

/* Links Participation -> Team, Player, Rank */
ALTER TABLE "match_participation"
ADD CONSTRAINT "fk_participation_team" FOREIGN KEY("match_team_id") REFERENCES "match_teams"("id") ON DELETE CASCADE;

ALTER TABLE "match_participation"
ADD CONSTRAINT "fk_participation_player" FOREIGN KEY("player_id") REFERENCES "players"("id");

ALTER TABLE "match_participation"
ADD CONSTRAINT "fk_participation_rank" FOREIGN KEY("rank_id") REFERENCES "ranks"("id");

/* Liens Stats (Enfant) -> Participation (Parent) */
ALTER TABLE "stats_core"
ADD CONSTRAINT "fk_stats_core_participation" FOREIGN KEY("participation_id") REFERENCES "match_participation"("id") ON DELETE CASCADE;

ALTER TABLE "stats_boost"
ADD CONSTRAINT "fk_stats_boost_participation" FOREIGN KEY("participation_id") REFERENCES "match_participation"("id") ON DELETE CASCADE;

ALTER TABLE "stats_movement"
ADD CONSTRAINT "fk_stats_movement_participation" FOREIGN KEY("participation_id") REFERENCES "match_participation"("id") ON DELETE CASCADE;

ALTER TABLE "stats_positioning"
ADD CONSTRAINT "fk_stats_positioning_participation" FOREIGN KEY("participation_id") REFERENCES "match_participation"("id") ON DELETE CASCADE;
