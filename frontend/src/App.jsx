import { useState, useEffect } from "react";
import { searchPlayers, getPlayerRank, getPlayerCoreStats, PLATFORMS, findRankInfo } from "./api/apiClient";
import SearchBar   from "./components/SearchBar";
import PlayerPage  from "./components/PlayerPage";
import GlobalStats from "./components/GlobalStats";

const MAX_HISTORY = 10;

export default function App() {
  const [page,           setPage]           = useState("home");
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [searchQuery,    setSearchQuery]    = useState("");
  const [suggestions,    setSuggestions]    = useState([]);
  const [loading,        setLoading]        = useState(false);
  const [loadingPlayer,  setLoadingPlayer]  = useState(false);
  const [history,        setHistory]        = useState(() => {
    try {
      return JSON.parse(sessionStorage.getItem("rl_history") || "[]");
    } catch {
      return [];
    }
  });

  useEffect(() => {
  if (searchQuery.length >= 3) {
    setLoading(true);
    searchPlayers(searchQuery, null)
      .then((results) => {
        if (!results || results.length === 0) { setSuggestions([]); return; }
        // Affiche immédiatement sans rang, puis enrichit chaque joueur dès que son rang arrive
        setSuggestions(results);
        results.forEach(async (p) => {
          const id = p.platform_user_id ?? p.id;
          if (!id) return;
          const rankData = await getPlayerRank(id).catch(() => null);
          if (!rankData) return;
          setSuggestions((prev) =>
            prev.map((s) =>
              (s.platform_user_id ?? s.id) === id
                ? { ...s, rank: rankData.full_rank ?? s.rank, mmr: rankData.mmr ?? s.mmr }
                : s
            )
          );
        });
      })
      .catch(() => setSuggestions([]))
      .finally(() => setLoading(false));
  } else {
    setSuggestions([]);
  }
}, [searchQuery]);

  const handleSearch = () => {
    if (!searchQuery.trim() || suggestions.length === 0) return;
    openPlayer(suggestions[0]);
  };

  const addToHistory = (player) => {
    setHistory((prev) => {
      const filtered = prev.filter(p => p.platform_user_id !== player.platform_user_id);
      const next = [player, ...filtered].slice(0, MAX_HISTORY);
      try { sessionStorage.setItem("rl_history", JSON.stringify(next)); } catch {}
      return next;
    });
  };

  const openPlayer = async (basicPlayer) => {
    setLoadingPlayer(true);
    try {
      const platform_user_id = basicPlayer.platform_user_id ?? basicPlayer.id;

      const [rankData, statsData] = await Promise.all([
        getPlayerRank(platform_user_id).catch(() => null),
        getPlayerCoreStats(platform_user_id).catch(() => null),
      ]);

      const enrichedPlayer = {
        ...basicPlayer,
        platform_user_id,
        rank:      rankData?.full_rank ?? basicPlayer.rank ?? "Unranked",
        mmr:       rankData?.mmr       ?? basicPlayer.mmr  ?? 0,
        coreStats: statsData?.data ? {
          shots:              statsData.data.shots               ?? 0,
          goals:              statsData.data.goals               ?? 0,
          saves:              statsData.data.saves               ?? 0,
          assists:            statsData.data.assists             ?? 0,
          score:              statsData.data.score               ?? 0,
          shootingPercentage: statsData.data.shooting_percentage ?? 0,
          demoInflicted:      statsData.data.demo_inflicted      ?? 0,
          demoTaken:          statsData.data.demo_taken          ?? 0,
        } : null,
      };

      addToHistory(enrichedPlayer);
      setSelectedPlayer(enrichedPlayer);
      setPage("player");
      setSearchQuery("");
    } catch (error) {
      console.error("Erreur lors du chargement du profil joueur:", error);
      const fallback = { ...basicPlayer, platform_user_id: basicPlayer.platform_user_id ?? basicPlayer.id };
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
          <div className="nav-logo" onClick={() => setPage("home")}>
            <span className="nav-logo-icon">🚀</span>
            RLSTATS
          </div>
          <div className="nav-links">
            <div className={`nav-link ${page === "home"   ? "active" : ""}`} onClick={() => setPage("home")}>Home</div>
            <div className={`nav-link ${page === "global" ? "active" : ""}`} onClick={() => setPage("global")}>Global Stats</div>
          </div>
        </nav>

        <main>
          {page === "home" && (
            <div className="fade-in">
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
                              {/* Platform logo */}
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