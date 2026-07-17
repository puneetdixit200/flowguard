# FlowGuard — Case Study

## Objective
Detect network anomalies (port scans, DDoS, brute force) in real time using
a C++ packet-capture pipeline and a 3-model ML ensemble.

## Approach
- C++17 + libpcap for performance-sensitive packet parsing and flow aggregation
- Producer-consumer threading with a bounded blocking queue
- Python ensemble: Isolation Forest (unsupervised), Random Forest (supervised
  multi-class), PyTorch Autoencoder (reconstruction-error anomaly detection)
- 2-of-3 vote rule to reduce false positives from any single model
- PostgreSQL (via Prisma) for durable alert storage, Redis Pub/Sub for
  real-time dashboard updates
- Local threat intel correlation against known-bad IP ranges

## Findings
- On synthetic held-out test data: [paste your evaluate_models.py output here]
- On real attack pcap replay: [document real false positive/negative rate here]
- Isolation Forest alone had the highest false positive rate; Random Forest
  was most precise but needs labeled data the other two don't
- The ensemble reduced false positives by requiring agreement, at the cost
  of slightly lower recall on subtle/stealthy attacks

## Reflection
- Rule-based systems are easy to reason about but miss unknown attack shapes
- Unsupervised models catch novelty but are noisier
- Explainability (showing WHY a flow was flagged) mattered more for trust
  than raw model accuracy
- Next step: adversarial testing against slow/low-and-slow scan patterns
