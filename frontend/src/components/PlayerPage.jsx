import { useState, useEffect } from "react";
import { RANKS, PLATFORMS, getPlayerCoreStats, requestPlayerUpdate } from "../api/apiClient";
import RecentMatches from "./RecentMatches";

const GAME_MODES = [
  { id: "ranked-duels",    label: "Ranked 1V1" },
  { id: "ranked-doubles",  label: "Ranked 2V2" },
  { id: "ranked-standard", label: "Ranked 3V3" },
];

const getCoreStatsCards = (stats) => {
  if (!stats) return [];
  return [
    { label: "Goals",           value: stats.goals               != null ? Number(stats.goals).toFixed(1)                    : "—", sub: "per game",  color: "var(--orange)" },
    { label: "Assists",         value: stats.assists             != null ? Number(stats.assists).toFixed(1)                  : "—", sub: "per game",  color: "var(--purple)" },
    { label: "Saves",           value: stats.saves               != null ? Number(stats.saves).toFixed(1)                   : "—", sub: "per game",  color: "#00ff88"       },
    { label: "Shots",           value: stats.shots               != null ? Number(stats.shots).toFixed(1)                   : "—", sub: "per game",  color: "#ff4e50"       },
    { label: "Shooting %",      value: stats.shooting_percentage != null ? `${Number(stats.shooting_percentage).toFixed(1)}%` : "—", sub: "accuracy",  color: "var(--cyan)"   },
    { label: "Score",           value: stats.score               != null ? Number(stats.score).toFixed(0)                   : "—", sub: "per match", color: "#ffd700"       },
    { label: "Demos Inflicted", value: stats.demo_inflicted      != null ? Number(stats.demo_inflicted).toFixed(1)           : "—", sub: "per game",  color: "#ff6b1a"       },
    { label: "Demos Taken",     value: stats.demo_taken          != null ? Number(stats.demo_taken).toFixed(1)               : "—", sub: "per game",  color: "#b347ff"       },
  ];
};

async function fetchWithRetry(platformId, modeId, retries = 2) {
  for (let i = 0; i <= retries; i++) {
    try {
      const data = await getPlayerCoreStats(platformId, modeId);
      return { stats: data?.data ?? data?.stats ?? data ?? null, error: null };
    } catch (err) {
      const is500 = err.message.includes("500");
      if (is500 && i < retries) {
        await new Promise((r) => setTimeout(r, 300 * (i + 1)));
        continue;
      }
      return { stats: null, error: err.message };
    }
  }
}

export default function PlayerPage({ player, onBack, onPlayerClick }) {
  const [selectedMode,   setSelectedMode]   = useState("ranked-duels");
  const [modeStats,      setModeStats]      = useState({});
  const [modeErrors,     setModeErrors]     = useState({});
  const [loadingStats,   setLoadingStats]   = useState(false);
  const [refreshing,     setRefreshing]     = useState(false);
  const [refreshResult,  setRefreshResult]  = useState(null);
  const [matchesKey,     setMatchesKey]     = useState(0);

  const rankMatch = player.rank?.match(/^([A-Za-z\s]+\s[IVX]+)/)?.[1] || player.rank || "Unranked";
  const rankInfo  = RANKS.find((r) => r.fullName === rankMatch);
  const platInfo  = PLATFORMS.find((p) => p.id === player.platform);

  useEffect(() => {
    const platform_user_id = player.platform_user_id;
    if (!platform_user_id) return;

    setLoadingStats(true);
    setModeStats({});
    setModeErrors({});

    Promise.all(
      GAME_MODES.map((mode) =>
        fetchWithRetry(platform_user_id, mode.id).then(({ stats, error }) => ({
          mode: mode.id, stats, error,
        }))
      )
    ).then((results) => {
      const statsMap  = {};
      const errorsMap = {};
      results.forEach(({ mode, stats, error }) => {
        statsMap[mode]  = stats;
        errorsMap[mode] = error;
      });
      setModeStats(statsMap);
      setModeErrors(errorsMap);
    }).finally(() => setLoadingStats(false));
  }, [player]);

  const handleRefresh = async () => {
    setRefreshing(true);
    setRefreshResult(null);
    try {
      const res = await requestPlayerUpdate({
        playerPlatform: platInfo?.id ?? player.platform,
        playerId:       player.platform_user_id,
        gameCount:      5,
        createdAfter:   "2024-01-01T00:00:00Z",
      });
      setRefreshResult({ success: true, data: res });
      setMatchesKey(k => k + 1);
    } catch (err) {
      setRefreshResult({ success: false, message: err.message });
    } finally {
      setRefreshing(false);
    }
  };

  const currentStats = modeStats[selectedMode];
  const currentError = modeErrors[selectedMode];
  const hasData      = currentStats && Object.keys(currentStats).length > 0;
  const coreCards    = getCoreStatsCards(currentStats);

  return (
    <div className="fade-in">
      <button className="back-btn" onClick={onBack}>← Back</button>

      {/* ── Header ── */}
      <div className="player-header">
        <div className="player-header-bg" />
        {rankInfo?.image ? (
          <img src={rankInfo.image} alt={rankMatch} className="player-avatar-img" />
        ) : (
          <div className="player-avatar">{rankInfo?.icon || "🎮"}</div>
        )}
        <div className="player-info">
          <div className="player-name">{player.name}</div>
          <div className="player-meta">
            <span className="player-badge platform-badge">
              {platInfo?.logo ? <img src={platInfo.logo} alt={platInfo.label} style={{ width: 14, height: 14, objectFit: "contain", verticalAlign: "middle" }} /> : null} {platInfo?.label}
            </span>
            <span
              className="player-badge rank-badge"
              style={{ color: rankInfo?.color, borderColor: rankInfo?.color, background: rankInfo?.glow }}
            >
              {player.rank}
            </span>
          </div>
        </div>

        {/* ── Refresh button ── */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 6, flexShrink: 0 }}>
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            style={{
              padding: "8px 18px", borderRadius: 8,
              border: "1px solid rgba(0,229,255,0.3)",
              background: refreshing ? "rgba(0,229,255,0.04)" : "rgba(0,229,255,0.08)",
              color: "var(--cyan)", fontFamily: "'Exo 2', sans-serif",
              fontWeight: 700, fontSize: "0.78rem", letterSpacing: "0.08em",
              textTransform: "uppercase", transition: "all .2s",
              display: "flex", alignItems: "center", gap: 6,
              opacity: refreshing ? 0.6 : 1, cursor: refreshing ? "not-allowed" : "pointer",
              whiteSpace: "nowrap",
            }}
          >
            {refreshing ? "Fetching..." : "↻ Refresh Games"}
          </button>

          {refreshResult && (
            <div style={{
              fontSize: "0.72rem", fontWeight: 600, textAlign: "right",
              color: refreshResult.success ? "#00ff88" : "#ff6b6b",
              fontFamily: "'Share Tech Mono', monospace", lineHeight: 1.6,
            }}>
              {refreshResult.success ? (
                <>
                  <div>{refreshResult.data.details?.new_matches_downloaded ?? 0} new match(es)</div>
                  <div style={{ color: "var(--muted)" }}>
                    {refreshResult.data.details?.total_analysed ?? "?"} analysed
                    {refreshResult.data.latest_match_date
                      ? " · " + new Date(refreshResult.data.latest_match_date).toLocaleDateString()
                      : ""}
                  </div>
                </>
              ) : (
                <div>Error: {refreshResult.message}</div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* ── Core Stats ── */}
      <div className="section-header" style={{ marginTop: "2rem" }}>
        <span className="section-title">Core Stats</span>
        <div className="section-line" />
      </div>

      <div className="game-mode-tabs">
        {GAME_MODES.map((mode) => {
          const loaded = mode.id in modeStats;
          const hasErr = loaded && !!modeErrors[mode.id];
          const hasOk  = loaded && !!modeStats[mode.id];
          return (
            <button
              key={mode.id}
              className={`game-mode-btn ${selectedMode === mode.id ? "active" : ""}`}
              onClick={() => setSelectedMode(mode.id)}
            >
              {mode.label}
              {hasOk  && <span style={{ marginLeft: 6, fontSize: "0.65rem", color: "#00ff88" }}>✓</span>}
              {hasErr && <span style={{ marginLeft: 6, fontSize: "0.65rem", color: "#ff4e50" }}>✕</span>}
            </button>
          );
        })}
      </div>

      {loadingStats ? (
        <div style={{ textAlign: "center", padding: "3rem" }}>
          <div className="spinner" style={{ margin: "0 auto 16px" }} />
          <p className="overlay-text">Chargement des statistiques...</p>
        </div>
      ) : currentError ? (
        <div style={{ padding: "20px 24px", background: "rgba(255,78,80,0.08)", border: "1px solid rgba(255,78,80,0.25)", borderRadius: 12, color: "#ff6b6b", marginTop: 8 }}>
          <div style={{ fontWeight: 700, marginBottom: 6 }}>Aucune donnée pour ce mode</div>
          <div style={{ fontSize: "0.8rem", color: "var(--muted)", fontFamily: "'Share Tech Mono', monospace" }}>
            {currentError.includes("404") ? "Ce mode n'a pas encore de stats enregistrées."
              : currentError.includes("422") ? "Paramètre refusé — vérifie les noms de game_mode."
              : currentError.includes("500") ? "Erreur serveur — réessaie plus tard."
              : currentError}
          </div>
        </div>
      ) : hasData ? (
        <div className="stats-grid">
          {coreCards.map((s) => (
            <div key={s.label} className="stat-card" style={{ "--stat-color": s.color }}>
              <div className="stat-num">{s.value}</div>
              <div className="stat-label">{s.label}</div>
              <div className="stat-sub">{s.sub}</div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ textAlign: "center", padding: "2rem", color: "var(--muted)" }}>
          Aucune statistique disponible pour ce mode.
        </div>
      )}

      {/* key forces RecentMatches to re-mount and re-fetch after refresh */}
      <RecentMatches key={matchesKey} player={player} onPlayerClick={onPlayerClick} />
    </div>
  );
}
