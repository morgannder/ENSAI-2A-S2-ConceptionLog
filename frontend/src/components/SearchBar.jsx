import { useRef, useState } from "react";
import { PLATFORMS, RANKS, requestPlayerUpdate } from "../api/apiClient";

const PLATFORM_LOGOS = {
  epic:   "/images/platforms/epic.png",
  steam:  "/images/platforms/steam.png",
  ps4:    "/images/platforms/psn.png",
  xbox:   "/images/platforms/xbox.png",
  switch: "/images/platforms/switch.png",
};

const MODAL_PLATFORMS = [
  { id: "epic",    label: "Epic"        },
  { id: "steam",   label: "Steam"       },
  { id: "ps4",     label: "PlayStation" },
  { id: "xbox",    label: "Xbox"        },
  { id: "psynet",  label: "PsyNet"      },
  { id: "unknown", label: "Unknown"     },
];

// ── Modal "Add your games" ────────────────────────────────────────────────────
function AddGamesModal({ onClose }) {
  const [mode,         setMode]         = useState("pseudo");
  const [platform,     setPlatform]     = useState("epic");
  const [playerId,     setPlayerId]     = useState("");
  const [pseudo,       setPseudo]       = useState("");
  const [gameCount,    setGameCount]    = useState(10);
  const [createdAfter, setCreatedAfter] = useState("2024-01-01");
  const [loading,      setLoading]      = useState(false);
  const [result,       setResult]       = useState(null);

  function switchMode(m) {
    setMode(m);
    setResult(null);
    setPseudo("");
    setPlayerId("");
    setPlatform("epic");
  }

  async function handleSubmit() {
    setResult(null);
    if (mode === "pseudo" && !pseudo.trim()) {
      setResult({ success: false, message: "Please enter a pseudo." });
      return;
    }
    if (mode === "id") {
      if (!playerId.trim()) { setResult({ success: false, message: "Please enter a Player ID." }); return; }
      if (!platform)        { setResult({ success: false, message: "Please select a platform." }); return; }
    }
    setLoading(true);
    try {
      const res = await requestPlayerUpdate({
        playerPlatform:    mode === "id" ? platform : undefined,
        playerId:          mode === "id" ? playerId.trim() : undefined,
        playerExactPseudo: mode === "pseudo" ? pseudo.trim() : undefined,
        gameCount,
        createdAfter: `${createdAfter}T00:00:00Z`,
      });
      const newMatches = res?.details?.new_matches_downloaded ?? res?.new_matches_downloaded ?? 0;
      const total      = res?.details?.total_analysed ?? res?.total_analysed ?? null;
      if (newMatches > 0) {
        setResult({ success: true,  message: `${newMatches} new match(es) added to the database${total != null ? ` (${total} analysed)` : ""}.` });
      } else {
        setResult({ success: false, message: `No new matches found — ${total ?? 0} analysed, already up to date.` });
      }
    } catch (err) {
      setResult({ success: false, message: err.message });
    } finally {
      setLoading(false);
    }
  }

  const tabBtn = (id, label) => (
    <button onClick={() => switchMode(id)} style={{
      flex: 1, padding: "9px 0", borderRadius: 8, cursor: "pointer",
      border: `1px solid ${mode === id ? "var(--cyan)" : "var(--border)"}`,
      background: mode === id ? "rgba(0,229,255,0.1)" : "var(--bg2)",
      color: mode === id ? "var(--cyan)" : "var(--muted)",
      fontFamily: "'Exo 2', sans-serif", fontWeight: 700, fontSize: "0.8rem",
      letterSpacing: "0.06em", textTransform: "uppercase", transition: "all .2s",
    }}>{label}</button>
  );

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box add-games-modal fade-in" onClick={(e) => e.stopPropagation()}>
        <div style={{ marginBottom: "20px", position: "relative" }}>
          <div style={{ textAlign: "center" }}>
            <div className="modal-title" style={{ color: "var(--cyan)", fontSize: "1.2rem" }}>Add your games</div>
            <div style={{ fontSize: "0.78rem", color: "var(--muted)", marginTop: 2 }}>
              Register your account to populate our database
            </div>
          </div>
          <button className="modal-close" onClick={onClose} style={{ position: "absolute", top: 0, right: 0 }}>✕</button>
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          {tabBtn("pseudo", "By Pseudo")}
          {tabBtn("id",     "By Player ID")}
        </div>

        <div className="add-games-form">
          {mode === "pseudo" ? (
            <div className="form-group">
              <label className="form-label">Exact Pseudo <span style={{ color: "#ff4e50", fontSize: "0.65rem" }}>required</span></label>
              <input
                className="form-input" placeholder="e.g. Squishy" autoFocus
                value={pseudo} onChange={(e) => setPseudo(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              />
            </div>
          ) : (<>
            <div className="form-group">
              <label className="form-label">Platform <span style={{ color: "#ff4e50", fontSize: "0.65rem" }}>required</span></label>
              <select className="form-select" value={platform} onChange={(e) => setPlatform(e.target.value)}>
                {MODAL_PLATFORMS.map((p) => <option key={p.id} value={p.id}>{p.label}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Player ID <span style={{ color: "#ff4e50", fontSize: "0.65rem" }}>required</span></label>
              <input
                className="form-input" placeholder="e.g. abc123xyz" autoFocus
                value={playerId} onChange={(e) => setPlayerId(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              />
            </div>
          </>)}

          <div className="form-group">
            <label className="form-label">Games to import <span className="form-hint">(max 200)</span></label>
            <div className="number-stepper">
              <button type="button" className="stepper-btn" onClick={() => setGameCount(v => Math.max(1, v - 1))}>−</button>
              <input
                type="number" min={1} max={200} value={gameCount}
                onChange={(e) => setGameCount(Math.min(200, Math.max(1, Number(e.target.value))))}
              />
              <button type="button" className="stepper-btn" onClick={() => setGameCount(v => Math.min(200, v + 1))}>+</button>
            </div>
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
              {result.success ? "✓" : "✕"} {result.message}
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
        <div className="search-suggestions" style={{ maxHeight: "240px", overflowY: "auto", overflowX: "hidden" }}>
          {suggestions.map((p) => {
            const playerId    = p.platform_user_id || p.id;
            const currentRank = p.rank || "Unranked";
            const rankMatch   = currentRank.match(/^([A-Za-z\s]+\s[IVX]+)/)?.[1] || currentRank;
            const rankInfo    = RANKS.find(r => r.fullName === rankMatch || r.name === rankMatch);
            const platInfo    = PLATFORMS.find(pl => pl.id === p.platform);
            const platLogo    = PLATFORM_LOGOS[p.platform];
            return (
              <div key={playerId || p.name} className="suggestion-item" onClick={() => onSuggestionClick(p)}
                style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                {rankInfo?.image
                  ? <img src={rankInfo.image} alt={currentRank} style={{ width: 22, height: 22, objectFit: "contain" }} />
                  : <span>{rankInfo?.icon || "❓"}</span>
                }
                <span style={{ fontWeight: 700 }}>{p.name}</span>
                <span className="suggestion-platform">
                  {platLogo
                    ? <img src={platLogo} alt={platInfo?.label || p.platform} style={{ width: 12, height: 12, objectFit: "contain", verticalAlign: "middle" }} />
                    : platInfo?.icon
                  }
                  {" "}{platInfo?.label || p.platform || "Unknown"}
                </span>
                <span style={{ marginLeft: "auto", fontSize: "0.75rem", color: "var(--muted)", fontFamily: "monospace" }}>
                  {playerId}
                </span>
                {p.mmr && <span className="suggestion-mmr">{p.mmr} MMR</span>}
              </div>
            );
          })}
        </div>
      )}

      <div style={{ textAlign: "center", marginTop: "12px" }}>
        <span
          onClick={() => setShowModal(true)}
          style={{ fontSize: "0.8rem", color: "var(--muted)", cursor: "pointer", transition: "color 0.2s" }}
          onMouseEnter={(e) => e.target.style.color = "var(--cyan)"}
          onMouseLeave={(e) => e.target.style.color = "var(--muted)"}
        >
          Can't find your account?{" "}
          <span style={{ color: "var(--cyan)", fontWeight: 700, textDecoration: "underline" }}>
            Add your games to our database
          </span>
        </span>
      </div>

      {showModal && <AddGamesModal onClose={() => setShowModal(false)} />}
    </div>
  );
}
