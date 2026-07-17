// Renders the live alert feed, driven entirely by the WebSocket hook.
// Each alert shows severity, confidence, and (from our earlier build)
// a human-readable explanation — no black-box scores.
import { useLiveAlerts } from "../hooks/useLiveAlerts";

export default function AlertFeed() {
  const { alerts, connected } = useLiveAlerts();

  return (
    <div className="panel">
      <div className="panel-header">
        <h3>Live Alerts {connected ? "🟢" : "🔴"}</h3>
        <span>{alerts.length} received this session</span>
      </div>

      {alerts.length === 0 ? (
        <div className="empty-state">No alerts yet — run analysis to scan flows.</div>
      ) : (
        <table>
          <thead>
            <tr><th>Time</th><th>Source</th><th>Severity</th><th>Explanation</th></tr>
          </thead>
          <tbody>
            {alerts.map((a) => (
              <tr key={a.id}>
                <td>{new Date(a.timestamp).toLocaleTimeString()}</td>
                <td className="mono">{a.src_ip} → {a.dst_ip}</td>
                <td><span className={`badge ${a.severity}`}>{a.severity}</span></td>
                <td>{a.explanation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
