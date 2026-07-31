const repositoryUrl = "https://github.com/puneetdixit200/flowguard";
const evaluationUrl = `${repositoryUrl}/blob/main/docs/real_only_evaluation.txt`;

const headlineStats = [
  {
    value: "34,000",
    label: "real-flow rows",
    detail: "20k training · 4k validation · 10k testing",
  },
  {
    value: "98.94%",
    label: "Random Forest recall",
    detail: "4,947 of 5,000 malicious test flows surfaced",
  },
  {
    value: "90.36%",
    label: "Random Forest ROC-AUC",
    detail: "strongest individual model discrimination",
  },
  {
    value: "84.71%",
    label: "ensemble accuracy",
    detail: "four-model consensus on the real test set",
  },
  {
    value: "54.3%",
    label: "fewer false positives",
    detail: "ensemble vs. Random Forest in the same test split",
  },
  {
    value: "160k",
    label: "test-graph edges",
    detail: "10,000 nodes used for GraphSAGE evaluation",
  },
];

const measuredImpact = [
  {
    number: "4,947",
    title: "Malicious flows identified",
    description:
      "Random Forest detected 4,947 of 5,000 malicious flows in the held-out test set, missing 53 during that evaluation.",
    footnote: "98.94% recall · supervised model",
  },
  {
    number: "612",
    title: "Ensemble false positives",
    description:
      "Four-model consensus reduced false positives from 1,338 to 612 compared with Random Forest, while trading some recall for stricter agreement.",
    footnote: "54.3% reduction · same 10k test split",
  },
  {
    number: "84.99%",
    title: "DDoS-family recall",
    description:
      "The selected ensemble also reached 80.35% recall on PortScan flows. Bot recall remained 2.27%, exposing a concrete limitation for future work.",
    footnote: "family-level results · limitations included",
  },
];

const engineeringImpact = [
  {
    marker: "01",
    title: "From packet edge to analyst evidence",
    description:
      "FlowGuard connects XDP and PCAP capture, C++ flow aggregation, model inference, persistence, notifications, and visualization instead of stopping at a notebook metric.",
  },
  {
    marker: "02",
    title: "Reproducible security experimentation",
    description:
      "Checked-in training scripts, thresholds, evaluation outputs, diagrams, and Docker services make results easier to inspect, repeat, challenge, and improve.",
  },
  {
    marker: "03",
    title: "Transparent model trade-offs",
    description:
      "Per-model scores, confusion matrices, family-level recall, and consensus behavior reveal where the system performs well and where more research is required.",
  },
];

function BrandMark() {
  return (
    <span className="chrome-brand-mark" aria-hidden="true">
      <span className="chrome-brand-core" />
      <span className="chrome-brand-ring chrome-brand-ring-one" />
      <span className="chrome-brand-ring chrome-brand-ring-two" />
    </span>
  );
}

function GitHubIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 2.6a9.7 9.7 0 0 0-3.1 18.9c.5.1.7-.2.7-.5v-1.9c-2.8.6-3.4-1.2-3.4-1.2-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 0 1.6 1.1 1.6 1.1.9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.7-1.3-2.3-.3-4.7-1.1-4.7-5.1 0-1.1.4-2 1-2.8-.1-.3-.4-1.3.1-2.8 0 0 .8-.3 2.9 1.1a10 10 0 0 1 5.2 0c2-1.4 2.9-1.1 2.9-1.1.5 1.5.2 2.5.1 2.8.6.8 1 1.7 1 2.8 0 4-2.4 4.8-4.7 5.1.4.3.7 1 .7 2v3c0 .3.2.6.7.5A9.7 9.7 0 0 0 12 2.6Z" />
    </svg>
  );
}

function ArrowIcon() {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true">
      <path d="M4 10h11M11 5l5 5-5 5" />
    </svg>
  );
}

export function StickyNavigation() {
  return (
    <header className="flowguard-sticky-header">
      <div className="chrome-header-inner">
        <a className="chrome-brand" href="#top" aria-label="FlowGuard home">
          <BrandMark />
          <span>
            <strong>FlowGuard</strong>
            <small>Network intelligence</small>
          </span>
        </a>

        <nav className="chrome-nav" aria-label="Primary navigation">
          <a href="#architecture">Architecture</a>
          <a href="#pipeline">Pipeline</a>
          <a href="#models">Models</a>
          <a href="#capabilities">Capabilities</a>
          <a href="#impact">Stats &amp; impact</a>
        </nav>

        <a className="chrome-github" href={repositoryUrl} target="_blank" rel="noreferrer">
          <GitHubIcon />
          <span>GitHub</span>
        </a>
      </div>
    </header>
  );
}

export function ImpactSection() {
  return (
    <>
      <section className="impact-section" id="impact">
        <div className="impact-shell">
          <div className="impact-heading">
            <div>
              <span className="impact-label">REAL STATS &amp; OBSERVED IMPACT</span>
              <h2>Measured results, including the inconvenient parts.</h2>
            </div>
            <p>
              These figures come from FlowGuard&apos;s checked-in real-flow evaluation artifacts.
              They describe the research test set, not an unverified production guarantee.
            </p>
          </div>

          <div className="headline-stat-grid">
            {headlineStats.map((stat) => (
              <article className="headline-stat" key={stat.label}>
                <strong>{stat.value}</strong>
                <span>{stat.label}</span>
                <small>{stat.detail}</small>
              </article>
            ))}
          </div>

          <div className="impact-subheading">
            <span className="impact-label">EVALUATION OUTCOMES</span>
            <h3>What the system actually changed in testing.</h3>
          </div>

          <div className="measured-impact-grid">
            {measuredImpact.map((item) => (
              <article className="measured-impact-card" key={item.title}>
                <strong className="impact-number">{item.number}</strong>
                <h4>{item.title}</h4>
                <p>{item.description}</p>
                <small>{item.footnote}</small>
              </article>
            ))}
          </div>

          <div className="engineering-impact-panel">
            <div className="engineering-impact-copy">
              <span className="impact-label">ENGINEERING IMPACT</span>
              <h3>More than a classifier with a dramatic chart.</h3>
              <p>
                FlowGuard&apos;s larger contribution is the connected, inspectable path from raw
                network traffic to an explainable alert and a usable operator interface.
              </p>
              <a href={evaluationUrl} target="_blank" rel="noreferrer">
                View raw evaluation output <ArrowIcon />
              </a>
            </div>

            <div className="engineering-impact-list">
              {engineeringImpact.map((item) => (
                <article key={item.marker}>
                  <span>{item.marker}</span>
                  <div>
                    <h4>{item.title}</h4>
                    <p>{item.description}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      <footer className="chrome-footer">
        <div className="chrome-footer-inner">
          <div className="chrome-footer-brand">
            <BrandMark />
            <div>
              <strong>FlowGuard</strong>
              <span>End-to-end network intrusion detection</span>
            </div>
          </div>
          <p>Designed and engineered by Puneet Dixit.</p>
          <div className="chrome-footer-links">
            <a href={repositoryUrl} target="_blank" rel="noreferrer">Repository</a>
            <a href={`${repositoryUrl}/tree/main/docs`} target="_blank" rel="noreferrer">Documentation</a>
            <a href="#top">Back to top</a>
          </div>
        </div>
      </footer>
    </>
  );
}
