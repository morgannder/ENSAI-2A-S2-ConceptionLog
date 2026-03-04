import { useState, useEffect, useRef } from "react";
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
    { label: "Goals",           value: stats.goals               != null ? Number(stats.goals).toFixed(1)                     : "—", sub: "per game",  color: "var(--orange)" },
    { label: "Assists",         value: stats.assists             != null ? Number(stats.assists).toFixed(1)                   : "—", sub: "per game",  color: "var(--purple)" },
    { label: "Saves",           value: stats.saves               != null ? Number(stats.saves).toFixed(1)                    : "—", sub: "per game",  color: "#00ff88"       },
    { label: "Shots",           value: stats.shots               != null ? Number(stats.shots).toFixed(1)                    : "—", sub: "per game",  color: "#ff4e50"       },
    { label: "Shooting %",      value: stats.shooting_percentage != null ? `${Number(stats.shooting_percentage).toFixed(1)}%` : "—", sub: "accuracy",  color: "var(--cyan)"   },
    { label: "Score",           value: stats.score               != null ? Number(stats.score).toFixed(0)                    : "—", sub: "per match", color: "#ffd700"       },
    { label: "Demos Inflicted", value: stats.demo_inflicted      != null ? Number(stats.demo_inflicted).toFixed(1)            : "—", sub: "per game",  color: "#ff6b1a"       },
    { label: "Demos Taken",     value: stats.demo_taken          != null ? Number(stats.demo_taken).toFixed(1)                : "—", sub: "per game",  color: "#b347ff"       },
  ];
};

async function fetchModeWithRetry(platformId, modeId, maxRetries = 3) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      if (attempt > 0) await new Promise(r => setTimeout(r, 400 * Math.pow(2, attempt - 1)));
      const data = await getPlayerCoreStats(platformId, modeId);
      if (data === null) return { stats: null, error: null };
      const stats = data?.data ?? data?.stats ?? data ?? null;
      if (stats && typeof stats === "object" && Object.keys(stats).length === 0) {
        return { stats: null, error: null };
      }
      return { stats, error: null };
    } catch (err) {
      const is5xx = /5\d\d/.test(err.message);
      if (is5xx && attempt < maxRetries) {
        await new Promise(r => setTimeout(r, 300 * Math.pow(2, attempt)));
        continue;
      }
      return { stats: null, error: null };
    }
  }
  return { stats: null, error: null };
}

function loadAllModes(pid, cancelRef, setModes) {
  setModes(GAME_MODES.map(m => ({ id: m.id, stats: null, error: null, loading: true })));
  GAME_MODES.forEach((mode, idx) => {
    setTimeout(() => {
      if (cancelRef.current) return;
      fetchModeWithRetry(pid, mode.id).then(({ stats, error }) => {
        if (cancelRef.current) return;
        setModes(prev => {
          const next = [...prev];
          next[idx] = { id: mode.id, stats, error, loading: false };
          return next;
        });
      });
    }, idx * 300);
  });
}

export default function PlayerPage({ player, onBack, onPlayerClick }) {
  const [selectedMode,  setSelectedMode]  = useState("ranked-duels");
  const [modes,         setModes]         = useState(
    GAME_MODES.map(m => ({ id: m.id, stats: null, error: null, loading: true }))
  );
  const [refreshing,    setRefreshing]    = useState(false);
  const [refreshResult, setRefreshResult] = useState(null);
  const [matchesKey,    setMatchesKey]    = useState(0);

  const cancelRef = useRef(false);

  const rankMatch = player.rank?.match(/^([A-Za-z\s]+\s[IVX]+)/)?.[1] || player.rank || "Unranked";
  const rankInfo  = RANKS.find(r => r.fullName === rankMatch);
  const platInfo  = PLATFORMS.find(p => p.id === player.platform);

  useEffect(() => {
    const pid = player.platform_user_id;
    if (!pid) return;
    cancelRef.current = false;
    loadAllModes(pid, cancelRef, setModes);
    return () => { cancelRef.current = true; };
  }, [player.platform_user_id]);

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

      const newMatches = res?.details?.new_matches_downloaded ?? res?.new_matches_downloaded ?? 0;
      const total      = res?.details?.total_analysed ?? res?.total_analysed ?? 0;

      setRefreshResult({ success: true, newMatches, total, data: res });

      await new Promise(r => setTimeout(r, 1500));
      cancelRef.current = false;
      loadAllModes(player.platform_user_id, cancelRef, setModes);
      setMatchesKey(k => k + 1);
    } catch (err) {
      setRefreshResult({ success: false, message: err.message });
    } finally {
      setRefreshing(false);
    }
  };

  const anyLoading    = modes.some(m => m.loading);
  const currentSlot   = modes.find(m => m.id === selectedMode) ?? modes[0];
  const isLoadingMode = currentSlot.loading;
  const currentStats  = currentSlot.stats;
  const hasData       = currentStats && Object.keys(currentStats).length > 0;
  const coreCards     = getCoreStatsCards(currentStats);

  return (
    <div className="fade-in">
      <button className="back-btn" onClick={onBack}>← Back</button>

      {/* ── Header ── */}
      <div className="player-header">
        <div className="player-header-bg" />
        {rankInfo?.image
          ? <img src={rankInfo.image} alt={rankMatch} className="player-avatar-img" />
          : <div className="player-avatar">{rankInfo?.icon || "🎮"}</div>
        }
        <div className="player-info">
          <div className="player-name">{player.name}</div>
          <div className="player-meta">
            <span className="player-badge platform-badge">
              {platInfo?.logo && <img src={platInfo.logo} alt={platInfo.label} style={{ width: 14, height: 14, objectFit: "contain", verticalAlign: "middle" }} />}
              {" "}{platInfo?.label}
            </span>
            <span className="player-badge rank-badge" style={{ color: rankInfo?.color, borderColor: rankInfo?.color, background: rankInfo?.glow }}>
              {player.rank}
            </span>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 6, flexShrink: 0 }}>
          <button onClick={handleRefresh} disabled={refreshing} style={{
            padding: "8px 18px", borderRadius: 8,
            border: "1px solid rgba(0,229,255,0.3)",
            background: refreshing ? "rgba(0,229,255,0.04)" : "rgba(0,229,255,0.08)",
            color: "var(--cyan)", fontFamily: "'Exo 2', sans-serif",
            fontWeight: 700, fontSize: "0.78rem", letterSpacing: "0.08em",
            textTransform: "uppercase", transition: "all .2s",
            display: "flex", alignItems: "center", gap: 6,
            opacity: refreshing ? 0.6 : 1, cursor: refreshing ? "not-allowed" : "pointer",
            whiteSpace: "nowrap",
          }}>
            {refreshing ? "Fetching..." : "↻ Refresh Games"}
          </button>

          {refreshResult && (
            <div style={{ fontSize: "0.72rem", fontWeight: 600, textAlign: "right", fontFamily: "'Share Tech Mono', monospace", lineHeight: 1.6 }}>
              {refreshResult.success ? (<>
                <div style={{ color: refreshResult.newMatches > 0 ? "#00ff88" : "var(--muted)" }}>
                  {refreshResult.newMatches} new match(es)
                </div>
                <div style={{ color: "var(--muted)" }}>
                  {refreshResult.total} analysed
                  {refreshResult.data.latest_match_date
                    ? " · " + new Date(refreshResult.data.latest_match_date).toLocaleDateString()
                    : ""}
                </div>
              </>) : (
                <div style={{ color: "#ff6b6b" }}>Error: {refreshResult.message}</div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* ── Core Stats ── */}
      <div className="section-header" style={{ marginTop: "2rem" }}>
        <span className="section-title">Core Stats</span>
        <div className="section-line" />
        {anyLoading && (
          <span style={{ fontSize: "0.7rem", color: "var(--muted)", fontFamily: "'Share Tech Mono', monospace", display: "flex", alignItems: "center", gap: 6 }}>
            <span className="spinner" style={{ width: 12, height: 12, borderWidth: 2, display: "inline-block" }} />
            loading…
          </span>
        )}
      </div>

      <div className="game-mode-tabs">
        {GAME_MODES.map((mode, idx) => {
          const slot      = modes[idx];
          const isLoading = slot.loading;
          const hasOk     = !isLoading && !!slot.stats;
          const noData    = !isLoading && !slot.stats;
          return (
            <button key={mode.id} className={`game-mode-btn ${selectedMode === mode.id ? "active" : ""}`} onClick={() => setSelectedMode(mode.id)}>
              {mode.label}
              {isLoading && <span style={{ marginLeft: 6, fontSize: "0.65rem", color: "var(--muted)" }}>…</span>}
              {hasOk     && <span style={{ marginLeft: 6, fontSize: "0.65rem", color: "#00ff88" }}>✓</span>}
              {noData    && <span style={{ marginLeft: 6, fontSize: "0.65rem", color: "var(--muted)" }}>—</span>}
            </button>
          );
        })}
      </div>

      {isLoadingMode ? (
        <div style={{ textAlign: "center", padding: "3rem" }}>
          <div className="spinner" style={{ margin: "0 auto 16px" }} />
          <p className="overlay-text">Loading stats…</p>
        </div>
      ) : hasData ? (
        <div className="stats-grid">
          {coreCards.map(s => (
            <div key={s.label} className="stat-card" style={{ "--stat-color": s.color }}>
              <div className="stat-num">{s.value}</div>
              <div className="stat-label">{s.label}</div>
              <div className="stat-sub">{s.sub}</div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ textAlign: "center", padding: "2rem", color: "var(--muted)" }}>
          No stats available for this mode.
        </div>
      )}

      <RecentMatches key={matchesKey} player={player} onPlayerClick={onPlayerClick} />
    </div>
  );
}
