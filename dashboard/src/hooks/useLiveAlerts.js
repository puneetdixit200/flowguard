// Custom hook that connects to the WebSocket stream from Part 2 of our
// backend build and keeps a running list of alerts, updated in real time —
// no polling needed.
import { useEffect, useRef, useState } from "react";

export function useLiveAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/stream/alerts");
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);

    ws.onmessage = (event) => {
      const alert = JSON.parse(event.data);
      // Prepend new alert, cap the list at 100 so the UI stays fast.
      setAlerts((prev) => [alert, ...prev].slice(0, 100));
    };

    return () => ws.close(); // cleanup on unmount — avoids memory leaks
  }, []);

  return { alerts, connected };
}
