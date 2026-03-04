import { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import { RANKS } from "../api/apiClient";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

// ── API helpers ───────────────────────────────────────────────────────────────

async function getRecentMatches(platformUserId, limit = 20) {
  const res = await fetch(`${API_BASE}/participation/player/${platformUserId}/recent?limit=${limit}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function getMatchPlayers(matchTeamId) {
  const res = await fetch(`${API_BASE}/match/match-players/?match_id=${matchTeamId}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Step 1: _match_team_id hash → { id (= match_id), playlist_id, ... }
async function getMatchByMatchTeamId(matchTeamId) {
  const res = await fetch(`${API_BASE}/match/by-match-team/${matchTeamId}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Step 2: match_id → [{ id, match_id, color, score, ... }, ...]  (2 entries)
async function getMatchTeamsByMatchId(matchId) {
  const res = await fetch(`${API_BASE}/match_team/match/${matchId}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Chain: _match_team_id → match_id → both team scores
async function fetchMatchScore(matchTeamId) {
  try {
    const matchInfo = await getMatchByMatchTeamId(matchTeamId);
    const matchId   = matchInfo?.id ?? matchInfo?.match_id;
    if (!matchId) return null;

    const teams = await getMatchTeamsByMatchId(matchId);
    const list  = Array.isArray(teams) ? teams : (teams?.data ?? teams?.results ?? []);

    let orangeScore = null, blueScore = null;
    for (const t of list) {
      if (t.color === "orange") orangeScore = t.score;
      else if (t.color === "blue") blueScore = t.score;
    }
    return { orangeScore, blueScore };
  } catch {
    return null;
  }
}

// ── Utils ─────────────────────────────────────────────────────────────────────
function formatDuration(startTime, endTime) {
  if (endTime == null) return "—";
  const s = Math.round(endTime - (startTime ?? 0));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

const CAR_COLORS = {
  Octane: "var(--cyan)", Fennec: "var(--orange)", Dominus: "var(--purple)",
  Breakout: "#00ff88",  Mantis: "#ffd700",        Merc: "#ff4e50",
};

// ── RankBadge ─────────────────────────────────────────────────────────────────
function RankBadge({ rankStr }) {
  if (!rankStr || rankStr === "Unranked") return null;
  const extracted = rankStr.match(/^([A-Za-z\s]+\s[IVX]+)/)?.[1]?.trim() || rankStr.trim();
  const info = RANKS.find(r => r.fullName === extracted || r.fullName === rankStr.trim() || r.name === rankStr.trim());
  if (!info) return null;
  return info.image
    ? <img src={info.image} alt={rankStr} title={rankStr} style={{ width: 18, height: 18, objectFit: "contain", flexShrink: 0 }} />
    : <span style={{ fontSize: "0.75rem" }} title={rankStr}>{info.icon}</span>;
}

// ── TeamColumn ────────────────────────────────────────────────────────────────
function TeamColumn({ label, players, accentColor, currentPlayerId, onPlayerClick, onClose }) {
  return (
    <div className="team-column">
      <div className="team-label" style={{ color: accentColor }}>{label}</div>
      {players.length === 0 ? (
        <div style={{ fontSize: "0.78rem", color: "var(--muted)", padding: "8px 0" }}>—</div>
      ) : players.map(p => {
        const isCurrent   = p.platform_user_id === currentPlayerId;
        const isClickable = !isCurrent && !!p.platform_user_id;
        const isMvp       = p._mvp === 1 || p._mvp === true;
        return (
          <div
            key={p.id ?? p.platform_user_id}
            className={`team-player ${isClickable ? "clickable" : ""} ${isCurrent ? "is-current" : ""}`}
            onClick={isClickable ? () => { onPlayerClick(p); onClose(); } : undefined}
            title={isClickable ? `View ${p.name}'s profile` : undefined}
          >
            <RankBadge rankStr={p.rank ?? p.full_rank ?? null} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <span className="team-player-name" style={{ color: isMvp ? "#ffd700" : isCurrent ? "var(--cyan)" : "var(--text)", display: "block" }}>
                {p.name}
              </span>
              {isMvp && <span style={{ fontSize: "0.58rem", fontWeight: 800, color: "#ffd700", letterSpacing: "0.1em", textTransform: "uppercase", opacity: 0.85 }}>mvp</span>}
            </div>
            {p.score != null && (
              <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "0.7rem", color: "#ffd700", marginLeft: "auto", flexShrink: 0 }}>
                {Math.round(p.score)}pts
              </span>
            )}
            {isCurrent   && <span className="team-player-you">You</span>}
            {isClickable && <span className="team-player-arrow">→</span>}
          </div>
        );
      })}
    </div>
  );
}

// ── MatchDetailModal ──────────────────────────────────────────────────────────
function MatchDetailModal({ match, onClose, onPlayerClick, currentPlayerId }) {
  const [players,  setPlayers]  = useState(null);
  const [loadingPl,setLoadingPl]= useState(true);
  const [score,    setScore]    = useState(null);
  const [errorPl,  setErrorPl]  = useState(null);

  const matchTeamId   = match._match_team_id;
  const duration      = formatDuration(match._start_time, match._end_time);
  const carName       = match._car_name ?? "Unknown";
  const carColor      = CAR_COLORS[carName] ?? "var(--muted)";
  const personalScore = match._score ?? match.score ?? null;

  useEffect(() => {
    if (!matchTeamId) return;
    setLoadingPl(true);
    setScore(null);
    setErrorPl(null);

    Promise.all([
      getMatchPlayers(matchTeamId),
      fetchMatchScore(matchTeamId),
    ])
      .then(([playersData, scoreData]) => {
        setPlayers(playersData);
        setScore(scoreData);
      })
      .catch(err => setErrorPl(err.message))
      .finally(() => setLoadingPl(false));
  }, [matchTeamId]);

  const orangePlayers = players ? ["orange1","orange2","orange3","orange4"].map(k => players[k]).filter(Boolean) : [];
  const bluePlayers   = players ? ["blue1","blue2","blue3","blue4"].map(k => players[k]).filter(Boolean) : [];

  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="match-detail-modal fade-in" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} style={{ position: "absolute", top: 16, right: 16 }}>✕</button>

        {/* ── Score hero ── */}
        <div style={{ textAlign: "center", marginBottom: 24, paddingRight: 32 }}>
          {/* meta row */}
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 10, marginBottom: 16, flexWrap: "wrap" }}>
            <div style={{
              display: "flex", alignItems: "center", gap: 5,
              background: "rgba(255,255,255,0.04)", border: "1px solid var(--border)",
              borderRadius: 6, padding: "3px 10px",
            }}>
              <span style={{ fontSize: "0.6rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.1em" }}>Match</span>
              <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "0.72rem", color: "rgba(255,255,255,0.5)" }}>#{String(matchTeamId ?? "").slice(-6)}</span>
            </div>
            <div style={{
              display: "flex", alignItems: "center", gap: 5,
              background: "rgba(255,255,255,0.04)", border: "1px solid var(--border)",
              borderRadius: 6, padding: "3px 10px",
            }}>
              <span style={{ fontSize: "0.6rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.1em" }}>Duration</span>
              <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "0.72rem", color: "rgba(255,255,255,0.5)" }}>{duration}</span>
            </div>
          </div>

          {/* big score */}
          {score?.orangeScore != null && score?.blueScore != null ? (
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 20, marginBottom: 14 }}>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "0.65rem", fontWeight: 700, color: "#ff6b1a", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: 4, opacity: 0.8 }}>Orange</div>
                <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "3.2rem", fontWeight: 900, color: "#ff6b1a", lineHeight: 1, textShadow: "0 0 30px rgba(255,107,26,0.5)" }}>
                  {score.orangeScore}
                </span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4, paddingTop: 18 }}>
                <div style={{ width: 1, height: 20, background: "var(--border)" }} />
                <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "0.7rem", color: "var(--muted)", letterSpacing: "0.1em" }}>VS</span>
                <div style={{ width: 1, height: 20, background: "var(--border)" }} />
              </div>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "0.65rem", fontWeight: 700, color: "var(--cyan)", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: 4, opacity: 0.8 }}>Blue</div>
                <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "3.2rem", fontWeight: 900, color: "var(--cyan)", lineHeight: 1, textShadow: "0 0 30px rgba(0,229,255,0.5)" }}>
                  {score.blueScore}
                </span>
              </div>
            </div>
          ) : loadingPl ? (
            <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "0.78rem", color: "var(--muted)", marginBottom: 14 }}>Loading score…</div>
          ) : null}

          {/* MVP badge */}
          {(() => {
            const allP = players ? Object.values(players).filter(Boolean) : [];
            const mvp  = allP.find(p => p._mvp === 1 || p._mvp === true);
            return mvp ? (
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 7, marginBottom: 14 }}>
                <span style={{ fontSize: "1rem" }}>🏆</span>
                <span style={{ fontSize: "0.7rem", fontWeight: 800, color: "#ffd700", letterSpacing: "0.12em", textTransform: "uppercase" }}>MVP</span>
                <span style={{
                  fontFamily: "'Exo 2', sans-serif", fontSize: "0.85rem", fontWeight: 800, color: "#ffd700",
                  background: "rgba(255,215,0,0.1)", border: "1px solid rgba(255,215,0,0.3)",
                  borderRadius: 6, padding: "2px 10px",
                }}>{mvp.name}</span>
              </div>
            ) : null;
          })()}

          {/* personal stats row */}
          <div style={{ display: "flex", justifyContent: "center", gap: 20, flexWrap: "wrap" }}>
            {personalScore != null && (
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "0.6rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 2 }}>Score</div>
                <span style={{ fontFamily: "'Share Tech Mono', monospace", color: "#ffd700", fontWeight: 800, fontSize: "1.1rem" }}>{Math.round(personalScore)}</span>
              </div>
            )}
            {[
              { key: "_goals",   label: "Goals",   color: "var(--orange)" },
              { key: "_assists", label: "Assists",  color: "var(--purple)" },
              { key: "_saves",   label: "Saves",    color: "#00ff88"       },
              { key: "_shots",   label: "Shots",    color: "#ff4e50"       },
            ].map(({ key, label, color }) =>
              match[key] != null ? (
                <div key={key} style={{ textAlign: "center" }}>
                  <div style={{ fontSize: "0.6rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 2 }}>{label}</div>
                  <span style={{ fontFamily: "'Share Tech Mono', monospace", color, fontWeight: 800, fontSize: "1.1rem" }}>{match[key]}</span>
                </div>
              ) : null
            )}
          </div>
        </div>

        <div style={{ height: 1, background: "var(--border)", marginBottom: 18 }} />

        {loadingPl ? (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12, padding: "2rem" }}>
            <div className="spinner" style={{ width: 36, height: 36, borderWidth: 2 }} />
            <span style={{ color: "var(--muted)", fontSize: "0.85rem" }}>Loading players…</span>
          </div>
        ) : errorPl ? (
          <div style={{ padding: "1.5rem", color: "#ff6b6b", textAlign: "center", fontSize: "0.85rem" }}>
            Unable to load match players.
          </div>
        ) : (
          <div className="match-teams-grid">
            <TeamColumn label="🟠 Orange" players={orangePlayers} accentColor="#ff6b1a" currentPlayerId={currentPlayerId} onPlayerClick={onPlayerClick} onClose={onClose} />
            <div className="match-vs-divider">
              <div className="match-vs-line" />
              <span className="match-vs-text">VS</span>
              <div className="match-vs-line" />
            </div>
            <TeamColumn label="🔵 Blue" players={bluePlayers} accentColor="var(--cyan)" currentPlayerId={currentPlayerId} onPlayerClick={onPlayerClick} onClose={onClose} />
          </div>
        )}
      </div>

      <style>{`
        .match-detail-modal {
          background: var(--bg3); border: 1px solid var(--border); border-radius: 16px;
          padding: 28px; max-width: 600px; width: 92%; position: relative;
          box-shadow: 0 0 80px rgba(0,0,0,0.7), 0 0 40px rgba(0,229,255,0.05);
        }
        .match-teams-grid { display: grid; grid-template-columns: 1fr auto 1fr; gap: 16px; align-items: start; }
        .match-vs-divider { display: flex; flex-direction: column; align-items: center; gap: 8px; padding-top: 32px; }
        .match-vs-line { width: 1px; height: 40px; background: var(--border); }
        .match-vs-text { font-size: 0.65rem; font-weight: 900; color: var(--muted); letter-spacing: 0.15em; }
        .team-column { display: flex; flex-direction: column; gap: 8px; }
        .team-label { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; }
        .team-player {
          display: flex; align-items: center; gap: 7px; padding: 10px 12px;
          background: var(--card); border: 1px solid var(--border); border-radius: 8px;
          transition: border-color 0.2s, background 0.2s, transform 0.15s; min-width: 0;
        }
        .team-player.clickable { cursor: pointer; }
        .team-player.clickable:hover { background: var(--bg2); border-color: rgba(0,229,255,0.3); transform: translateX(3px); }
        .team-player.is-current { border-color: rgba(0,229,255,0.35); background: rgba(0,229,255,0.05); }
        .team-player-name { font-size: 0.85rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .team-player-you { font-size: 0.6rem; color: var(--cyan); font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; border: 1px solid rgba(0,229,255,0.3); border-radius: 4px; padding: 1px 6px; flex-shrink: 0; }
        .team-player-arrow { font-size: 0.75rem; color: var(--muted); flex-shrink: 0; transition: color 0.2s, transform 0.2s; }
        .team-player.clickable:hover .team-player-arrow { color: var(--cyan); transform: translateX(2px); }
      `}</style>
    </div>
  , document.body);
}

// ── MatchCard ─────────────────────────────────────────────────────────────────
function MatchCard({ match, index, onClick }) {
  const isMvp         = match._mvp === 1 || match._mvp === true;
  const duration      = formatDuration(match._start_time, match._end_time);
  const carName       = match._car_name ?? "Unknown";
  const carColor      = CAR_COLORS[carName] ?? "var(--muted)";
  const displayId     = String(match._match_team_id ?? index).slice(-6);
  const personalScore = match._score ?? match.score ?? null;

  return (
    <div className="match-card" style={{ "--delay": `${index * 60}ms`, "--car-color": carColor, cursor: "pointer" }} onClick={() => onClick(match)}>
      {/* left accent bar */}
      <div className="match-accent-bar" />

      <div className="match-content">
        {/* top row: id + duration + MVP badge */}
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10, flexWrap: "wrap" }}>
          <span className="match-id">#{displayId}</span>
          <span style={{ width: 3, height: 3, borderRadius: "50%", background: "var(--muted)", opacity: 0.4, flexShrink: 0 }} />
          <span className="match-duration">{duration}</span>
          {isMvp && (
            <span style={{
              marginLeft: 4, fontSize: "0.6rem", fontWeight: 800, color: "#ffd700",
              background: "rgba(255,215,0,0.1)", border: "1px solid rgba(255,215,0,0.3)",
              borderRadius: 4, padding: "1px 7px", letterSpacing: "0.1em", textTransform: "uppercase",
            }}>🏆 MVP</span>
          )}
          <span style={{ marginLeft: "auto", fontSize: "0.68rem", color: "var(--muted)", display: "flex", alignItems: "center", gap: 4, flexShrink: 0 }}>
            Details <span style={{ fontSize: "0.8rem" }}>→</span>
          </span>
        </div>

        {/* bottom row: car + personal score */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ fontSize: "1rem" }}>🚗</span>
            <span style={{ fontWeight: 700, fontSize: "0.88rem", color: carColor, letterSpacing: "0.02em" }}>{carName}</span>
          </div>
          {personalScore != null && (
            <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "1rem", color: "#ffd700", fontWeight: 800 }}>
              {Math.round(personalScore)}<span style={{ fontSize: "0.65rem", color: "var(--muted)", marginLeft: 2 }}>pts</span>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────────
export default function RecentMatches({ player, onPlayerClick }) {
  const [matches,       setMatches]       = useState([]);
  const [loading,       setLoading]       = useState(true);
  const [error,         setError]         = useState(null);
  const [selectedMatch, setSelectedMatch] = useState(null);

  const platformUserId = player.platform_user_id ?? player.id;

  useEffect(() => {
    if (!platformUserId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    setMatches([]);

    getRecentMatches(platformUserId, 20)
      .then(data => {
        if (cancelled) return;
        const list =
          Array.isArray(data)          ? data         :
          Array.isArray(data?.data)    ? data.data    :
          Array.isArray(data?.results) ? data.results :
          Array.isArray(data?.matches) ? data.matches :
          [];
        setMatches(list);
      })
      .catch(err => { if (!cancelled) setError(err.message); })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [platformUserId]);

  const mvpCount = matches.filter(m => m._mvp === 1 || m._mvp === true).length;
  const avgDur   = matches.length > 0
    ? Math.round(matches.reduce((acc, m) => acc + ((m._end_time ?? 0) - (m._start_time ?? 0)), 0) / matches.length)
    : null;

  return (
    <div className="recent-matches-section">
      <style>{`
        .recent-matches-section { margin-top: 2rem; }
        .matches-summary { display: flex; gap: 12px; margin-bottom: 28px; flex-wrap: wrap; }
        .summary-chip { padding: 8px 16px; border-radius: 20px; background: var(--card); border: 1px solid var(--border); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.06em; display: flex; align-items: center; gap: 6px; }
        .summary-chip .chip-val { color: var(--cyan); font-family: 'Share Tech Mono', monospace; }
        .summary-chip.mvp-chip .chip-val { color: #ffd700; }
        .matches-feed { display: flex; flex-direction: column; gap: 8px; }
        .match-card {
          display: flex; align-items: stretch; gap: 0;
          animation: matchSlideIn 0.35s ease both; animation-delay: var(--delay, 0ms);
          border-radius: 12px; overflow: hidden;
          border: 1px solid var(--border);
          transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
        }
        .match-card:hover {
          border-color: rgba(0,229,255,0.2);
          box-shadow: 0 4px 24px rgba(0,229,255,0.07);
          transform: translateX(3px);
        }
        @keyframes matchSlideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
        .match-accent-bar {
          width: 3px; flex-shrink: 0;
          background: var(--car-color, var(--cyan));
          box-shadow: 0 0 8px var(--car-color, var(--cyan));
          opacity: 0.7;
          transition: opacity 0.2s;
        }
        .match-card:hover .match-accent-bar { opacity: 1; }
        .match-content { flex: 1; background: var(--card); padding: 14px 18px; }
        .match-id { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: var(--muted); }
        .match-duration { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: var(--muted); }
        .matches-empty { text-align: center; padding: 3rem; color: var(--muted); background: var(--card); border-radius: 12px; border: 1px solid var(--border); }
        .matches-error { padding: 16px 20px; border-radius: 12px; color: #ff6b6b; background: rgba(255,78,80,0.08); border: 1px solid rgba(255,78,80,0.25); }
        .matches-loading { display: flex; flex-direction: column; align-items: center; gap: 14px; padding: 3rem; color: var(--muted); }
      `}</style>

      <div className="section-header">
        <span className="section-title">Recent Matches</span>
        <div className="section-line" />
        {!loading && matches.length > 0 && <span className="section-badge">{matches.length} games</span>}
      </div>

      {!loading && matches.length > 0 && (
        <div className="matches-summary">
          <div className="summary-chip">Matches <span className="chip-val">{matches.length}</span></div>
          <div className="summary-chip mvp-chip">MVP <span className="chip-val">{mvpCount}</span></div>
          <div className="summary-chip">MVP Rate <span className="chip-val">{((mvpCount / matches.length) * 100).toFixed(0)}%</span></div>
          {avgDur != null && (
            <div className="summary-chip">Avg Duration <span className="chip-val">{Math.floor(avgDur / 60)}:{String(avgDur % 60).padStart(2, "0")}</span></div>
          )}
        </div>
      )}

      {loading ? (
        <div className="matches-loading"><div className="spinner" /><span>Loading matches…</span></div>
      ) : error && matches.length === 0 ? (
        <div className="matches-error">
          <div style={{ fontWeight: 700, marginBottom: 4 }}>Failed to load matches</div>
          <div style={{ fontSize: "0.8rem", fontFamily: "'Share Tech Mono', monospace" }}>{error}</div>
        </div>
      ) : matches.length === 0 ? (
        <div className="matches-empty">No recent matches found.</div>
      ) : (
        <div className="matches-feed">
          {matches.map((match, i) => (
            <MatchCard key={match._match_team_id ?? i} match={match} index={i} onClick={setSelectedMatch} />
          ))}
        </div>
      )}

      {selectedMatch && (
        <MatchDetailModal
          match={selectedMatch}
          onClose={() => setSelectedMatch(null)}
          onPlayerClick={onPlayerClick}
          currentPlayerId={platformUserId}
        />
      )}
    </div>
  );
}
