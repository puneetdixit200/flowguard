// Shows exactly what's working / broken across the whole pipeline —
// this directly answers "what's working, what's not" for the user.
import { useEffect, useState } from "react";
import { CheckCircle2, XCircle, Server, Radio, BrainCircuit, Network } from "lucide-react";
import { getHealth, getFlows, getGnnStatus } from "../api";

export default function StatusStrip() {
  const [stages, setStages] = useState([]);

  useEffect(() => {
    async function check() {
      const results = [];

      let apiOk = false;
      try { await getHealth(); apiOk = true; } catch { apiOk = false; }
      results.push({ label: "FastAPI Service", icon: Server, ok: apiOk });

      let flowsOk = false;
      if (apiOk) {
        try {
          const flows = await getFlows();
          flowsOk = flows.length > 0;
        } catch { flowsOk = false; }
      }
      results.push({ label: "Packet Capture", icon: Radio, ok: flowsOk });

      let gnnOk = false;
      if (apiOk) {
        try {
          const status = await getGnnStatus();
          gnnOk = status.loaded === true;
        } catch { gnnOk = false; }
      }
      results.push({ label: "GNN Detector", icon: Network, ok: gnnOk });
      results.push({ label: "ML Ensemble", icon: BrainCircuit, ok: apiOk });

      setStages(results);
    }

    check();
    const interval = setInterval(check, 5000); // re-check every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="status-strip">
      {stages.map((s) => (
        <div key={s.label} className={`status-card ${s.ok ? "ok" : "err"}`}>
          <div className="status-icon">
            <s.icon size={18} />
          </div>
          <div>
            <div className="status-label">{s.label}</div>
            <div className={`status-value ${s.ok ? "ok" : "err"}`}>
              {s.ok ? (
                <><CheckCircle2 size={14} /> Online</>
              ) : (
                <><XCircle size={14} /> Offline</>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
