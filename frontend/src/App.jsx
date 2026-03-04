import { useState, useEffect } from "react";
import { searchPlayers, getPlayerRank, getPlayerCoreStats, PLATFORMS, findRankInfo, requestPlayerUpdate } from "./api/apiClient";
import SearchBar   from "./components/SearchBar";
import PlayerPage  from "./components/PlayerPage";
import GlobalStats from "./components/GlobalStats";

const MAX_HISTORY = 10;

// ── Rank fetcher: updates suggestions live as each rank arrives ──────────────
async function fetchRanksLive(players, onRankLoaded, isCancelled, delay = 60) {
  for (const p of players) {
    if (isCancelled()) return;
    const id = p.platform_user_id ?? p.id;
    if (!id) continue;
    try {
      const rankData = await getPlayerRank(id);
      if (isCancelled()) return;
      if (rankData) onRankLoaded(id, rankData.full_rank ?? null, rankData.mmr ?? null);
    } catch {
    }
    if (delay > 0) await new Promise(r => setTimeout(r, delay));
  }
}

export default function App() {
  const [page,           setPage]           = useState("home");
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [searchQuery,    setSearchQuery]    = useState("");
  const [suggestions,    setSuggestions]    = useState([]);
  const [loading,        setLoading]        = useState(false);
  const [loadingPlayer,  setLoadingPlayer]  = useState(false);
  const [refreshing,     setRefreshing]     = useState(false);
  const [refreshResult,  setRefreshResult]  = useState(null);
  const [homeKey,        setHomeKey]        = useState(0);
  const [history,        setHistory]        = useState(() => {
    try {
      return JSON.parse(sessionStorage.getItem("rl_history") || "[]");
    } catch {
      return [];
    }
  });

  const [rankFetchId, setRankFetchId] = useState(0);

  useEffect(() => {
    if (searchQuery.length < 3) {
      setSuggestions([]);
      return;
    }

    let cancelled = false;
    const currentFetchId = Date.now();
    setRankFetchId(currentFetchId);
    setLoading(true);

    searchPlayers(searchQuery, null)
      .then(async (results) => {
        if (cancelled) return;
        if (!results || results.length === 0) {
          setSuggestions([]);
          return;
        }
        setSuggestions(results);
        await fetchRanksLive(
          results,
          (id, rank, mmr) => {
            setSuggestions(prev => prev.map(p =>
              (p.platform_user_id ?? p.id) === id ? { ...p, rank, mmr } : p
            ));
          },
          () => cancelled,
          60
        );
      })
      .catch(() => { if (!cancelled) setSuggestions([]); })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [searchQuery]);

  const handleSearch = () => {
    if (!searchQuery.trim() || suggestions.length === 0) return;
    openPlayer(suggestions[0]);
  };

  const addToHistory = (player) => {
    const { _openedAt, ...playerToSave } = player;
    setHistory((prev) => {
      const filtered = prev.filter(p => p.platform_user_id !== playerToSave.platform_user_id);
      const next = [playerToSave, ...filtered].slice(0, MAX_HISTORY);
      try { sessionStorage.setItem("rl_history", JSON.stringify(next)); } catch {}
      return next;
    });
  };

  const handleRefreshLatest = async () => {
    setRefreshing(true);
    setRefreshResult(null);
    try {
      const res = await requestPlayerUpdate({ gameCount: 10, createdAfter: "2024-01-01T00:00:00Z" });
      setRefreshResult({ success: true, data: res });
    } catch (err) {
      setRefreshResult({ success: false, message: err.message });
    } finally {
      setRefreshing(false);
    }
  };

  const goHome = () => {
    setPage("home");
    setSearchQuery("");
    setSuggestions([]);
    setHomeKey(k => k + 1);
  };

  const openPlayer = async (basicPlayer) => {
    setLoadingPlayer(true);

    await new Promise(r => setTimeout(r, 300));

    try {
      const platform_user_id = basicPlayer.platform_user_id ?? basicPlayer.id;

      const hasExistingStats = !!basicPlayer.coreStats;

      const [rankData, statsData] = await Promise.allSettled([
        getPlayerRank(platform_user_id),
        hasExistingStats
          ? Promise.resolve({ data: basicPlayer.coreStats })
          : getPlayerCoreStats(platform_user_id),
      ]);

      const rank  = rankData.status  === "fulfilled" ? rankData.value  : null;
      const stats = statsData.status === "fulfilled" ? statsData.value : null;

      const rawStats = stats?.data ?? (hasExistingStats ? basicPlayer.coreStats : null);

      const enrichedPlayer = {
        ...basicPlayer,
        platform_user_id,
        platform:  basicPlayer.platform ?? "epic",
        rank:      rank?.full_rank ?? basicPlayer.rank ?? "Unranked",
        mmr:       rank?.mmr       ?? basicPlayer.mmr  ?? 0,
        _openedAt: Date.now(),
        coreStats: rawStats ? {
          shots:              rawStats.shots               ?? 0,
          goals:              rawStats.goals               ?? 0,
          saves:              rawStats.saves               ?? 0,
          assists:            rawStats.assists             ?? 0,
          score:              rawStats.score               ?? 0,
          shootingPercentage: rawStats.shooting_percentage ?? rawStats.shootingPercentage ?? 0,
          demoInflicted:      rawStats.demo_inflicted      ?? rawStats.demoInflicted      ?? 0,
          demoTaken:          rawStats.demo_taken          ?? rawStats.demoTaken          ?? 0,
        } : null,
      };

      addToHistory(enrichedPlayer);
      setSelectedPlayer(enrichedPlayer);
      setPage("player");
      setSearchQuery("");
    } catch (error) {
      console.error("Erreur lors du chargement du profil joueur:", error);
      const fallback = {
        ...basicPlayer,
        platform_user_id: basicPlayer.platform_user_id ?? basicPlayer.id,
        _openedAt: Date.now(),
      };
      addToHistory(fallback);
      setSelectedPlayer(fallback);
      setPage("player");
      setSearchQuery("");
    } finally {
      setLoadingPlayer(false);
    }
  };

  return (
    <>
      <div className="bg-grid" />
      <div className="bg-orb bg-orb-1" />
      <div className="bg-orb bg-orb-2" />

      <div className="app">
        <nav>
          <div className="nav-logo" onClick={goHome}>
            <span className="nav-logo-icon">🚀</span>
            RCLStast
          </div>
          <div className="nav-links">
            <div className={`nav-link ${page === "home"   ? "active" : ""}`} onClick={goHome}>Home</div>
            <div className={`nav-link ${page === "global" ? "active" : ""}`} onClick={() => setPage("global")}>Global Stats</div>
          </div>
        </nav>

        <main>
          {page === "home" && (
            <div key={homeKey} className="fade-in">
              <div className="hero">
                <h1 className="hero-title">
                  <span className="line1">TRACK YOUR</span>
                  <span className="line2">ROCKET LEAGUE</span>
                  <span className="line1">STATS</span>
                </h1>
                <p className="hero-sub">
                  Search any player across all platforms — PC, PlayStation, Xbox and Switch
                </p>
                <SearchBar
                  query={searchQuery}
                  setQuery={setSearchQuery}
                  onSearch={handleSearch}
                  suggestions={suggestions}
                  onSuggestionClick={openPlayer}
                  onPlayerClick={openPlayer}
                />

              {/* ── Refresh Latest Games ── */}
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12, margin: "24px 0 0" }}>
                <button
                  onClick={handleRefreshLatest}
                  disabled={refreshing}
                  style={{
                    padding: "10px 28px", borderRadius: 8,
                    border: "1px solid rgba(0,229,255,0.3)",
                    background: refreshing ? "rgba(0,229,255,0.04)" : "rgba(0,229,255,0.08)",
                    color: "var(--cyan)", fontFamily: "'Exo 2', sans-serif",
                    fontWeight: 700, fontSize: "0.85rem", letterSpacing: "0.08em",
                    textTransform: "uppercase", transition: "all .2s",
                    display: "flex", alignItems: "center", gap: 8,
                    opacity: refreshing ? 0.6 : 1, cursor: refreshing ? "not-allowed" : "pointer",
                  }}
                >
                  {refreshing ? "Fetching..." : "↻  Refresh Latest Games"}
                </button>

                {refreshResult && (
                  <div style={{
                    padding: "10px 20px", borderRadius: 8, fontSize: "0.8rem", fontWeight: 600,
                    background: refreshResult.success ? "rgba(0,255,136,0.06)" : "rgba(255,78,80,0.06)",
                    border: `1px solid ${refreshResult.success ? "rgba(0,255,136,0.2)" : "rgba(255,78,80,0.2)"}`,
                    color: refreshResult.success ? "#00ff88" : "#ff6b6b",
                    display: "flex", flexDirection: "column", alignItems: "center", gap: 4,
                    fontFamily: "'Share Tech Mono', monospace", textAlign: "center",
                  }}>
                    {refreshResult.success ? (
                      <>
                        <span>{refreshResult.data.details?.new_matches_downloaded ?? 0} new match(es) downloaded</span>
                        <span style={{ color: "var(--muted)", fontSize: "0.72rem" }}>
                          {refreshResult.data.details?.total_analysed ?? "?"} analysed
                          {" · "}{refreshResult.data.details?.already_in_db ?? "?"} already in DB
                          {refreshResult.data.latest_match_date
                            ? " · Latest: " + new Date(refreshResult.data.latest_match_date).toLocaleDateString()
                            : ""}
                        </span>
                      </>
                    ) : (
                      <span>Error: {refreshResult.message}</span>
                    )}
                  </div>
                )}
              </div>
              </div>

              {history.length > 0 && (
                <>
                  <div className="section-header">
                    <span className="section-title">Recent Searches</span>
                    <div className="section-line" />
                    <button
                      onClick={() => {
                        setHistory([]);
                        try { sessionStorage.removeItem("rl_history"); } catch {}
                      }}
                      style={{
                        background: "none", border: "none", cursor: "pointer",
                        fontSize: "0.72rem", color: "var(--muted)", letterSpacing: "0.06em",
                        textTransform: "uppercase", fontFamily: "'Exo 2', sans-serif",
                        transition: "color 0.2s",
                      }}
                      onMouseEnter={(e) => e.target.style.color = "#ff4e50"}
                      onMouseLeave={(e) => e.target.style.color = "var(--muted)"}
                    >
                      Clear
                    </button>
                  </div>

                  <div className="history-grid">
                    {history.map((p) => {
                      const rankInfo = findRankInfo(p.rank);
                      const platInfo = PLATFORMS.find(pl => pl.id === p.platform);
                      const platLogo = platInfo?.logo ?? null;

                      return (
                        <div
                          key={p.platform_user_id}
                          className="history-card"
                          onClick={() => openPlayer(p)}
                        >
                          <div className="history-card-glow" />

                          <div className="history-avatar">
                            <img
                              src={rankInfo?.image ?? "/images/ranks/unranked.png"}
                              alt={rankInfo?.fullName ?? "Unranked"}
                              style={{ width: "100%", height: "100%", objectFit: "contain", padding: 4 }}
                            />
                          </div>

                          <div className="history-info">
                            <div className="history-name">{p.name}</div>
                            <div className="history-meta">
                              <span className="history-platform">
                                {platLogo
                                  ? <img src={platLogo} alt={platInfo?.label || p.platform} style={{ width: 14, height: 14, objectFit: "contain", verticalAlign: "middle" }} />
                                  : platInfo?.icon
                                }
                                {" "}{platInfo?.label || p.platform}
                              </span>
                              {p.rank && (
                                <span style={{ color: rankInfo?.color || "var(--muted)", fontSize: "0.72rem", fontWeight: 700 }}>
                                  {p.rank}
                                </span>
                              )}
                            </div>
                          </div>

                          {p.mmr > 0 && (
                            <div className="history-mmr">{p.mmr}</div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </>
              )}
            </div>
          )}

          {page === "global" && <GlobalStats />}

          {page === "player" && selectedPlayer && (
            <PlayerPage
              key={selectedPlayer._openedAt}
              player={selectedPlayer}
              onBack={() => setPage("home")}
              onPlayerClick={openPlayer}
            />
          )}
        </main>
      </div>

      <style>{`
        .history-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
          gap: 12px;
          margin-bottom: 48px;
        }
        .history-card {
          display: flex; align-items: center; gap: 14px;
          padding: 14px 16px; background: var(--card);
          border: 1px solid var(--border); border-radius: 12px;
          cursor: pointer; position: relative; overflow: hidden;
          transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
        }
        .history-card:hover {
          border-color: rgba(0,229,255,0.3);
          transform: translateY(-2px);
          box-shadow: 0 6px 24px rgba(0,229,255,0.08);
        }
        .history-card-glow {
          position: absolute; inset: 0; opacity: 0;
          background: radial-gradient(ellipse at left, rgba(0,229,255,0.08), transparent 70%);
          transition: opacity 0.2s; pointer-events: none;
        }
        .history-card:hover .history-card-glow { opacity: 1; }
        .history-avatar {
          width: 44px; height: 44px; border-radius: 8px;
          background: var(--bg3); border: 1px solid var(--border);
          display: flex; align-items: center; justify-content: center;
          flex-shrink: 0; overflow: hidden;
        }
        .history-info { flex: 1; min-width: 0; }
        .history-name {
          font-size: 0.95rem; font-weight: 800;
          white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
          margin-bottom: 4px;
        }
        .history-meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
        .history-platform {
          display: flex; align-items: center; gap: 4px;
          color: var(--muted); font-size: 0.72rem;
        }
        .history-mmr {
          font-family: 'Share Tech Mono', monospace;
          font-size: 0.85rem; color: var(--cyan); font-weight: 700; flex-shrink: 0;
        }
      `}</style>
    </>
  );
}
