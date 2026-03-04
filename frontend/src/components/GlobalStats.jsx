import { useState, useEffect } from "react";
import { RANKS, getRankStats } from "../api/apiClient";

// ── API rank keys (what the endpoint expects) ─────────────────────────────────
// The endpoint takes e.g. "Bronze", "Silver"... not "Bronze I"
// We deduplicate RANKS to get one entry per main rank group
const RANK_GROUPS = (() => {
  const seen = new Set();
  return RANKS.filter(r => {
    const base = r.name.replace(/ (I|II|III)$/, "").trim();
    if (seen.has(base) || base === "Unranked") return false;
    seen.add(base);
    return true;
  }).map(r => ({
    key:   r.name.replace(/ (I|II|III)$/, "").trim(),
    label: r.name.replace(/ (I|II|III)$/, "").trim(),
    color: r.color,
    glow:  r.glow,
    icon:  r.icon,
    short: r.name.replace(/ (I|II|III)$/, "").replace("Grand Champion", "GC").replace("Supersonic Legend", "SSL").replace("Champion", "Champ").replace("Platinum", "Plat").replace("Diamond", "Diam").trim(),
  }));
})();

// ── Constants ─────────────────────────────────────────────────────────────────
const GAME_MODES = [
  { label: "1v1 Ranked", value: "ranked-duels"    },
  { label: "2v2 Ranked", value: "ranked-doubles"  },
  { label: "3v3 Ranked", value: "ranked-standard" },
];

const STAT_TABS = [
  { key: "core",        label: "Core",        icon: "⚽", route: "statscore/average"        },
  { key: "boost",       label: "Boost",       icon: "🚀", route: "statsboost/rank"           },
  { key: "positioning", label: "Positioning", icon: "📍", route: "statspositioning/rank"     },
  { key: "movement",    label: "Movement",    icon: "💨", route: "statsmovement/rank"        },
];

// Exact keys from API responses
const STAT_FIELDS = {
  core: [
    { key: "shots",               label: "Shots / Game"        },
    { key: "goals",               label: "Goals / Game"        },
    { key: "saves",               label: "Saves / Game"        },
    { key: "assists",             label: "Assists / Game"      },
    { key: "score",               label: "Score / Game"        },
    { key: "shooting_percentage", label: "Shooting %"          },
    { key: "demo_inflicted",      label: "Demos Inflicted"     },
    { key: "demo_taken",          label: "Demos Taken"         },
  ],
  boost: [
    { key: "average_amount",               label: "Avg Boost Amount"    },
    { key: "boost_per_minute",             label: "Boost / Min"         },
    { key: "amount_collected",             label: "Boost Collected"     },
    { key: "amount_stolen",                label: "Boost Stolen"        },
    { key: "amount_used_while_supersonic", label: "Used Supersonic"     },
    { key: "percent_zero_boost",           label: "Time @ 0 Boost %"   },
    { key: "percent_full_boost",           label: "Time @ Full Boost %" },
    { key: "amount_overfill",              label: "Boost Overfill"      },
    { key: "percent_boost_0_25",           label: "Boost 0–25 %"        },
    { key: "percent_boost_25_50",          label: "Boost 25–50 %"       },
    { key: "percent_boost_50_75",          label: "Boost 50–75 %"       },
    { key: "percent_boost_75_100",         label: "Boost 75–100 %"      },
  ],
  positioning: [
    { key: "percent_defensive_half",        label: "Defensive Half %"      },
    { key: "percent_offensive_half",        label: "Offensive Half %"      },
    { key: "percent_defensive_third",       label: "Defensive Third %"     },
    { key: "percent_offensive_third",       label: "Offensive Third %"     },
    { key: "percent_neutral_third",         label: "Neutral Third %"       },
    { key: "percent_behind_ball",           label: "Behind Ball %"         },
    { key: "percent_infront_ball",          label: "Infront Ball %"        },
    { key: "percent_most_back",             label: "Most Back %"           },
    { key: "percent_most_forward",          label: "Most Forward %"        },
    { key: "average_distance_to_ball",      label: "Avg Dist to Ball"      },
    { key: "average_distance_to_mates",     label: "Avg Dist to Mates"     },
    { key: "goals_against_while_last_defender", label: "Goals as Last Def" },
  ],
  movement: [
    { key: "avg_speed",                label: "Avg Speed"           },
    { key: "avg_speed_percentage",     label: "Speed %"             },
    { key: "total_distance",           label: "Total Distance"      },
    { key: "percent_supersonic_speed", label: "Supersonic %"        },
    { key: "percent_boost_speed",      label: "Boost Speed %"       },
    { key: "percent_slow_speed",       label: "Slow Speed %"        },
    { key: "percent_ground",           label: "Ground %"            },
    { key: "percent_low_air",          label: "Low Air %"           },
    { key: "percent_high_air",         label: "High Air %"          },
    { key: "time_powerslide",          label: "Powerslide Time"     },
    { key: "count_powerslide",         label: "Powerslide Count"    },
    { key: "avg_powerslide_duration",  label: "Powerslide Duration" },
  ],
};


// ── BarChart ──────────────────────────────────────────────────────────────────
function BarChart({ field, data, loading }) {
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    setAnimated(false);
    if (!loading && data) {
      const t = setTimeout(() => setAnimated(true), 60);
      return () => clearTimeout(t);
    }
  }, [loading, data, field.key]);

  const values = RANK_GROUPS.map(r => data?.[r.key]?.[field.key] ?? null);
  const nonNull = values.filter(v => v != null);
  const minVal = nonNull.length ? Math.min(...nonNull) : 0;
  const maxVal = nonNull.length ? Math.max(...nonNull) : 0.001;
  const range  = maxVal - minVal || 0.001;

  const formatVal = (v) => {
    if (v == null) return "—";
    if (v >= 100000) return `${(v / 1000).toFixed(0)}k`;
    if (v >= 1000)   return `${(v / 1000).toFixed(1)}k`;
    return v % 1 === 0 ? String(Math.round(v)) : v.toFixed(2);
  };

  return (
    <div style={{
      background: "rgba(255,255,255,0.03)",
      border: "1px solid rgba(255,255,255,0.07)",
      borderRadius: 14,
      padding: "18px 18px 12px",
    }}>
      <div style={{
        fontSize: 10,
        fontWeight: 700,
        letterSpacing: 2,
        color: "rgba(255,255,255,0.35)",
        textTransform: "uppercase",
        marginBottom: 16,
      }}>
        {field.label}
      </div>

      {/* Bars */}
      <div style={{ display: "flex", alignItems: "flex-end", gap: 4, height: 110 }}>
        {RANK_GROUPS.map((rank, i) => {
          const val = values[i];
          const pct = val != null ? ((val - minVal) / range) * 85 + 5 : 0; // 5% min height so bar is always visible
          return (
            <div
              key={rank.key}
              title={`${rank.label}: ${formatVal(val)}`}
              style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-end", gap: 3, height: "100%" }}
            >
              <div style={{
                fontSize: 8,
                fontWeight: 700,
                color: rank.color,
                fontVariantNumeric: "tabular-nums",
                opacity: animated ? 1 : 0,
                transform: animated ? "none" : "translateY(4px)",
                transition: `opacity .3s ${i * 35}ms, transform .3s ${i * 35}ms`,
                whiteSpace: "nowrap",
                lineHeight: 1,
              }}>
                {loading ? "" : formatVal(val)}
              </div>
              <div style={{
                width: "100%", flex: 1,
                background: "rgba(255,255,255,0.05)",
                borderRadius: "4px 4px 2px 2px",
                display: "flex", alignItems: "flex-end", overflow: "hidden",
              }}>
                {loading ? (
                  <div style={{ width: "100%", height: "35%", background: "rgba(255,255,255,0.08)", animation: "pulse 1.5s ease infinite", animationDelay: `${i * 80}ms` }} />
                ) : (
                  <div style={{
                    width: "100%",
                    height: animated ? `${pct}%` : "0%",
                    background: `linear-gradient(to top, ${rank.color}, ${rank.color}99)`,
                    borderRadius: "3px 3px 0 0",
                    transition: `height 0.65s cubic-bezier(0.22,1,0.36,1) ${i * 40}ms`,
                    boxShadow: animated ? `0 -3px 10px ${rank.color}50` : "none",
                  }} />
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* X-axis */}
      <div style={{ display: "flex", gap: 4, marginTop: 6 }}>
        {RANK_GROUPS.map(rank => (
          <div key={rank.key} style={{
            flex: 1, textAlign: "center",
            fontSize: 8, fontWeight: 700, color: rank.color, letterSpacing: 0.3,
          }}>
            {rank.short}
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────────
export default function GlobalStats() {
  const [gameMode, setGameMode] = useState("ranked-doubles");
  const [activeTab, setActiveTab] = useState("core");
  const [cache, setCache] = useState({});
  const [loading, setLoading] = useState(false);

  const tab = STAT_TABS.find(t => t.key === activeTab);
  const cacheKey = `${activeTab}__${gameMode}`;

  useEffect(() => {
    if (!tab || cache[cacheKey]) return;
    setLoading(true);
    Promise.all(
      RANK_GROUPS.map(rank =>
        getRankStats(tab.route, rank.key, gameMode).then(res => [rank.key, res])
      )
    ).then(results => {
      const byRank = Object.fromEntries(results.map(([k, v]) => [k, v ?? {}]));
      setCache(prev => ({ ...prev, [cacheKey]: byRank }));
      setLoading(false);
    });
  }, [activeTab, gameMode]);

  const currentData = cache[cacheKey] || null;
  const fields = STAT_FIELDS[activeTab] || [];

  return (
    <div>
      <style>{`
        @keyframes pulse { 0%,100%{opacity:.3} 50%{opacity:.8} }
        @keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:none} }
      `}</style>

      {/* Game mode selector */}
      <div style={{ display: "flex", gap: 8, marginBottom: 28 }}>
        {GAME_MODES.map(m => {
          const active = gameMode === m.value;
          return (
            <button key={m.value} onClick={() => setGameMode(m.value)} style={{
              padding: "8px 20px", borderRadius: 8,
              border: active ? "1px solid var(--cyan, #00d4ff)" : "1px solid rgba(255,255,255,0.1)",
              background: active ? "rgba(0,212,255,0.12)" : "rgba(255,255,255,0.04)",
              color: active ? "var(--cyan, #00d4ff)" : "rgba(255,255,255,0.45)",
              fontWeight: 700, fontSize: 13, cursor: "pointer", transition: "all .2s", letterSpacing: 0.5,
            }}>
              {m.label}
            </button>
          );
        })}
      </div>

      {/* Stat tabs */}
      <div style={{ display: "flex", gap: 4, marginBottom: 28, borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
        {STAT_TABS.map(t => {
          const active = activeTab === t.key;
          return (
            <button key={t.key} onClick={() => setActiveTab(t.key)} style={{
              padding: "10px 22px", border: "none",
              borderBottom: active ? "2px solid var(--orange, #ff6b35)" : "2px solid transparent",
              background: "none",
              color: active ? "white" : "rgba(255,255,255,0.4)",
              fontWeight: active ? 700 : 500, fontSize: 14, cursor: "pointer",
              transition: "all .2s", letterSpacing: 0.5,
              display: "flex", alignItems: "center", gap: 6,
            }}>
              {t.label}
            </button>
          );
        })}
      </div>

      {/* Charts grid */}
      <div key={cacheKey} style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(380px, 1fr))",
        gap: 16,
        animation: "fadeUp .4s ease both",
      }}>
        {fields.map(field => (
          <BarChart key={field.key} field={field} data={currentData} loading={loading} />
        ))}
      </div>
    </div>
  );
}
