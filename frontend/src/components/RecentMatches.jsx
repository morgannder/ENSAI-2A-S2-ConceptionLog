import { useState, useEffect } from "react";
import { RANKS } from "../api/apiClient";

const API_BASE = "/api";

async function getRecentMatches(platformUserId, limit = 20) {
  const response = await fetch(
    `${API_BASE}/participation/player/${platformUserId}/recent?limit=${limit}`
  );
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return response.json();
}

async function getMatchPlayers(matchId) {
  const response = await fetch(`${API_BASE}/match/match-players/?match_id=${matchId}`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return response.json();
}

function formatDuration(startTime, endTime) {
  if (endTime == null) return "—";
  const totalSecs = Math.round(endTime - (startTime ?? 0));
  const m = Math.floor(totalSecs / 60);
  const s = totalSecs % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

const CAR_COLORS = {
  Octane:   "var(--cyan)",
  Fennec:   "var(--orange)",
  Dominus:  "var(--purple)",
  Breakout: "#00ff88",
  Mantis:   "#ffd700",
  Merc:     "#ff4e50",
};

// ── Rank badge inline ─────────────────────────────────────────────────────────
function RankBadge({ rankStr }) {
  if (!rankStr || rankStr === "Unranked") return null;
  const rankInfo = RANKS.find((r) => r.fullName === rankStr || r.name === rankStr);
  if (!rankInfo) return null;
  return rankInfo.image ? (
    <img
      src={rankInfo.image}
      alt={rankStr}
      title={rankStr}
      style={{ width: 18, height: 18, objectFit: "contain", flexShrink: 0 }}
    />
  ) : (
    <span style={{ fontSize: "0.75rem" }} title={rankStr}>{rankInfo.icon}</span>
  );
}

// ── Team column ───────────────────────────────────────────────────────────────
function TeamColumn({ label, players, accentColor, currentPlayerId, onPlayerClick, onClose }) {
  return (
    <div className="team-column">
      <div className="team-label" style={{ color: accentColor }}>{label}</div>
      {players.length === 0 ? (
        <div style={{ fontSize: "0.78rem", color: "var(--muted)", padding: "8px 0" }}>—</div>
      ) : (
        players.map((p) => {
          const isCurrent   = p.platform_user_id === currentPlayerId;
          const isClickable = !isCurrent && !!p.platform_user_id;
          const rankStr     = p.rank ?? p.full_rank ?? null;
          return (
            <div
              key={p.id ?? p.platform_user_id}
              className={`team-player ${isClickable ? "clickable" : ""} ${isCurrent ? "is-current" : ""}`}
              onClick={isClickable ? () => { onPlayerClick(p); onClose(); } : undefined}
              title={isClickable ? `View ${p.name}'s profile` : undefined}
            >
              <RankBadge rankStr={rankStr} />
              <span className="team-player-name" style={{ color: isCurrent ? "var(--cyan)" : "var(--text)" }}>
                {p.name}
              </span>
              {p.score != null && (
                <span style={{
                  fontFamily: "'Share Tech Mono', monospace",
                  fontSize: "0.7rem",
                  color: "#ffd700",
                  marginLeft: "auto",
                  flexShrink: 0,
                }}>
                  {Math.round(p.score)}pts
                </span>
              )}
              {p._mvp === 1 || p._mvp === true ? (
                <span style={{ fontSize: "0.75rem", flexShrink: 0 }} title="MVP">⭐</span>
              ) : null}
              {isCurrent  && <span className="team-player-you">You</span>}
              {isClickable && <span className="team-player-arrow">→</span>}
            </div>
          );
        })
      )}
    </div>
  );
}

// ── Match detail modal ────────────────────────────────────────────────────────
function MatchDetailModal({ match, onClose, onPlayerClick, currentPlayerId }) {
  const [players, setPlayers] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);

  const matchId  = match._match_team_id ?? match._id;
  const isMvp    = match._mvp === 1 || match._mvp === true;
  const duration = formatDuration(match._start_time, match._end_time);
  const carName  = match._car_name ?? "Unknown";
  const carColor = CAR_COLORS[carName] ?? "var(--muted)";
  const score    = match._score ?? match.score ?? null;

  useEffect(() => {
    if (!matchId) return;
    setLoading(true);
    getMatchPlayers(matchId)
      .then((data) => setPlayers(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [matchId]);

  const orangePlayers = players
    ? ["orange1","orange2","orange3","orange4"].map((k) => players[k]).filter(Boolean)
    : [];
  const bluePlayers = players
    ? ["blue1","blue2","blue3","blue4"].map((k) => players[k]).filter(Boolean)
    : [];

  // Compute team scores from players if available
  const orangeScore = orangePlayers.reduce((acc, p) => acc + (p._team_score ?? p.team_score ?? 0), 0) || null;
  const blueScore   = bluePlayers.reduce((acc, p) => acc + (p._team_score ?? p.team_score ?? 0), 0) || null;

  // Try direct match fields for team goals
  const matchOrangeGoals = match._orange_goals ?? match.orange_goals ?? null;
  const matchBlueGoals   = match._blue_goals   ?? match.blue_goals   ?? null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="match-detail-modal fade-in" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} style={{ position: "absolute", top: 16, right: 16 }}>✕</button>

        {/* Header */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 8, marginBottom: 12, paddingRight: 32 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "0.8rem", color: "var(--muted)" }}>
              #{String(matchId ?? "").slice(-6)}
            </span>
            {isMvp && <span className="match-mvp-badge">⭐ MVP</span>}
            <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: "0.8rem", color: "var(--muted)" }}>
              ⏱ {duration}
            </span>
          </div>
          <div style={{ fontSize: "0.9rem", color: carColor, fontWeight: 700 }}>🚗 {carName}</div>
        </div>

        {/* Score + personal stats row */}
        <div style={{
          display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap",
          marginBottom: 14, padding: "10px 14px",
          background: "rgba(255,255,255,0.03)", borderRadius: 10,
          border: "1px solid var(--border)",
        }}>
          {/* Team goals if available */}
          {(matchOrangeGoals != null && matchBlueGoals != null) && (
            <div style={{ display: "flex", alignItems: "center", gap: 8, fontFamily: "'Share Tech Mono', monospace" }}>
              <span style={{ color: "#ff6b1a", fontWeight: 800, fontSize: "1.1rem" }}>{matchOrangeGoals}</span>
              <span style={{ color: "var(--muted)", fontSize: "0.75rem" }}>–</span>
              <span style={{ color: "var(--cyan)", fontWeight: 800, fontSize: "1.1rem" }}>{matchBlueGoals}</span>
            </div>
          )}
          {/* Personal score */}
          {score != null && (
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span style={{ fontSize: "0.65rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>Score</span>
              <span style={{ fontFamily: "'Share Tech Mono', monospace", color: "#ffd700", fontWeight: 800, fontSize: "0.95rem" }}>
                {Math.round(score)}
              </span>
            </div>
          )}
          {/* Goals / Assists / Saves / Shots */}
          {[
            { key: "_goals",   label: "G",  color: "var(--orange)" },
            { key: "_assists", label: "A",  color: "var(--purple)" },
            { key: "_saves",   label: "Sv", color: "#00ff88"       },
            { key: "_shots",   label: "Sh", color: "#ff4e50"       },
          ].map(({ key, label, color }) =>
            match[key] != null ? (
              <div key={key} style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <span style={{ fontSize: "0.65rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>{label}</span>
                <span style={{ fontFamily: "'Share Tech Mono', monospace", color, fontWeight: 700, fontSize: "0.9rem" }}>
                  {match[key]}
                </span>
              </div>
            ) : null
          )}
        </div>

        <div style={{ height: 1, background: "var(--border)", marginBottom: 18 }} />

        {/* Teams */}
        {loading ? (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12, padding: "2rem" }}>
            <div className="spinner" style={{ width: 36, height: 36, borderWidth: 2 }} />
            <span style={{ color: "var(--muted)", fontSize: "0.85rem" }}>Loading players...</span>
          </div>
        ) : error ? (
          <div style={{ padding: "1.5rem", color: "#ff6b6b", textAlign: "center", fontSize: "0.85rem" }}>
            Unable to load match players.
          </div>
        ) : (
          <div className="match-teams-grid">
            <TeamColumn
              label="🟠 Orange"
              players={orangePlayers}
              accentColor="#ff6b1a"
              currentPlayerId={currentPlayerId}
              onPlayerClick={onPlayerClick}
              onClose={onClose}
            />
            <div className="match-vs-divider">
              <div className="match-vs-line" />
              <span className="match-vs-text">VS</span>
              <div className="match-vs-line" />
            </div>
            <TeamColumn
              label="🔵 Blue"
              players={bluePlayers}
              accentColor="var(--cyan)"
              currentPlayerId={currentPlayerId}
              onPlayerClick={onPlayerClick}
              onClose={onClose}
            />
          </div>
        )}
      </div>

      <style>{`
        .match-detail-modal {
          background: var(--bg3);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 28px;
          max-width: 600px;
          width: 92%;
          position: relative;
          box-shadow: 0 0 80px rgba(0,0,0,0.7), 0 0 40px rgba(0,229,255,0.05);
        }

        .match-teams-grid {
          display: grid;
          grid-template-columns: 1fr auto 1fr;
          gap: 16px;
          align-items: start;
        }

        .match-vs-divider {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
          padding-top: 32px;
        }

        .match-vs-line {
          width: 1px;
          height: 40px;
          background: var(--border);
        }

        .match-vs-text {
          font-size: 0.65rem;
          font-weight: 900;
          color: var(--muted);
          letter-spacing: 0.15em;
          writing-mode: horizontal-tb;
        }

        .team-column {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .team-label {
          font-size: 0.7rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          margin-bottom: 4px;
        }

        .team-player {
          display: flex;
          align-items: center;
          gap: 7px;
          padding: 10px 12px;
          background: var(--card);
          border: 1px solid var(--border);
          border-radius: 8px;
          transition: border-color 0.2s, background 0.2s, transform 0.15s;
          min-width: 0;
        }

        .team-player.clickable {
          cursor: pointer;
        }

        .team-player.clickable:hover {
          background: var(--bg2);
          border-color: rgba(0,229,255,0.3);
          transform: translateX(3px);
        }

        .team-player.is-current {
          border-color: rgba(0,229,255,0.35);
          background: rgba(0,229,255,0.05);
        }

        .team-player-name {
          font-size: 0.85rem;
          font-weight: 700;
          flex: 1;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .team-player-you {
          font-size: 0.6rem;
          color: var(--cyan);
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          border: 1px solid rgba(0,229,255,0.3);
          border-radius: 4px;
          padding: 1px 6px;
          flex-shrink: 0;
        }

        .team-player-arrow {
          font-size: 0.75rem;
          color: var(--muted);
          flex-shrink: 0;
          transition: color 0.2s, transform 0.2s;
        }

        .team-player.clickable:hover .team-player-arrow {
          color: var(--cyan);
          transform: translateX(2px);
        }
      `}</style>
    </div>
  );
}

// ── Match card ────────────────────────────────────────────────────────────────
function MatchCard({ match, index, onClick }) {
  const isMvp    = match._mvp === 1 || match._mvp === true;
  const duration = formatDuration(match._start_time, match._end_time);
  const carName  = match._car_name ?? "Unknown";
  const carColor = CAR_COLORS[carName] ?? "var(--muted)";
  const matchId  = String(match._id ?? match._match_team_id ?? index).slice(-6);
  const score    = match._score ?? match.score ?? null;

  return (
    <div
      className="match-card"
      style={{ "--delay": `${index * 60}ms`, cursor: "pointer" }}
      onClick={() => onClick(match)}
    >
      <div className="match-timeline-line">
        <div className="match-dot" style={{
          background: isMvp ? "#ffd700" : "var(--border)",
          boxShadow:  isMvp ? "0 0 12px #ffd700" : "none",
        }} />
      </div>
      <div className="match-content">
        <div className="match-header">
          <span className="match-id">#{matchId}</span>
          {isMvp && <span className="match-mvp-badge">⭐ MVP</span>}
          <span className="match-duration">⏱ {duration}</span>
          {score != null && (
            <span style={{
              fontFamily: "'Share Tech Mono', monospace",
              fontSize: "0.72rem",
              color: "#ffd700",
              fontWeight: 700,
            }}>
              {Math.round(score)}pts
            </span>
          )}
          <span style={{ marginLeft: "auto", fontSize: "0.7rem", color: "var(--muted)", paddingLeft: 8, flexShrink: 0 }}>
            Details →
          </span>
        </div>
        <div className="match-car" style={{ color: carColor }}>
          <span className="match-car-icon">🚗</span>
          <span className="match-car-name">{carName}</span>
        </div>
        <div className="match-bar" style={{
          background:  `linear-gradient(90deg, ${carColor}33, transparent)`,
          borderColor: `${carColor}44`,
        }} />
      </div>
    </div>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────
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
      .then((data) => {
        if (cancelled) return;
        const list =
          Array.isArray(data)          ? data         :
          Array.isArray(data?.data)    ? data.data    :
          Array.isArray(data?.results) ? data.results :
          Array.isArray(data?.matches) ? data.matches :
          [];
        setMatches(list);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err.message);
      })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [platformUserId]);

  const mvpCount = matches.filter((m) => m._mvp === 1 || m._mvp === true).length;
  const avgDur   = matches.length > 0
    ? Math.round(matches.reduce((acc, m) => acc + ((m._end_time ?? 0) - (m._start_time ?? 0)), 0) / matches.length)
    : null;

  return (
    <div className="recent-matches-section">
      <style>{`
        .recent-matches-section { margin-top: 2rem; }

        .matches-summary { display: flex; gap: 12px; margin-bottom: 28px; flex-wrap: wrap; }
        .summary-chip {
          padding: 8px 16px; border-radius: 20px;
          background: var(--card); border: 1px solid var(--border);
          font-size: 0.8rem; font-weight: 700; letter-spacing: 0.06em;
          display: flex; align-items: center; gap: 6px;
        }
        .summary-chip .chip-val { color: var(--cyan); font-family: 'Share Tech Mono', monospace; }
        .summary-chip.mvp-chip .chip-val { color: #ffd700; }

        .matches-feed { position: relative; padding-left: 24px; }
        .matches-feed::before {
          content: ''; position: absolute; left: 7px; top: 12px; bottom: 12px;
          width: 2px;
          background: linear-gradient(to bottom, var(--cyan), var(--border) 80%, transparent);
        }

        .match-card {
          display: flex; gap: 0; margin-bottom: 12px;
          animation: matchSlideIn 0.4s ease both;
          animation-delay: var(--delay, 0ms);
        }
        @keyframes matchSlideIn {
          from { opacity: 0; transform: translateX(-12px); }
          to   { opacity: 1; transform: translateX(0); }
        }

        .match-timeline-line {
          display: flex; flex-direction: column; align-items: center;
          margin-right: 16px; position: relative; top: 14px; flex-shrink: 0;
        }
        .match-dot {
          width: 14px; height: 14px; border-radius: 50%;
          border: 2px solid var(--bg); flex-shrink: 0;
          transition: transform 0.2s; margin-left: -21px;
        }
        .match-card:hover .match-dot { transform: scale(1.4); }

        .match-content {
          flex: 1; background: var(--card); border-radius: 12px;
          padding: 14px 18px; border: 1px solid var(--border);
          transition: border-color 0.2s, box-shadow 0.2s;
          position: relative; overflow: hidden;
        }
        .match-card:hover .match-content {
          border-color: rgba(0,229,255,0.25);
          box-shadow: 0 4px 20px rgba(0,229,255,0.08);
        }

        .match-header {
          display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap;
        }
        .match-id { font-family: 'Share Tech Mono', monospace; font-size: 0.75rem; color: var(--muted); }
        .match-mvp-badge {
          padding: 2px 10px; border-radius: 10px;
          background: rgba(255,215,0,0.12); border: 1px solid rgba(255,215,0,0.35);
          color: #ffd700; font-size: 0.7rem; font-weight: 800; letter-spacing: 0.08em;
        }
        .match-duration { font-family: 'Share Tech Mono', monospace; font-size: 0.78rem; color: var(--muted); }

        .match-car { display: flex; align-items: center; gap: 8px; font-size: 0.92rem; font-weight: 700; }
        .match-car-icon { font-size: 1rem; }
        .match-car-name { letter-spacing: 0.03em; }

        .match-bar { position: absolute; bottom: 0; left: 0; right: 0; height: 2px; border-top: 1px solid; }

        .matches-empty {
          text-align: center; padding: 3rem; color: var(--muted);
          background: var(--card); border-radius: 12px; border: 1px solid var(--border);
        }
        .matches-error {
          padding: 16px 20px; border-radius: 12px; color: #ff6b6b;
          background: rgba(255,78,80,0.08); border: 1px solid rgba(255,78,80,0.25);
        }
        .matches-loading {
          display: flex; flex-direction: column; align-items: center;
          gap: 14px; padding: 3rem; color: var(--muted);
        }
      `}</style>

      <div className="section-header">
        <span className="section-title">Recent Matches</span>
        <div className="section-line" />
        {!loading && matches.length > 0 && (
          <span className="section-badge">{matches.length} games</span>
        )}
      </div>

      {!loading && matches.length > 0 && (
        <div className="matches-summary">
          <div className="summary-chip">
            Matches <span className="chip-val">{matches.length}</span>
          </div>
          <div className="summary-chip mvp-chip">
            MVP <span className="chip-val">{mvpCount}</span>
          </div>
          <div className="summary-chip">
            MVP Rate <span className="chip-val">{((mvpCount / matches.length) * 100).toFixed(0)}%</span>
          </div>
          {avgDur != null && (
            <div className="summary-chip">
              Avg Duration <span className="chip-val">{Math.floor(avgDur / 60)}:{String(avgDur % 60).padStart(2, "0")}</span>
            </div>
          )}
        </div>
      )}

      {loading ? (
        <div className="matches-loading">
          <div className="spinner" />
          <span>Loading matches...</span>
        </div>
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
            <MatchCard
              key={match._id ?? i}
              match={match}
              index={i}
              onClick={setSelectedMatch}
            />
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