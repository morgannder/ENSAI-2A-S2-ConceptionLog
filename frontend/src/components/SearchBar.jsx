import { useRef, useState } from "react";
import { PLATFORMS, findRankInfo, requestPlayerUpdate, searchPlayers } from "../api/apiClient";

// ── Modal "Add your games" ────────────────────────────────────────────────────
function AddGamesModal({ onClose, onPlayerClick }) {
  const [platform,     setPlatform]     = useState("epic");
  const [playerId,     setPlayerId]     = useState("");
  const [pseudo,       setPseudo]       = useState("");
  const [gameCount,    setGameCount]    = useState(10);
  const [createdAfter, setCreatedAfter] = useState("2024-01-01");
  const [loading,      setLoading]      = useState(false);
  const [result,       setResult]       = useState(null);

  const MODAL_PLATFORMS = [
    { id: "epic",    label: "Epic"        },
    { id: "steam",   label: "Steam"       },
    { id: "psn",     label: "PlayStation" },
    { id: "xbox",    label: "Xbox"        },
    { id: "switch",  label: "Switch"      },
    { id: "psynet",  label: "PsyNet"      },
    { id: "unknown", label: "Unknown"     },
  ];

  async function handleSubmit() {
    if (!playerId.trim() && !pseudo.trim()) {
      setResult({ success: false, message: "Please fill in at least Player ID or Exact Pseudo." });
      return;
    }
    if (playerId.trim() && !platform) {
      setResult({ success: false, message: "Platform is required when using a Player ID." });
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      await requestPlayerUpdate({
        playerPlatform:    playerId.trim() ? platform : undefined,
        playerId:          playerId.trim() || undefined,
        playerExactPseudo: pseudo.trim()   || undefined,
        gameCount,
        createdAfter:      `${createdAfter}T00:00:00Z`,
      });

      const searchTerm = pseudo.trim() || playerId.trim();
      const results = await searchPlayers(searchTerm, null);

      if (results.length === 0) {
        setResult({ success: false, message: "Player added but not found yet, try searching manually in a few seconds." });
        return;
      }

      onClose();
      onPlayerClick(results[0]);
    } catch (err) {
      setResult({ success: false, message: err.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box add-games-modal fade-in" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header" style={{ marginBottom: "20px" }}>
          <div style={{ fontSize: "1.6rem" }}>&#x1F680;</div>
          <div>
            <div className="modal-title" style={{ color: "var(--cyan)", fontSize: "1.2rem" }}>
              Add your games
            </div>
            <div style={{ fontSize: "0.78rem", color: "var(--muted)", marginTop: 2 }}>
              Register your account to populate our database
            </div>
          </div>
          <button className="modal-close" onClick={onClose}>&#x2715;</button>
        </div>

        <div className="add-games-form">
          <div className="form-group">
            <label className="form-label">Platform</label>
            <select className="form-select" value={platform} onChange={(e) => setPlatform(e.target.value)}>
              {MODAL_PLATFORMS.map((p) => (
                <option key={p.id} value={p.id}>{p.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Player ID <span className="form-hint">(optional)</span></label>
            <input className="form-input" placeholder="e.g. abc123xyz" value={playerId} onChange={(e) => setPlayerId(e.target.value)} />
          </div>

          <div className="form-group">
            <label className="form-label">Exact Pseudo <span className="form-hint">(optional)</span></label>
            <input className="form-input" placeholder="e.g. Squishy" value={pseudo} onChange={(e) => setPseudo(e.target.value)} />
          </div>

          <div className="form-group">
            <label className="form-label">Games to import <span className="form-hint">(max 200)</span></label>
            <input
              type="number" className="form-input" min={1} max={200} value={gameCount}
              onChange={(e) => setGameCount(Math.min(200, Math.max(1, Number(e.target.value))))}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Games after</label>
            <input type="date" className="form-input" value={createdAfter} onChange={(e) => setCreatedAfter(e.target.value)} />
          </div>

          {result && (
            <div className="form-result" style={{
              color:      result.success ? "#00ff88" : "#ff4e50",
              background: result.success ? "rgba(0,255,136,0.08)" : "rgba(255,78,80,0.08)",
              border:     `1px solid ${result.success ? "rgba(0,255,136,0.25)" : "rgba(255,78,80,0.25)"}`,
            }}>
              {result.success ? "\u2713" : "\u2715"} {result.message}
            </div>
          )}

          <button className="form-submit" onClick={handleSubmit} disabled={loading}>
            {loading ? <><span className="spinner-sm" /> Sending...</> : "Add to Database"}
          </button>
        </div>
      </div>

      <style>{`
        .add-games-modal { max-width: 420px; width: 92%; padding: 28px; }
        .add-games-form { display: flex; flex-direction: column; gap: 14px; }
        .form-group { display: flex; flex-direction: column; gap: 6px; }
        .form-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); display: flex; align-items: center; gap: 6px; }
        .form-hint { font-size: 0.65rem; color: #333b55; text-transform: none; font-weight: 400; }
        .form-input, .form-select {
          background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
          color: var(--text); padding: 10px 14px;
          font-family: 'Exo 2', sans-serif; font-size: 0.9rem; outline: none;
          transition: border-color 0.2s, box-shadow 0.2s; appearance: none;
        }
        .form-input:focus, .form-select:focus { border-color: rgba(0,229,255,0.5); box-shadow: 0 0 0 3px rgba(0,229,255,0.08); }
        .form-input::placeholder { color: var(--muted); }
        .form-result { padding: 10px 14px; border-radius: 8px; font-size: 0.82rem; font-weight: 600; letter-spacing: 0.03em; }
        .form-submit {
          padding: 12px; border-radius: 8px; border: none; cursor: pointer;
          background: linear-gradient(135deg, var(--cyan), #0099bb);
          color: #000; font-family: 'Exo 2', sans-serif; font-size: 0.9rem; font-weight: 800;
          letter-spacing: 0.08em; text-transform: uppercase; transition: filter 0.2s, opacity 0.2s;
          display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 4px;
        }
        .form-submit:hover:not(:disabled) { filter: brightness(1.15); }
        .form-submit:disabled { opacity: 0.6; cursor: not-allowed; }
        .spinner-sm { width: 16px; height: 16px; border: 2px solid rgba(0,0,0,0.2); border-top-color: #000; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }
      `}</style>
    </div>
  );
}

// ── SearchBar ─────────────────────────────────────────────────────────────────
export default function SearchBar({ query, setQuery, onSearch, suggestions, onSuggestionClick, onPlayerClick }) {
  const inputRef    = useRef();
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="search-container">
      <div className="search-box">
        <input
          ref={inputRef}
          className="search-input"
          placeholder="Enter player name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onSearch()}
        />
        <button className="search-btn" onClick={onSearch}>Search</button>
      </div>

      {suggestions.length > 0 && (
        <div className="search-suggestions">
          {suggestions.slice(0, 5).map((p) => {
            const rankInfo = findRankInfo(p.rank);
            const platInfo = PLATFORMS.find((pl) => pl.id === p.platform);
            return (
              <div
                key={p.platform_user_id || p.name}
                className="suggestion-item"
                onClick={() => onSuggestionClick(p)}
              >
                {/* Rank image — unranked.png as fallback */}
                <img
                  src={rankInfo?.image ?? "/images/ranks/unranked.png"}
                  alt={rankInfo?.fullName ?? "Unranked"}
                  style={{ width: 28, height: 28, objectFit: "contain", flexShrink: 0 }}
                />

                {/* Player name */}
                <span style={{ fontWeight: 700, flex: 1, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {p.name}
                </span>

                {/* Rank label in color */}
                {rankInfo && (
                  <span style={{ fontSize: "0.7rem", fontWeight: 700, color: rankInfo.color, whiteSpace: "nowrap", flexShrink: 0 }}>
                    {rankInfo.fullName}
                  </span>
                )}

                {/* Platform */}
                <span className="suggestion-platform" style={{ display: "flex", alignItems: "center", gap: 4, flexShrink: 0 }}>
                  {platInfo?.logo
                    ? <img src={platInfo.logo} alt={platInfo.label} style={{ width: 12, height: 12, objectFit: "contain", verticalAlign: "middle" }} />
                    : platInfo?.icon
                  }
                  {" "}{platInfo?.label || p.platform || "Unknown"}
                </span>

                {p.mmr && <span className="suggestion-mmr" style={{ flexShrink: 0 }}>{p.mmr} MMR</span>}
              </div>
            );
          })}
        </div>
      )}

      {/* Only the link text is clickable */}
      <div style={{ textAlign: "center", marginTop: "12px" }}>
        <span style={{ fontSize: "0.8rem", color: "var(--muted)", cursor: "default", userSelect: "none" }}>
          Can't find your account?{" "}
        </span>
        <span
          onClick={() => setShowModal(true)}
          style={{ fontSize: "0.8rem", color: "var(--cyan)", fontWeight: 700, textDecoration: "underline", cursor: "pointer", transition: "color 0.2s" }}
          onMouseEnter={(e) => e.target.style.color = "#00ffff"}
          onMouseLeave={(e) => e.target.style.color = "var(--cyan)"}
        >
          Add your games to our database
        </span>
      </div>

      {showModal && (
        <AddGamesModal onClose={() => setShowModal(false)} onPlayerClick={onPlayerClick} />
      )}
    </div>
  );
}