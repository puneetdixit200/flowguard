const repositoryUrl = "https://github.com/puneetdixit200/flowguard";

const stack = [
  "eBPF / XDP",
  "C++17",
  "FastAPI",
  "Scikit-learn",
  "PyTorch",
  "PostgreSQL",
  "Redis",
  "Docker",
];

const architectureLayers = [
  {
    number: "01",
    eyebrow: "Kernel edge",
    title: "Packet capture",
    description:
      "eBPF/XDP observes packets before the traditional network stack, with a libpcap path available for repeatable offline analysis.",
    tags: ["XDP hook", "libbpf", "PCAP replay"],
  },
  {
    number: "02",
    eyebrow: "Systems core",
    title: "Flow processing",
    description:
      "A C++17 engine parses Ethernet, IPv4, TCP, and UDP traffic, then aggregates packets into bounded, thread-safe flow records.",
    tags: ["Parser", "Flow key", "Bounded queue"],
  },
  {
    number: "03",
    eyebrow: "Feature layer",
    title: "Telemetry shaping",
    description:
      "Raw flows become model-ready features such as byte rate, packet rate, TCP flag counts, duration, and connection ratios.",
    tags: ["JSONL", "Normalization", "Feature parity"],
  },
  {
    number: "04",
    eyebrow: "Detection layer",
    title: "Multi-model inference",
    description:
      "Isolation Forest, Random Forest, Autoencoder, and GraphSAGE contribute complementary anomaly and classification signals.",
    tags: ["Ensemble", "Thresholds", "Confidence"],
  },
  {
    number: "05",
    eyebrow: "Application layer",
    title: "Alert intelligence",
    description:
      "FastAPI turns model output into severity, explanations, persistence records, cached state, and live notification events.",
    tags: ["REST", "WebSocket", "Threat context"],
  },
  {
    number: "06",
    eyebrow: "Operator layer",
    title: "Security dashboard",
    description:
      "A live console exposes health, model posture, traffic trends, protocol distribution, and prioritized alerts for investigation.",
    tags: ["Metrics", "Charts", "Alert queue"],
  },
];

const pipeline = [
  ["Capture", "Packets enter through XDP or PCAP"],
  ["Parse", "Headers become typed packet records"],
  ["Aggregate", "Bidirectional traffic becomes flows"],
  ["Engineer", "Runtime features match training inputs"],
  ["Score", "Models vote with tuned thresholds"],
  ["Explain", "Severity and evidence are attached"],
  ["Respond", "Alerts persist, publish, and render"],
];

const modelMetrics = [
  {
    name: "Random Forest",
    role: "Supervised classifier",
    accuracy: "86.09%",
    recall: "98.94%",
    scoreLabel: "ROC-AUC",
    score: "90.36%",
    accent: "cyan",
  },
  {
    name: "Autoencoder",
    role: "Reconstruction anomaly model",
    accuracy: "75.86%",
    recall: "81.80%",
    scoreLabel: "ROC-AUC",
    score: "77.65%",
    accent: "violet",
  },
  {
    name: "Isolation Forest",
    role: "Unsupervised anomaly model",
    accuracy: "62.51%",
    recall: "99.26%",
    scoreLabel: "ROC-AUC",
    score: "65.58%",
    accent: "amber",
  },
  {
    name: "Four-model ensemble",
    role: "Consensus detection",
    accuracy: "84.71%",
    recall: "81.66%",
    scoreLabel: "F1 score",
    score: "84.23%",
    accent: "green",
  },
];

const capabilities = [
  {
    marker: "KERNEL",
    title: "High-speed packet visibility",
    description:
      "Capture begins close to the network interface, reducing unnecessary handoffs before FlowGuard starts understanding traffic.",
  },
  {
    marker: "SYSTEMS",
    title: "Purpose-built C++ data plane",
    description:
      "Typed parsing, flow keys, bounded queues, multithreading, and atomic coordination keep the core explicit and measurable.",
  },
  {
    marker: "ML",
    title: "Complementary detection models",
    description:
      "Supervised, unsupervised, reconstruction, and graph-based approaches expose different failure modes instead of trusting one oracle.",
  },
  {
    marker: "API",
    title: "Explainable alert contract",
    description:
      "Each detection carries severity, confidence, model votes, predicted class, and supporting details for the operator.",
  },
  {
    marker: "DATA",
    title: "Persistent and real-time state",
    description:
      "PostgreSQL stores alerts while Redis supports caching and publish-subscribe paths for responsive downstream consumers.",
  },
  {
    marker: "OPS",
    title: "Containerized end-to-end runtime",
    description:
      "Docker Compose connects capture, inference, storage, cache, and dashboard services into a reproducible environment.",
  },
];

function BrandMark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <span className="brand-mark-core" />
      <span className="brand-mark-ring brand-mark-ring-one" />
      <span className="brand-mark-ring brand-mark-ring-two" />
    </span>
  );
}

function ArrowIcon() {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true">
      <path d="M4 10h11M11 5l5 5-5 5" />
    </svg>
  );
}

function GitHubIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 2.6a9.7 9.7 0 0 0-3.1 18.9c.5.1.7-.2.7-.5v-1.9c-2.8.6-3.4-1.2-3.4-1.2-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 0 1.6 1.1 1.6 1.1.9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.7-1.3-2.3-.3-4.7-1.1-4.7-5.1 0-1.1.4-2 1-2.8-.1-.3-.4-1.3.1-2.8 0 0 .8-.3 2.9 1.1a10 10 0 0 1 5.2 0c2-1.4 2.9-1.1 2.9-1.1.5 1.5.2 2.5.1 2.8.6.8 1 1.7 1 2.8 0 4-2.4 4.8-4.7 5.1.4.3.7 1 .7 2v3c0 .3.2.6.7.5A9.7 9.7 0 0 0 12 2.6Z" />
    </svg>
  );
}

function DashboardPreview() {
  return (
    <div className="dashboard-window" aria-label="Illustrated FlowGuard dashboard preview">
      <div className="window-bar">
        <div className="window-dots" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <div className="window-address">
          <span className="address-lock" />
          flowguard.local / overview
        </div>
        <span className="live-chip"><span /> live</span>
      </div>

      <div className="dashboard-body">
        <div className="dashboard-sidebar">
          <BrandMark />
          <span className="side-item active" />
          <span className="side-item" />
          <span className="side-item" />
          <span className="side-item" />
        </div>

        <div className="dashboard-content">
          <div className="preview-header">
            <div>
              <span className="preview-kicker">NETWORK POSTURE</span>
              <strong>Flow telemetry</strong>
            </div>
            <span className="preview-status">All systems online</span>
          </div>

          <div className="preview-stats">
            <div>
              <span>Capture</span>
              <strong>XDP</strong>
              <small>kernel path</small>
            </div>
            <div>
              <span>Detection</span>
              <strong>4 models</strong>
              <small>consensus layer</small>
            </div>
            <div>
              <span>Pipeline</span>
              <strong>7 stages</strong>
              <small>end to end</small>
            </div>
          </div>

          <div className="preview-grid">
            <div className="traffic-panel">
              <div className="panel-heading">
                <span>Traffic activity</span>
                <small>LAST 60 SECONDS</small>
              </div>
              <div className="chart-grid" aria-hidden="true">
                <span /><span /><span /><span />
                <svg viewBox="0 0 520 150" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#2dd4bf" stopOpacity="0.35" />
                      <stop offset="100%" stopColor="#2dd4bf" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  <path className="chart-area" d="M0 130 C38 118 42 75 80 88 S136 125 170 74 S225 38 265 68 S320 136 355 82 S412 35 448 55 S486 103 520 24 L520 150 L0 150 Z" />
                  <path className="chart-line" d="M0 130 C38 118 42 75 80 88 S136 125 170 74 S225 38 265 68 S320 136 355 82 S412 35 448 55 S486 103 520 24" />
                  <circle cx="520" cy="24" r="5" />
                </svg>
              </div>
            </div>

            <div className="model-panel">
              <div className="panel-heading">
                <span>Model votes</span>
                <small>FLOW 8F3A</small>
              </div>
              <div className="vote-list">
                <div><span><i className="vote-dot danger" />Random Forest</span><b>attack</b></div>
                <div><span><i className="vote-dot danger" />Autoencoder</span><b>anomaly</b></div>
                <div><span><i className="vote-dot safe" />Isolation Forest</span><b>normal</b></div>
                <div><span><i className="vote-dot danger" />GraphSAGE</span><b>attack</b></div>
              </div>
              <div className="risk-card">
                <span>Ensemble decision</span>
                <strong>HIGH RISK</strong>
                <small>3 of 4 models agree</small>
              </div>
            </div>
          </div>

          <div className="alert-row">
            <span className="alert-pulse" />
            <div><strong>Potential intrusion detected</strong><small>10.10.2.101 → 43.159.99.24 · TCP · confidence 0.91</small></div>
            <span className="severity-badge">HIGH</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <main>
      <div className="ambient ambient-one" aria-hidden="true" />
      <div className="ambient ambient-two" aria-hidden="true" />

      <header className="site-header">
        <a className="brand" href="#top" aria-label="FlowGuard home">
          <BrandMark />
          <span className="brand-copy">
            <strong>FlowGuard</strong>
            <small>Network intelligence</small>
          </span>
        </a>

        <nav className="desktop-nav" aria-label="Primary navigation">
          <a href="#architecture">Architecture</a>
          <a href="#pipeline">Pipeline</a>
          <a href="#models">Models</a>
          <a href="#capabilities">Capabilities</a>
        </nav>

        <a className="header-cta" href={repositoryUrl} target="_blank" rel="noreferrer">
          <GitHubIcon />
          GitHub
        </a>
      </header>

      <section className="hero section-shell" id="top">
        <div className="hero-copy">
          <div className="eyebrow"><span /> Research-grade intrusion detection</div>
          <h1>
            See threats <span>before</span> they become incidents.
          </h1>
          <p className="hero-lead">
            FlowGuard connects kernel-level packet capture, a multithreaded C++ flow engine,
            four machine-learning models, and an operator dashboard into one end-to-end
            network defense framework.
          </p>

          <div className="hero-actions">
            <a className="button button-primary" href="#architecture">
              Explore the system <ArrowIcon />
            </a>
            <a className="button button-secondary" href={repositoryUrl} target="_blank" rel="noreferrer">
              <GitHubIcon /> View source
            </a>
          </div>

          <div className="hero-proof" aria-label="FlowGuard highlights">
            <div><strong>4</strong><span>detection models</span></div>
            <div><strong>7</strong><span>pipeline stages</span></div>
            <div><strong>10k</strong><span>real-flow test rows</span></div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="visual-orbit orbit-one" aria-hidden="true" />
          <div className="visual-orbit orbit-two" aria-hidden="true" />
          <DashboardPreview />
          <div className="floating-card floating-card-one">
            <span className="floating-icon">01</span>
            <div><strong>Packet captured</strong><small>XDP ingress path</small></div>
          </div>
          <div className="floating-card floating-card-two">
            <span className="floating-icon alert">!</span>
            <div><strong>Consensus reached</strong><small>3 model votes · high</small></div>
          </div>
        </div>
      </section>

      <section className="stack-strip" aria-label="Technology stack">
        <div className="stack-track">
          {stack.map((item) => (
            <span key={item}><i />{item}</span>
          ))}
        </div>
      </section>

      <section className="intro section-shell">
        <div className="section-label">WHY FLOWGUARD</div>
        <div className="intro-grid">
          <h2>Network security is not one model and a hopeful dashboard.</h2>
          <div className="intro-copy">
            <p>
              Useful intrusion detection requires visibility at the packet edge, disciplined
              systems engineering, feature consistency, calibrated models, persistent evidence,
              and an interface an operator can actually read.
            </p>
            <p>
              FlowGuard treats those as one connected system. Every layer is inspectable, from
              the first Ethernet frame to the final alert explanation.
            </p>
          </div>
        </div>
      </section>

      <section className="architecture section-shell" id="architecture">
        <div className="section-heading">
          <div>
            <span className="section-label">SYSTEM ARCHITECTURE</span>
            <h2>Defense in depth, implemented as software.</h2>
          </div>
          <p>
            Six coordinated layers transform raw traffic into evidence an analyst can act on.
          </p>
        </div>

        <div className="architecture-rail" aria-hidden="true">
          <span>NIC</span><i /><span>XDP</span><i /><span>C++</span><i /><span>ML</span><i /><span>API</span><i /><span>UI</span>
        </div>

        <div className="architecture-grid">
          {architectureLayers.map((layer) => (
            <article className="architecture-card" key={layer.number}>
              <div className="card-topline">
                <span className="layer-number">{layer.number}</span>
                <span className="layer-eyebrow">{layer.eyebrow}</span>
              </div>
              <h3>{layer.title}</h3>
              <p>{layer.description}</p>
              <div className="tag-row">
                {layer.tags.map((tag) => <span key={tag}>{tag}</span>)}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="pipeline section-shell" id="pipeline">
        <div className="pipeline-copy">
          <span className="section-label">PACKET TO ALERT</span>
          <h2>One observable path from wire to decision.</h2>
          <p>
            FlowGuard keeps the data lineage explicit. Each stage has a narrow responsibility,
            a clear handoff, and artifacts that can be inspected during debugging or research.
          </p>
          <a className="text-link" href={`${repositoryUrl}/tree/main/docs/diagrams`} target="_blank" rel="noreferrer">
            Open engineering diagrams <ArrowIcon />
          </a>
        </div>

        <div className="pipeline-list">
          {pipeline.map(([title, description], index) => (
            <div className="pipeline-step" key={title}>
              <span className="step-index">{String(index + 1).padStart(2, "0")}</span>
              <div><strong>{title}</strong><p>{description}</p></div>
              <span className="step-node" aria-hidden="true" />
            </div>
          ))}
        </div>
      </section>

      <section className="models" id="models">
        <div className="section-shell">
          <div className="section-heading models-heading">
            <div>
              <span className="section-label">MODEL BENCHMARKS</span>
              <h2>Measured on real-flow evaluation data.</h2>
            </div>
            <div className="dataset-note">
              <span><strong>20,000</strong> training</span>
              <span><strong>4,000</strong> validation</span>
              <span><strong>10,000</strong> testing</span>
            </div>
          </div>

          <div className="model-grid">
            {modelMetrics.map((model) => (
              <article className={`model-card model-${model.accent}`} key={model.name}>
                <div className="model-card-header">
                  <span className="model-status" />
                  <span>{model.role}</span>
                </div>
                <h3>{model.name}</h3>
                <div className="metric-primary">
                  <strong>{model.accuracy}</strong>
                  <span>accuracy</span>
                </div>
                <div className="metric-bars">
                  <div>
                    <span><b>Recall</b><em>{model.recall}</em></span>
                    <i><u style={{ width: model.recall }} /></i>
                  </div>
                  <div>
                    <span><b>{model.scoreLabel}</b><em>{model.score}</em></span>
                    <i><u style={{ width: model.score }} /></i>
                  </div>
                </div>
              </article>
            ))}
          </div>

          <p className="metrics-disclaimer">
            Evaluation results describe the checked-in research dataset and thresholds. They are
            evidence, not a magical guarantee that the internet has suddenly become well behaved.
          </p>
        </div>
      </section>

      <section className="capabilities section-shell" id="capabilities">
        <div className="section-heading">
          <div>
            <span className="section-label">ENGINEERING CAPABILITIES</span>
            <h2>Built across the whole stack.</h2>
          </div>
          <p>
            FlowGuard is deliberately broader than a notebook model or a dashboard mockup.
          </p>
        </div>

        <div className="capability-grid">
          {capabilities.map((capability) => (
            <article className="capability-card" key={capability.marker}>
              <span>{capability.marker}</span>
              <h3>{capability.title}</h3>
              <p>{capability.description}</p>
              <i aria-hidden="true" />
            </article>
          ))}
        </div>
      </section>

      <section className="code-section section-shell">
        <div className="code-window">
          <div className="code-window-bar">
            <span>flow_record.json</span>
            <div><i /><i /><i /></div>
          </div>
          <pre aria-label="Example FlowGuard flow record"><code>{`{
  "src_ip": "10.10.2.101",
  "dst_ip": "43.159.99.24",
  "protocol": "TCP",
  "packet_count": 184,
  "total_bytes": 129440,
  "duration_seconds": 1.82,
  "syn_count": 17,
  "rst_count": 4,
  "bytes_per_sec": 71120.88,
  "ensemble": {
    "votes": 3,
    "severity": "high",
    "confidence": 0.91
  }
}`}</code></pre>
        </div>

        <div className="code-copy">
          <span className="section-label">INSPECTABLE BY DESIGN</span>
          <h2>Security decisions should leave evidence.</h2>
          <p>
            Structured flow records connect capture, feature engineering, inference, persistence,
            and UI state. That makes the system easier to test, reproduce, audit, and improve.
          </p>
          <ul>
            <li><span>01</span> Deterministic flow keys and typed statistics</li>
            <li><span>02</span> Training and runtime feature parity</li>
            <li><span>03</span> Per-model votes and confidence metadata</li>
            <li><span>04</span> Stored alerts with analyst-facing context</li>
          </ul>
        </div>
      </section>

      <section className="cta-section section-shell">
        <div className="cta-glow" aria-hidden="true" />
        <div className="cta-copy">
          <span className="section-label">OPEN SOURCE PROJECT</span>
          <h2>Explore the architecture. Run the stack. Inspect every decision.</h2>
          <p>
            The repository includes capture engines, model training, evaluation artifacts, API
            services, dashboard code, diagrams, Docker configuration, and deployment blueprints.
          </p>
        </div>
        <div className="cta-actions">
          <a className="button button-light" href={repositoryUrl} target="_blank" rel="noreferrer">
            <GitHubIcon /> Explore on GitHub
          </a>
          <a className="button button-ghost" href={`${repositoryUrl}/tree/main/docs`} target="_blank" rel="noreferrer">
            Read the docs <ArrowIcon />
          </a>
        </div>
      </section>

      <footer className="site-footer section-shell">
        <div className="footer-brand">
          <BrandMark />
          <div><strong>FlowGuard</strong><span>End-to-end network intrusion detection</span></div>
        </div>
        <p>Designed and engineered by Puneet Dixit.</p>
        <div className="footer-links">
          <a href={repositoryUrl} target="_blank" rel="noreferrer">Repository</a>
          <a href={`${repositoryUrl}/tree/main/docs`} target="_blank" rel="noreferrer">Documentation</a>
          <a href="#top">Back to top</a>
        </div>
      </footer>
    </main>
  );
}
