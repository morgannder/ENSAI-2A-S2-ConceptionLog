/**
 * Client API pour communiquer avec le backend Rocket League Stats
 */

// ── Configuration Dynamique de l'URL ──────────────────────────────────────────
// En production, Vite lira l'URL "http://rocketcl..." depuis ton fichier .env.production
// En local, s'il ne trouve pas la variable, il utilisera "/api" (ton proxy local)
const API_BASE = import.meta.env.VITE_API_URL || "/api";

// ── Données statiques des Rangs avec icônes, couleurs et images ────────────
export const RANKS = [
  { name: "Bronze I",          fullName: "Bronze I",          color: "#cd7f32", glow: "#cd7f3255", icon: "🥉", image: "/images/ranks/bronze_1.png"        },
  { name: "Bronze II",         fullName: "Bronze II",         color: "#cd7f32", glow: "#cd7f3255", icon: "🥉", image: "/images/ranks/bronze_2.png"        },
  { name: "Bronze III",        fullName: "Bronze III",        color: "#cd7f32", glow: "#cd7f3255", icon: "🥉", image: "/images/ranks/bronze_3.png"        },
  { name: "Silver I",          fullName: "Silver I",          color: "#a8a9ad", glow: "#a8a9ad55", icon: "🥈", image: "/images/ranks/argent_1.png"        },
  { name: "Silver II",         fullName: "Silver II",         color: "#a8a9ad", glow: "#a8a9ad55", icon: "🥈", image: "/images/ranks/argent_2.png"        },
  { name: "Silver III",        fullName: "Silver III",        color: "#a8a9ad", glow: "#a8a9ad55", icon: "🥈", image: "/images/ranks/argent_3.png"        },
  { name: "Gold I",            fullName: "Gold I",            color: "#ffd700", glow: "#ffd70055", icon: "🥇", image: "/images/ranks/or_1.png"            },
  { name: "Gold II",           fullName: "Gold II",           color: "#ffd700", glow: "#ffd70055", icon: "🥇", image: "/images/ranks/or_2.png"            },
  { name: "Gold III",          fullName: "Gold III",          color: "#ffd700", glow: "#ffd70055", icon: "🥇", image: "/images/ranks/or_3.png"            },
  { name: "Platinum I",        fullName: "Platinum I",        color: "#00cfff", glow: "#00cfff55", icon: "💠", image: "/images/ranks/platine_1.png"       },
  { name: "Platinum II",       fullName: "Platinum II",       color: "#00cfff", glow: "#00cfff55", icon: "💠", image: "/images/ranks/platine_2.png"       },
  { name: "Platinum III",      fullName: "Platinum III",      color: "#00cfff", glow: "#00cfff55", icon: "💠", image: "/images/ranks/platine_3.png"       },
  { name: "Diamond I",         fullName: "Diamond I",         color: "#6a9de0", glow: "#6a9de055", icon: "💎", image: "/images/ranks/diamant_1.png"       },
  { name: "Diamond II",        fullName: "Diamond II",        color: "#6a9de0", glow: "#6a9de055", icon: "💎", image: "/images/ranks/diamant_2.png"       },
  { name: "Diamond III",       fullName: "Diamond III",       color: "#6a9de0", glow: "#6a9de055", icon: "💎", image: "/images/ranks/diamant_3.png"       },
  { name: "Champion I",        fullName: "Champion I",        color: "#c44dff", glow: "#c44dff55", icon: "👑", image: "/images/ranks/champion_1.png"      },
  { name: "Champion II",       fullName: "Champion II",       color: "#c44dff", glow: "#c44dff55", icon: "👑", image: "/images/ranks/champion_2.png"      },
  { name: "Champion III",      fullName: "Champion III",      color: "#c44dff", glow: "#c44dff55", icon: "👑", image: "/images/ranks/champion_3.png"      },
  { name: "Grand Champion I",  fullName: "Grand Champion I",  color: "#00ddff", glow: "#00ddff55", icon: "⭐", image: "/images/ranks/grand_champion_1.png" },
  { name: "Grand Champion II", fullName: "Grand Champion II", color: "#00ddff", glow: "#00ddff55", icon: "⭐", image: "/images/ranks/grand_champion_2.png" },
  { name: "Grand Champion III",fullName: "Grand Champion III",color: "#00ddff", glow: "#00ddff55", icon: "⭐", image: "/images/ranks/grand_champion_3.png" },
  { name: "Supersonic Legend", fullName: "Supersonic Legend", color: "#ff00ff", glow: "#ff00ff55", icon: "🚀", image: "/images/ranks/ssl.png"             },
  { name: "Unranked",          fullName: "Unranked",          color: "#888888", glow: "#88888855", icon: "❓", image: "/images/ranks/unranked.png"        },
];

/**
 * Extract the base rank name from any API rank string, then find the matching entry.
 * Uses the same regex as PlayerPage: captures "Word(s) + Roman numerals" at the start.
 * e.g. "Platinum II Division 2" → "Platinum II" → RANKS entry for Platinum II
 */
export function findRankInfo(rankStr) {
  if (!rankStr) return null;
  const extracted = rankStr.match(/^([A-Za-z\s]+\s[IVX]+)/)?.[1]?.trim() || rankStr.trim();
  return (
    RANKS.find((r) => r.fullName === extracted) ||
    RANKS.find((r) => r.fullName === rankStr.trim()) ||
    RANKS.find((r) => r.name    === rankStr.trim()) ||
    null
  );
}

// ── Données statiques des Plateformes ────────────────────────────────────────
export const PLATFORMS = [
  { id: "epic",    label: "Epic",        icon: "◈",  logo: "/images/platforms/epic.png"  },
  { id: "steam",   label: "Steam",       icon: "⬡",  logo: "/images/platforms/steam.png" },
  { id: "psn",     label: "PlayStation", icon: "▲",  logo: "/images/platforms/psn.png"   },
  { id: "xbox",    label: "Xbox",        icon: "⊞",  logo: "/images/platforms/xbox.png"  },
  { id: "switch",  label: "Switch",      icon: "⊕",  logo: "/images/platforms/switch.png"},
  { id: "psynet",  label: "PsyNet",      icon: "⬡",  logo: null                          },
];

// Normalize any platform string the API might return → canonical id
const PLATFORM_MAPPING = {
  // Epic
  "epic": "epic", "Epic": "epic", "EPIC": "epic",
  // Steam
  "steam": "steam", "Steam": "steam", "STEAM": "steam",
  // PlayStation — accept both ps4 and psn
  "psn": "psn", "PlayStation": "psn", "PSN": "psn",
  "ps4": "psn", "PS4": "psn", "playstation": "psn",
  // Xbox
  "xbox": "xbox", "Xbox": "xbox", "XBOX": "xbox",
  // Switch
  "switch": "switch", "Switch": "switch", "SWITCH": "switch",
  // PsyNet
  "psynet": "psynet", "PsyNet": "psynet", "PSYNET": "psynet",
};

function normalizePlatform(platformName) {
  if (!platformName) return "epic";
  return PLATFORM_MAPPING[platformName] || platformName.toLowerCase();
}

// ── Recherche de joueurs ──────────────────────────────────────────────────────
export async function searchPlayers(pseudonym, platform = null, limit = 30) {
  const params = new URLSearchParams({ pseudonym, limit });
  if (platform) params.append("platform", platform);

  const response = await fetch(`${API_BASE}/global/search?${params}`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

  const data = await response.json();
  return (data.results || []).map((player) => ({
    ...player,
    platform: normalizePlatform(player.platform),
    id: player.platform_user_id,
  }));
}

// ── Rang d'un joueur ──────────────────────────────────────────────────────────
export async function getPlayerRank(platformId) {
  const response = await fetch(`${API_BASE}/player/player/${platformId}/rank`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return response.json();
}

// ── Stats Core ────────────────────────────────────────────────────────────────
export async function getPlayerCoreStats(platformId, gameMode = null) {
  const params = new URLSearchParams({ platform_id: platformId });
  if (gameMode) params.append("game_mode", gameMode);

  const url = `${API_BASE}/statscore/player/${platformId}/averagecore?${params}`;
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return response.json();
}

// ── Stats Boost ───────────────────────────────────────────────────────────────
export async function getPlayerBoostStats(platformId) {
  const response = await fetch(`${API_BASE}/statsboost/player/${platformId}/averageboost`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return response.json();
}

// ── Player research update ─────────────────────────────────────────────────
export async function requestPlayerUpdate({ playerPlatform, playerId, playerExactPseudo, gameCount = 1, createdAfter = "2024-01-01T00:00:00Z" }) {
  const params = new URLSearchParams();
  if (playerPlatform) params.append("player_platform", playerPlatform);
  if (playerId)       params.append("player_id", playerId);
  if (playerExactPseudo) params.append("player_exact_pseudo", playerExactPseudo);
  params.append("game_count", gameCount);
  params.append("created_after", createdAfter);

  const response = await fetch(`${API_BASE}/global/player-research-update/?${params}`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return response.json();
}

// ── Stats par Rang (Global) ───────────────────────────────────────────────────
export async function getRankStats(route, rankName, gameMode) {
  const params = new URLSearchParams({ rank_name: rankName, game_mode: gameMode });
  const response = await fetch(`${API_BASE}/${route}/%7Brank%7D?${params}`);
  if (response.status === 404) return null;
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  const json = await response.json();
  return json.data ?? json;
}
