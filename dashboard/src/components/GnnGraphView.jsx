// Visualizes the IP graph the GNN is scoring — this is the killer demo
// screen. Flagged/anomalous IPs render in red so you can literally SEE
// a coordinated scan pattern that flat models would miss.
import { useEffect, useRef } from "react";
import * as d3 from "d3"; // run: npm install d3

export default function GnnGraphView({ nodes, edges }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!nodes?.length) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // clear previous render on data change

    const width = 600, height = 400;

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(edges).id((d) => d.id).distance(60))
      .force("charge", d3.forceManyBody().strength(-100))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("stroke", "#333");

    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 8)
      .attr("fill", (d) => (d.is_anomalous ? "#f87171" : "#2dd4bf"));

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x).attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x).attr("y2", (d) => d.target.y);
      node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    });
  }, [nodes, edges]);

  return (
    <div className="panel">
      <h3>Network Graph — GNN Threat View</h3>
      <p style={{ fontSize: 12, color: "#8b929e" }}>
        Red nodes = hosts the GNN flagged as anomalous based on graph structure, not just single-flow stats.
      </p>
      <svg ref={svgRef} width={600} height={400}></svg>
    </div>
  );
}
