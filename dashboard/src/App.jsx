import StatusStrip from "./components/StatusStrip";
import AlertFeed from "./components/AlertFeed";
import GnnGraphView from "./components/GnnGraphView";
import { useState, useEffect } from "react";
import { runAnalysis } from "./api";
import "./App.css";

function App() {
  const [running, setRunning] = useState(false);

  async function handleAnalyze() {
    setRunning(true);
    try { await runAnalysis(); } catch (e) { console.error(e); }
    setRunning(false);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>FlowGuard</h1>
        <button onClick={handleAnalyze} disabled={running}>
          {running ? "Analyzing..." : "Run Analysis"}
        </button>
      </header>

      <main>
        <StatusStrip />
        <div className="panel-grid">
          <AlertFeed />
          <GnnGraphView nodes={[]} edges={[]} /* wire this to /gnn/graph endpoint */ />
        </div>
      </main>
    </div>
  );
}

export default App;
