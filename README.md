
# FlowGuard

> A full-stack network intrusion detection and traffic-analysis platform built with C++17, native XDP/eBPF, FastAPI, scikit-learn, PyTorch, PyTorch Geometric, PostgreSQL, Redis, Prisma ORM, Docker Compose, and Nginx.

FlowGuard converts raw network packets into flow-level security telemetry, evaluates each flow using multiple machine-learning approaches, and exposes the resulting detections through a REST API and monitoring dashboard.

The project combines three engineering areas:

- **Systems and networking:** C++ packet parsing, multithreading, flow aggregation, libpcap, Linux networking, native XDP/eBPF, BPF maps, and ring buffers.
- **Machine learning:** Random Forest, Isolation Forest, Autoencoder, GraphSAGE, feature engineering, threshold tuning, capture-day-separated evaluation, and ensemble analysis.
- **Backend and infrastructure:** FastAPI, PostgreSQL, Prisma ORM, Redis pub/sub, Docker Compose, Nginx, health checks, persistence, and shadow deployment.

---

## Table of Contents

- [Highlights](#highlights)
- [Verified Results](#verified-results)
- [What FlowGuard Does](#what-flowguard-does)
- [Architecture](#architecture)
- [Project Components](#project-components)
- [Network Features](#network-features)
- [Machine-Learning Models](#machine-learning-models)
- [Dataset and Evaluation Methodology](#dataset-and-evaluation-methodology)
- [Real-Data Model Results](#real-data-model-results)
- [eBPF/XDP Performance Benchmark](#ebpfxdp-performance-benchmark)
- [Live Shadow-Mode Evaluation](#live-shadow-mode-evaluation)
- [Project Layout](#project-layout)
- [Requirements](#requirements)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual C++ Capture Run](#manual-c-capture-run)
- [Manual FastAPI Run](#manual-fastapi-run)
- [eBPF/XDP Build and Run](#ebpfxdp-build-and-run)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Benchmark Reproduction](#benchmark-reproduction)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Generated Artifacts](#generated-artifacts)
- [Docker and Infrastructure Notes](#docker-and-infrastructure-notes)
- [Design Decisions](#design-decisions)
- [Limitations and Honest Interpretation](#limitations-and-honest-interpretation)
- [Roadmap](#roadmap)
- [Resume-Ready Summary](#resume-ready-summary)
- [Technology Keywords](#technology-keywords)

---

## Highlights

- Multithreaded **C++17/libpcap** packet-to-flow processing pipeline.
- Ethernet, IPv4, TCP, UDP, and ICMP parsing.
- Bounded producer-consumer queue with backpressure.
- Five-tuple flow aggregation and TCP flag statistics.
- Native **XDP/eBPF** packet parsing and early filtering.
- Kernel-to-userspace communication through a BPF ring buffer.
- FastAPI inference service with batch analysis and alert persistence.
- PostgreSQL-backed alert storage through Prisma ORM.
- Redis-based internal messaging/pub-sub support.
- Random Forest, Isolation Forest, PyTorch Autoencoder, and GraphSAGE.
- Real CICIDS2017 training and capture-day-separated final evaluation.
- Validation-selected Random Forest operating thresholds.
- Shadow deployment and legacy-versus-real model comparison.
- Reproducible C++ versus XDP performance benchmark.
- Docker Compose orchestration for the complete local stack.

---

## Verified Results

### Real-data intrusion-detection result

The strongest individual model was Random Forest:

| Metric | Result |
|---|---:|
| Test flows | 10,000 |
| Benign flows | 5,000 |
| Attack flows | 5,000 |
| Accuracy | **86.09%** |
| Precision | **78.71%** |
| Recall | **98.94%** |
| F1 score | **0.8767** |
| ROC-AUC | **0.9036** |
| False positives | 1,338 |
| False negatives | 53 |

The test data was separated by capture day from the training and validation data.

### Native XDP/eBPF performance result

| Metric | C++ userspace parser | Native XDP/eBPF parser |
|---|---:|---:|
| Processing cost | 108.456 ns/packet | **62.301 ns/packet** |
| Equivalent throughput | 9.07 million packets/s | **16.05 million packets/s** |
| Processing-cost reduction | — | **42.6%** |
| Equivalent-throughput improvement | — | **1.77×** |
| Sustained complete replay path | — | 316,330 packets/s |
| Observed packet loss | — | approximately 0% |

The XDP benchmark used seven measured runs and approximately 1.46 million replayed packets per run.

### Four-model ensemble result

The strict four-model ensemble prioritized agreement and reduced false alarms:

| Metric | Result |
|---|---:|
| Accuracy | 84.71% |
| Precision | **86.96%** |
| Recall | 81.66% |
| F1 score | 0.8423 |
| False positives | 612 |
| False negatives | 917 |
| False-positive reduction vs Random Forest | **54.3%** |

The ensemble improved precision and reduced false positives, but it also missed more attacks. Random Forest therefore remains the strongest general headline model.

---

## What FlowGuard Does

FlowGuard implements the following pipeline:

1. Read packets from a PCAP file or inspect live ingress traffic.
2. Validate Ethernet and IPv4 headers.
3. Parse TCP, UDP, ICMP, ports, lengths, timestamps, and TCP flags.
4. Convert packets into a structured `PacketInfo` representation.
5. Group packets into flows using a network five-tuple.
6. Calculate duration, traffic volume, rate, and TCP-behaviour features.
7. Emit completed flows as JSON Lines.
8. Load the flows into a FastAPI inference service.
9. Score each flow with one or more detection models.
10. Compare model decisions in shadow mode.
11. Optionally persist alerts in PostgreSQL.
12. Expose flows, alerts, metrics, and health state through REST endpoints.
13. Display operational data through an Nginx-served dashboard.

---

## Architecture

```text
                         ┌──────────────────────────────┐
                         │ PCAP replay or live traffic  │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ C++17/libpcap capture  │              │ Native XDP/eBPF path   │
        │ Userspace packet path  │              │ Kernel ingress path    │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ PacketParser           │              │ BPF maps / ring buffer │
        │ Ethernet/IP/TCP/UDP    │              │ pass/drop/event output │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     └───────────────────┬───────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Five-tuple aggregation │
                            │ Packet/byte/TCP stats  │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ JSONL feature pipeline │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ FastAPI ML service     │
                            │ Normalization/scoring  │
                            └────────────┬───────────┘
                                         ▼
          ┌──────────────────────────────────────────────────────────┐
          │ Random Forest │ Isolation Forest │ Autoencoder │ GraphSAGE │
          └──────────────────────────────┬───────────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Shadow comparison /    │
                            │ voting / alert logic   │
                            └────────────┬───────────┘
                                         ▼
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
        ┌────────────────────────┐                  ┌────────────────────────┐
        │ PostgreSQL + Prisma    │                  │ Redis pub/sub          │
        │ Durable alert storage  │                  │ Internal notifications │
        └────────────┬───────────┘                  └────────────┬───────────┘
                     └───────────────────┬───────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Nginx dashboard        │
                            │ Flows/alerts/metrics   │
                            └────────────────────────┘
```

---

## Project Components

### `capture-cpp`

The C++17 layer is responsible for packet parsing and flow aggregation.

Key responsibilities:

- Open PCAP files through libpcap.
- Parse Ethernet and IPv4 packet structure.
- Extract transport protocol and ports.
- Record packet size and nanosecond timestamp representation.
- Extract TCP SYN, ACK, FIN, and RST flags.
- Send parsed packets through a bounded blocking queue.
- Aggregate packets into flows.
- Write completed flow records to JSONL.

Concurrency model:

```text
Capture thread
    │
    ▼
BlockingQueue<PacketInfo>
    │
    ▼
Aggregation thread
```

The bounded queue provides backpressure when aggregation is slower than capture and prevents unrestricted memory growth.

### `capture-ebpf`

The eBPF layer performs packet inspection at the Linux XDP hook.

Implemented concepts:

- Native XDP attachment.
- Safe packet-bound checks required by the eBPF verifier.
- Ethernet and IPv4 parsing.
- Variable-length IPv4 header handling.
- TCP and UDP port extraction.
- Per-source tracking through BPF maps.
- Demonstration early-drop action.
- BPF ring-buffer event transfer.
- libbpf userspace loader.
- Signal-based cleanup and XDP detach.
- Dedicated silent benchmark program.

### `ml-service`

The Python service provides:

- Flow normalization.
- Feature generation.
- Saved-model loading.
- Legacy ensemble inference.
- Real-data Random Forest inference.
- Operational-threshold selection.
- Shadow-mode scoring.
- Side-by-side model comparison.
- Optional alert persistence.
- Alert lookup.
- Model metric reporting.
- OpenAPI documentation.

### `dashboard`

The verified dashboard is a static HTML/CSS/JavaScript interface served by Nginx.

It is intended to display:

- Recent network flows.
- Detected anomalies.
- Persisted alerts.
- Model and system metrics.
- Basic operational health.

### `docker-compose.yml`

The local stack contains:

- PostgreSQL 16
- Redis 7
- C++ capture service
- FastAPI ML service
- Nginx dashboard

PostgreSQL and Redis are kept inside the Compose network and are not intentionally exposed through host ports.

---

## Network Features

The real-data model pipeline uses 11 flow-level features:

| Feature | Meaning |
|---|---|
| `duration_seconds` | Time between first and last packet |
| `packet_count` | Number of packets in the flow |
| `total_bytes` | Total transferred bytes |
| `bytes_per_sec` | Byte-transfer rate |
| `packets_per_sec` | Packet rate |
| `syn_count` | TCP SYN flags observed |
| `ack_count` | TCP ACK flags observed |
| `fin_count` | TCP FIN flags observed |
| `rst_count` | TCP RST flags observed |
| `syn_ack_ratio` | SYN count relative to ACK activity |
| `rst_ratio` | RST count relative to packet count |

Derived features:

```text
bytes_per_sec   = total_bytes / duration_seconds
packets_per_sec = packet_count / duration_seconds
syn_ack_ratio   = syn_count / (ack_count + 1)
rst_ratio       = rst_count / (packet_count + 1)
```

Zero-duration flows are handled safely to avoid division by zero.

---

## Machine-Learning Models

### Random Forest

A supervised binary attack classifier trained on labelled benign and malicious traffic.

Strengths:

- Best overall real-data F1 score.
- Very high attack recall.
- Direct attack-probability output.
- Feature-importance support.
- Fast CPU inference.

### Isolation Forest

An unsupervised anomaly detector trained on benign traffic.

Strengths:

- Does not require attack labels during fitting.
- Detects outliers that differ from normal behaviour.
- Provides an independent anomaly signal.

Observed limitation:

- Very high recall but excessive false positives on the final real-data test split.

### PyTorch Autoencoder

A neural anomaly detector trained to reconstruct benign feature vectors.

Detection principle:

```text
low reconstruction error  → resembles learned benign behaviour
high reconstruction error → possible anomaly
```

The reconstruction threshold is selected from validation behaviour.

### GraphSAGE

A graph neural network implemented with PyTorch Geometric.

For the real CICIDS2017 experiment:

- Each flow is represented as a node.
- Similar flows are connected through feature-space proximity.
- GraphSAGE aggregates neighbourhood information.
- The correct description is a **flow-similarity graph model**.

The CICIDS2017 CSV files used in this experiment did not provide source and destination IP columns, so this model must not be described as a host-communication graph.

### Legacy three-model ensemble

The original project path combines:

- Isolation Forest
- Random Forest
- Autoencoder

An anomaly is raised when at least two of the three models agree.

This path belongs to the earlier prototype/held-out evaluation.

### Real-data four-model ensemble

The research evaluation combines:

- Random Forest
- Isolation Forest
- Autoencoder
- GraphSAGE

The evaluated strict agreement rule reduced false positives but caused a substantial recall drop.

---

## Dataset and Evaluation Methodology

### CICIDS2017 data

Total labelled records available locally:

| Category | Count |
|---|---:|
| Total | 2,830,743 |
| Benign | 2,273,097 |
| Attack | 557,646 |

Attack families represented in the source collection include:

- DDoS
- PortScan
- Bot
- FTP-Patator
- SSH-Patator
- DoS Hulk
- DoS GoldenEye
- DoS Slowhttptest
- DoS slowloris
- Heartbleed
- Web Attack — Brute Force
- Web Attack — XSS
- Web Attack — SQL Injection
- Infiltration

### Capture-day-separated splits

Instead of randomly mixing rows from the same capture files, FlowGuard separates the data by collection day:

| Split | Capture days | Benign | Attack | Total |
|---|---|---:|---:|---:|
| Training | Monday–Wednesday | 10,000 | 10,000 | 20,000 |
| Validation | Thursday | 2,000 | 2,000 | 4,000 |
| Final test | Friday | 5,000 | 5,000 | 10,000 |

The validation set is used for threshold selection. The Friday test split remains untouched until final evaluation.

### Why day separation matters

Random row splitting can produce overly optimistic results when nearly identical flows from the same capture occur in both training and test data.

Day-separated evaluation provides a more difficult test of:

- Cross-day generalization.
- Traffic-distribution changes.
- Previously unseen or sparsely represented attack families.
- Threshold robustness.
- Resistance to train-test leakage.

---

## Real-Data Model Results

### Binary classification metrics

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Isolation Forest | 62.51% | 57.21% | 99.26% | 72.59% |
| Random Forest | **86.09%** | 78.71% | **98.94%** | **87.67%** |
| Autoencoder | 75.86% | 73.11% | 81.80% | 77.21% |
| GraphSAGE | 55.39% | 52.85% | 99.88% | 69.13% |
| Strict four-model ensemble | 84.71% | **86.96%** | 81.66% | 84.23% |

Random Forest ROC-AUC:

```text
0.9036
```

### Confusion matrices

Format:

```text
[[true negatives, false positives],
 [false negatives, true positives]]
```

Random Forest:

```text
[[3662, 1338],
 [  53, 4947]]
```

Strict four-model ensemble:

```text
[[4388,  612],
 [ 917, 4083]]
```

### Operational trade-off

Compared with Random Forest, the ensemble:

- Reduced false positives from 1,338 to 612.
- Reduced false positives by 54.3%.
- Increased precision from 78.71% to 86.96%.
- Increased false negatives from 53 to 917.
- Reduced attack recall from 98.94% to 81.66%.

The ensemble is useful when false alarms are especially expensive, but Random Forest is the stronger general detector.

### Per-family ensemble recall

| Attack family | Recall | Test flows |
|---|---:|---:|
| DDoS | 84.99% | 2,152 |
| PortScan | 80.35% | 2,804 |
| Bot | 2.27% | 44 |

Bot recall was poor because the final sampling included few Bot flows and the training-day attack data did not provide equivalent Bot coverage.

---

## eBPF/XDP Performance Benchmark

### Workload

- PCAP: infected-Android traffic capture.
- PCAP size: approximately 24 MB.
- Packets per PCAP loop: 29,125.
- XDP replay loops per measured run: 50.
- Expected packets per measured run: 1,456,250.
- Measured runs: 7.
- XDP attachment mode: native.
- C++ build: Release mode with `-O3`.
- XDP benchmark: silent parser using a per-CPU map.
- Runtime measurement: kernel BPF program statistics through `bpftool`.

### Median C++ result

```text
C++ median CPU cost:          108.456 ns/packet
C++ median wall cost:         110.278 ns/packet
C++ equivalent throughput:    9,067,963 packets/s
```

### Median native-XDP result

```text
XDP median kernel cost:       62.301 ns/packet
XDP equivalent throughput:    16,051,175 packets/s
XDP sustained replay rate:    316,330 packets/s
XDP observed packet loss:     approximately 0%
```

### Improvement

```text
Processing-cost speedup:      1.74×
Equivalent-throughput gain:   1.77×
Processing-cost reduction:    42.6%
Equivalent-throughput rise:   approximately 77%
```

### Interpretation

The 16.05 million packets/s result is equivalent throughput calculated from measured kernel execution time.

The 316,330 packets/s result measures the complete replay path:

```text
PCAP
  → tcpreplay
  → virtual Ethernet pair
  → Linux ingress path
  → native XDP program
```

The complete replay rate includes replay generation, veth, scheduling, and other kernel overhead. It should not be described as the XDP parser's maximum theoretical capacity.

A measured delivery rate slightly above 100% was caused by a few additional control/interface packets. It is reported as approximately 100% delivery and approximately 0% loss.

---

## Live Shadow-Mode Evaluation

The selected real-data Random Forest is integrated into FastAPI without replacing the legacy alert pipeline.

### Real-model health example

```json
{
  "status": "ok",
  "model": "real_only_random_forest",
  "threshold": 0.0235,
  "operational_mode": "balanced",
  "flow_file": "data/flows_output.jsonl",
  "mode": "shadow"
}
```

### Operational mode

Select the threshold configuration through:

```bash
RF_OPERATIONAL_MODE=balanced
```

The balanced threshold was selected on the Thursday validation split.

### Model-comparison endpoint

The comparison route runs the legacy ensemble and real-data Random Forest on the same recent flows without writing alerts.

Verified comparison over 100 flows:

| Metric | Result |
|---|---:|
| Analyzed | 100 |
| Errors | 0 |
| Legacy alerts | 85 |
| Real Random Forest alerts | 100 |
| Both alert | 85 |
| Both benign | 0 |
| Legacy only | 0 |
| Real Random Forest only | 15 |
| Agreement | 85% |

The 15 disagreements shared a repeated inbound TCP/source-port-8080 pattern.

These live flows did not contain ground-truth labels. Therefore, the results show model disagreement and alert volume—not verified attacks or live accuracy.

---

## Historical Prototype Result

The earlier synthetic/held-out prototype used 940 rows:

- 830 benign
- 110 attacks

The legacy 2-of-3 ensemble achieved:

| Metric | Result |
|---|---:|
| Accuracy | 98.94% |
| Precision | 96.30% |
| Recall | 94.55% |
| F1 | 95.41% |
| False positives | 4 |
| False negatives | 6 |

This result is retained for project history and regression comparison. It is not the main real-data headline.

---

## Project Layout

Representative layout:

```text
flowguard/
├── capture-cpp/
│   ├── include/
│   │   ├── BlockingQueue.hpp
│   │   ├── FeatureEmitter.hpp
│   │   ├── FlowAggregator.hpp
│   │   ├── FlowKey.hpp
│   │   ├── FlowStats.hpp
│   │   ├── JsonSerializer.hpp
│   │   ├── PacketInfo.hpp
│   │   └── PacketParser.hpp
│   ├── src/
│   │   ├── main.cpp
│   │   ├── PacketParser.cpp
│   │   ├── FlowAggregator.cpp
│   │   ├── FeatureEmitter.cpp
│   │   ├── JsonSerializer.cpp
│   │   ├── benchmark.cpp
│   │   └── parser_benchmark.cpp
│   ├── tests/
│   ├── CMakeLists.txt
│   └── Dockerfile
├── capture-ebpf/
│   ├── xdp_filter.bpf.c
│   ├── xdp_filter.o
│   ├── loader.c
│   ├── loader
│   ├── xdp_parser_benchmark.c
│   └── xdp_parser_benchmark.o
├── ml-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── ml/
│   │   │   ├── ensemble.py
│   │   │   └── real_only_predictor.py
│   │   ├── routes/
│   │   │   └── real_analysis.py
│   │   ├── services/
│   │   └── models/
│   │       └── real_only/
│   ├── data/
│   │   └── real_only/
│   ├── training/
│   │   ├── train_evaluate_real_only.py
│   │   └── tune_real_rf_thresholds.py
│   ├── tests/
│   ├── prisma/
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── index.html
│   └── Dockerfile
├── data/
│   ├── sample/
│   ├── attack_samples/
│   ├── cicids2017/
│   └── flows_output.jsonl
├── docs/
│   ├── cpp_parser_benchmark.txt
│   ├── ebpf_vs_cpp_runs.csv
│   ├── ebpf_vs_cpp_benchmark.json
│   ├── ebpf_vs_cpp_benchmark.md
│   └── model_comparison.json
├── scripts/
│   └── benchmark_ebpf_vs_cpp.sh
├── docker-compose.yml
├── HOW_TO_RUN.md
└── README.md
```

Some generated datasets, model artifacts, PCAPs, and build outputs may be intentionally excluded from Git.

---

## Requirements

### General

- Linux
- Git
- Docker and Docker Compose
- Python 3
- CMake
- A C++17 compiler

### C++ capture

- libpcap
- pthread support

### eBPF/XDP

- Linux kernel with eBPF and XDP support
- Clang/LLVM
- libbpf and development headers
- bpftool
- Linux networking tools (`ip`)
- Root privileges for loading and attaching XDP programs

### Benchmarking

- tcpreplay
- tcpdump
- Python 3
- `kernel.bpf_stats_enabled` support

---

## Quick Start with Docker Compose

From the repository root:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Expected services:

```text
postgres
redis
capture
ml-service
dashboard
```

Check the API:

```bash
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/flows/recent?limit=2"
```

Open:

- Dashboard: `http://127.0.0.1:8080`
- OpenAPI documentation: `http://127.0.0.1:8000/docs`

View logs:

```bash
docker compose logs -f ml-service
```

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

---

## Manual C++ Capture Run

### Configure and compile

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

### Process a PCAP

```bash
./capture-cpp/build/flowguard_capture \
  data/sample/small_sample.pcap \
  data/flows_output.jsonl
```

### Inspect output

```bash
head -n 5 data/flows_output.jsonl
```

Each line represents one aggregated flow.

---

## Manual FastAPI Run

From the repository root:

```bash
cd ml-service
source .venv/bin/activate
```

Run the selected real-data operating mode:

```bash
RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Using `python -m uvicorn` avoids relying on a globally installed `uvicorn` command.

Check the service:

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

Check the real model:

```bash
curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
```

Run shadow inference:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool
```

Compare detectors:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  | python -m json.tool
```

---

## eBPF/XDP Build and Run

### Compile the XDP program

From the repository root:

```bash
clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_filter.bpf.c \
  -o capture-ebpf/xdp_filter.o
```

Verify the object:

```bash
file capture-ebpf/xdp_filter.o
```

Expected type:

```text
ELF 64-bit LSB relocatable, eBPF
```

### Compile the userspace loader

```bash
cc \
  -O2 \
  -g \
  capture-ebpf/loader.c \
  -o capture-ebpf/loader \
  $(pkg-config --cflags --libs libbpf)
```

### Attach to an interface

First identify the interface:

```bash
ip -br link
```

Then run the loader from the directory containing `xdp_filter.o`:

```bash
cd capture-ebpf
sudo ./loader wlan0
```

Replace `wlan0` with the correct interface.

Press `Ctrl+C` to stop the loader and detach the XDP program.

### Warning

The demonstration packet threshold in `xdp_filter.bpf.c` counts packets over the lifetime of the BPF map entry. It is not a time-windowed packets-per-second production rate limiter.

---

## Model Training and Evaluation

### Expected real-data locations

```text
data/cicids2017/
ml-service/data/real_only/
```

### Real-only training/evaluation

From `ml-service`:

```bash
PYTHONPATH=. \
.venv/bin/python \
training/train_evaluate_real_only.py
```

### Operational-threshold tuning

```bash
PYTHONPATH=. \
.venv/bin/python \
training/tune_real_rf_thresholds.py
```

Generated real-model artifacts are stored under:

```text
ml-service/app/models/real_only/
```

Expected artifacts include:

```text
random_forest.joblib
supervised_scaler.joblib
isolation_forest.joblib
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
thresholds.json
rf_operational_thresholds.json
```

### Important reproducibility note

Do not select thresholds using the final Friday test set. The project uses Thursday validation data for threshold selection and Friday data only for final evaluation.

---

## Benchmark Reproduction

### C++ parser benchmark

```bash
./capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
```

### Full XDP versus C++ benchmark

```bash
chmod +x scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh
```

The script:

- Enables BPF runtime statistics temporarily.
- Creates a temporary veth pair.
- Loads and pins the benchmark XDP program.
- Attaches it in native mode when supported.
- Replays the PCAP multiple times.
- Reads BPF runtime and packet counters.
- Calculates median metrics.
- Writes CSV, JSON, and Markdown reports.
- Detaches XDP and removes the temporary interfaces.

Generated output:

```text
docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
```

The benchmark requires `sudo`.

---

## API Reference

### Health

```http
GET /health
```

Basic API health check.

### Recent flows

```http
GET /flows/recent?limit=20
```

Returns the most recent captured flow records.

### Legacy batch analysis

```http
POST /analyze?offset=0&limit=100&persist=false
```

Parameters:

| Parameter | Meaning |
|---|---|
| `offset` | Starting flow index |
| `limit` | Batch size, up to 1,000 |
| `persist` | Save detected anomalies to PostgreSQL |

Use `persist=false` while validating behaviour.

### Alerts

```http
GET /alerts
GET /alerts/{alert_id}
```

Retrieves persisted alerts.

### Historical model metrics

```http
GET /metrics/model
```

Returns the historical held-out prototype metrics. This endpoint does not represent the final real-only Random Forest evaluation.

### Real-data model health

```http
GET /real-model/health
```

Returns:

- Model identifier
- Selected operational threshold
- Operational mode
- Resolved flow file
- Shadow-mode state

### Real-data shadow analysis

```http
POST /real-model/analyze?limit=50
```

Scores recent flows with the real-only Random Forest.

It does not persist alerts.

### Detector comparison

```http
POST /analyze/compare?limit=100
```

Runs the legacy ensemble and real Random Forest on the same recent flows.

Returns:

- Alert totals
- Agreement categories
- Agreement rate
- Real Random Forest probabilities
- Per-flow disagreement information
- Error details

The comparison route never persists alerts.

### Legacy real-capture route

```http
POST /analyse/real
```

This older experimental route is retained for compatibility. Prefer the `/real-model/*` routes for current shadow evaluation.

---

## Testing

### Python tests

```bash
cd ml-service

PYTHONPATH=. \
.venv/bin/python \
-m pytest tests -q
```

Previously verified result:

```text
8 passed
```

Re-run the suite after modifying inference routes or model-loading code.

### C++ tests

Configure and build:

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Debug

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

Run registered tests:

```bash
ctest \
  --test-dir capture-cpp/build \
  --output-on-failure
```

C++ test targets cover areas such as:

- Flow key ordering
- Flow aggregation
- Blocking queue behaviour
- Packet parsing
- JSON serialization

### Syntax checks

Python:

```bash
python -m py_compile \
  ml-service/app/main.py \
  ml-service/app/ml/real_only_predictor.py \
  ml-service/app/routes/real_analysis.py
```

Bash:

```bash
bash -n scripts/benchmark_ebpf_vs_cpp.sh
```

---

## Generated Artifacts

### Model artifacts

```text
ml-service/app/models/real_only/
├── anomaly_scaler.joblib
├── autoencoder.pt
├── graphsage_flow_similarity.pt
├── isolation_forest.joblib
├── random_forest.joblib
├── rf_operational_thresholds.json
├── supervised_scaler.joblib
└── thresholds.json
```

### Evaluation artifacts

```text
docs/
├── cpp_parser_benchmark.txt
├── ebpf_vs_cpp_runs.csv
├── ebpf_vs_cpp_benchmark.json
├── ebpf_vs_cpp_benchmark.md
├── model_comparison.json
└── rf_threshold_tuning.txt
```

### Prepared real-data splits

```text
ml-service/data/real_only/
├── train_real.csv
├── validation_real.csv
└── test_real.csv
```

Large datasets, model files, PCAPs, and generated build files may need Git LFS or external storage rather than ordinary Git commits.

---

## Docker and Infrastructure Notes

### PostgreSQL

PostgreSQL provides durable alert storage.

The Compose configuration uses:

```text
database: flowguard
user: flowguard_user
```

Credentials in the development Compose file are for local use only and must be replaced for deployment.

### Prisma ORM

Prisma provides schema-driven database access.

The ML container startup performs:

1. Wait for PostgreSQL.
2. Wait for Redis.
3. Run `prisma db push`.
4. Run `prisma generate`.
5. Start Uvicorn.

### Redis

Redis is used inside the Compose network for messaging/pub-sub support.

It is not intentionally exposed to the host.

### Capture permissions

The capture container receives:

```text
NET_ADMIN
NET_RAW
```

These capabilities are required for packet-capture and networking operations but should be minimized in production.

### ML image

The ML image installs CPU-only PyTorch packages to avoid pulling unnecessary GPU/CUDA layers for the local CPU inference workflow.

### Dashboard image

The verified dashboard container serves the static dashboard through Nginx.

---

## Design Decisions

### JSONL between C++ and Python

JSON Lines was selected because it is:

- Human-readable.
- Append-friendly.
- Easy to debug with standard shell tools.
- Supported directly by Python.
- Independent of the C++ process lifetime.
- Suitable for replay and offline evaluation.

### Bounded queue instead of an unbounded queue

A bounded queue prevents the capture thread from consuming unlimited memory if the aggregation thread cannot keep pace.

### Model loading at startup

Saved models are loaded once when the API process starts rather than once per request. This reduces inference latency and avoids repeated disk deserialization.

### Shadow deployment

The real-data model does not immediately replace or persist into the existing alert path.

Shadow deployment allows FlowGuard to measure:

- Alert volume.
- Model disagreement.
- Probability distribution.
- Feature-semantic mismatch.
- Domain shift.
- Runtime errors.

### Day-separated evaluation

Capture-day separation was selected to reduce leakage and make the model prove that it can generalize beyond the exact capture distribution used for fitting.

### Median benchmark reporting

Performance results use medians across repeated runs to reduce sensitivity to scheduler noise and occasional outliers.

---

## Limitations and Honest Interpretation

FlowGuard is an engineering and research project, not a production-certified intrusion-detection appliance.

### Live predictions are not ground truth

A live model label of `ATTACK` is a prediction, not confirmation of malicious activity.

Accuracy, precision, and recall require labelled data.

### High live alert rate indicates possible domain shift

The real-only Random Forest produced a high alert rate on the infected-host capture. This can reflect:

- Truly unusual traffic.
- Different feature semantics.
- Dataset-to-live distribution shift.
- Poor probability calibration.
- Incomplete flow reconstruction.

It must not be described as a verified attack rate.

### Balanced final test set

The final test set intentionally contains equal benign and attack counts.

This makes model comparison clear but does not represent the natural attack prevalence of most real networks.

### GraphSAGE limitations

The GraphSAGE model had extremely high recall but very poor benign classification.

It demonstrates graph-learning implementation but requires:

- Better graph construction.
- Calibration.
- Class weighting.
- Additional validation.
- More representative graph data.

### Infected-Android PCAP labels

The infected-Android PCAP does not provide per-flow ground-truth labels.

It is valid for:

- Systems benchmarking.
- Replay.
- End-to-end testing.
- Shadow inference.
- Disagreement analysis.

It is not valid for reporting classification accuracy.

### eBPF benchmark scope

The benchmark compares implemented parser-level cost.

It does not include:

- Flow aggregation parity.
- Machine-learning inference.
- PostgreSQL persistence.
- Redis publication.
- Dashboard latency.
- Complete packet-to-alert latency.

### Demonstration drop threshold

The original XDP source counter is lifetime-based. Production rate limiting requires a time-windowed policy.

---

## Roadmap

### Detection quality

- Probability calibration using isotonic regression or Platt scaling.
- Evaluation on naturally imbalanced traffic.
- Precision-recall curves and confidence intervals.
- Leave-one-attack-family-out testing.
- Better Bot-family coverage.
- Weighted voting or stacking instead of strict agreement.
- Incident-level alert grouping.
- Feature-semantic alignment between C++ flows and CICIDS flow generation.

### Graph learning

- True IP host-communication graphs.
- Temporal graph construction.
- Class-weighted GraphSAGE loss.
- Focal loss.
- Graph mini-batching.
- Validation-based early stopping.
- Neighbourhood and edge-feature ablation studies.

### eBPF/XDP

- Time-windowed packet-rate limiting.
- Production per-CPU counters.
- Ring-buffer loss counters.
- IPv6 parsing.
- VLAN support.
- AF_XDP experiment.
- Multi-core scaling benchmark.
- Physical-NIC benchmark.
- Packet-to-alert latency measurement.

### Backend and operations

- Prometheus metrics.
- Grafana dashboards.
- Authentication and role-based access.
- Model registry and rollback.
- Alert deduplication.
- Deployment-specific secrets.
- CI for Python, C++, Docker, and eBPF verifier checks.
- Structured logging and tracing.

---

## Resume-Ready Summary

### Detailed version

> Built FlowGuard, a full-stack network intrusion detection platform using C++17/libpcap, native XDP/eBPF, FastAPI, PostgreSQL, Redis, Prisma ORM, and Docker Compose. Trained Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE on capture-day-separated CICIDS2017 data; Random Forest achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 on 10,000 real labelled flows. Benchmarked native XDP across seven runs and approximately 1.46 million packets per run, achieving 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than the C++ userspace parser.

### Compact bullets

- Built a C++17/Python network intrusion detection pipeline using libpcap, native XDP/eBPF, five-tuple flow aggregation, FastAPI, PostgreSQL, Redis, and Docker Compose.
- Achieved **86.09% accuracy, 98.94% recall, and 0.8767 F1** with Random Forest on **10,000 real capture-day-separated CICIDS2017 flows**.
- Reduced Random Forest false positives by **54.3%** with a strict four-model ensemble, improving precision to **86.96%** while documenting the recall trade-off.
- Benchmarked native XDP at **62.3 ns/packet and 16.05M equivalent packets/s**, delivering **1.77× higher equivalent throughput** than the C++ parser.

---

## Technology Keywords

### Languages and systems

```text
C++17, C, Python, SQL, Bash, JavaScript, Linux, systems programming,
multithreading, producer-consumer, bounded queue, backpressure, mutex,
condition variable, atomic state, kernel programming
```

### Networking

```text
libpcap, PCAP, tcpreplay, Ethernet, IPv4, TCP, UDP, ICMP, five-tuple,
flow aggregation, TCP flags, packet parsing, network telemetry,
network intrusion detection, NIDS, DDoS, PortScan, Bot detection
```

### eBPF/XDP

```text
eBPF, XDP, native XDP, libbpf, bpftool, BPF maps, per-CPU maps,
ring buffer, kernel-space packet processing, packet filtering,
nanoseconds per packet, packets per second
```

### Machine learning

```text
scikit-learn, PyTorch, PyTorch Geometric, Random Forest,
Isolation Forest, Autoencoder, GraphSAGE, GNN, anomaly detection,
supervised learning, unsupervised learning, feature engineering,
threshold tuning, ensemble learning, ROC-AUC, precision, recall,
F1 score, confusion matrix, domain shift, data leakage,
capture-day separation, model generalization, shadow deployment
```

### Backend and DevOps

```text
FastAPI, REST API, Uvicorn, PostgreSQL, Prisma ORM, Redis, pub/sub,
Docker, Docker Compose, Nginx, CMake, Clang, health checks,
model serving, persistent storage, internal service networking
```

---

## Security and Research Notice

FlowGuard is intended for authorized defensive-security research, learning, benchmarking, and controlled network monitoring.

Only capture, replay, or inspect traffic on systems and networks where you have permission.

Model outputs should be reviewed by a human analyst before being treated as confirmed security incidents.

---

## Current Verified Headline

> **FlowGuard achieved 86.09% accuracy, 98.94% recall, and 0.8767 F1 on 10,000 real capture-day-separated CICIDS2017 flows, while its native XDP parser delivered 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than its C++ userspace parser.**

Library
/
PROJECT 1
/FlowGuard_Detailed_README.md

# FlowGuard

> A full-stack network intrusion detection and traffic-analysis platform built with C++17, native XDP/eBPF, FastAPI, scikit-learn, PyTorch, PyTorch Geometric, PostgreSQL, Redis, Prisma ORM, Docker Compose, and Nginx.

FlowGuard converts raw network packets into flow-level security telemetry, evaluates each flow using multiple machine-learning approaches, and exposes the resulting detections through a REST API and monitoring dashboard.

The project combines three engineering areas:

- **Systems and networking:** C++ packet parsing, multithreading, flow aggregation, libpcap, Linux networking, native XDP/eBPF, BPF maps, and ring buffers.
- **Machine learning:** Random Forest, Isolation Forest, Autoencoder, GraphSAGE, feature engineering, threshold tuning, capture-day-separated evaluation, and ensemble analysis.
- **Backend and infrastructure:** FastAPI, PostgreSQL, Prisma ORM, Redis pub/sub, Docker Compose, Nginx, health checks, persistence, and shadow deployment.

---

## Table of Contents

- [Highlights](#highlights)
- [Verified Results](#verified-results)
- [What FlowGuard Does](#what-flowguard-does)
- [Architecture](#architecture)
- [Project Components](#project-components)
- [Network Features](#network-features)
- [Machine-Learning Models](#machine-learning-models)
- [Dataset and Evaluation Methodology](#dataset-and-evaluation-methodology)
- [Real-Data Model Results](#real-data-model-results)
- [eBPF/XDP Performance Benchmark](#ebpfxdp-performance-benchmark)
- [Live Shadow-Mode Evaluation](#live-shadow-mode-evaluation)
- [Project Layout](#project-layout)
- [Requirements](#requirements)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual C++ Capture Run](#manual-c-capture-run)
- [Manual FastAPI Run](#manual-fastapi-run)
- [eBPF/XDP Build and Run](#ebpfxdp-build-and-run)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Benchmark Reproduction](#benchmark-reproduction)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Generated Artifacts](#generated-artifacts)
- [Docker and Infrastructure Notes](#docker-and-infrastructure-notes)
- [Design Decisions](#design-decisions)
- [Limitations and Honest Interpretation](#limitations-and-honest-interpretation)
- [Roadmap](#roadmap)
- [Resume-Ready Summary](#resume-ready-summary)
- [Technology Keywords](#technology-keywords)

---

## Highlights

- Multithreaded **C++17/libpcap** packet-to-flow processing pipeline.
- Ethernet, IPv4, TCP, UDP, and ICMP parsing.
- Bounded producer-consumer queue with backpressure.
- Five-tuple flow aggregation and TCP flag statistics.
- Native **XDP/eBPF** packet parsing and early filtering.
- Kernel-to-userspace communication through a BPF ring buffer.
- FastAPI inference service with batch analysis and alert persistence.
- PostgreSQL-backed alert storage through Prisma ORM.
- Redis-based internal messaging/pub-sub support.
- Random Forest, Isolation Forest, PyTorch Autoencoder, and GraphSAGE.
- Real CICIDS2017 training and capture-day-separated final evaluation.
- Validation-selected Random Forest operating thresholds.
- Shadow deployment and legacy-versus-real model comparison.
- Reproducible C++ versus XDP performance benchmark.
- Docker Compose orchestration for the complete local stack.

---

## Verified Results

### Real-data intrusion-detection result

The strongest individual model was Random Forest:

| Metric | Result |
|---|---:|
| Test flows | 10,000 |
| Benign flows | 5,000 |
| Attack flows | 5,000 |
| Accuracy | **86.09%** |
| Precision | **78.71%** |
| Recall | **98.94%** |
| F1 score | **0.8767** |
| ROC-AUC | **0.9036** |
| False positives | 1,338 |
| False negatives | 53 |

The test data was separated by capture day from the training and validation data.

### Native XDP/eBPF performance result

| Metric | C++ userspace parser | Native XDP/eBPF parser |
|---|---:|---:|
| Processing cost | 108.456 ns/packet | **62.301 ns/packet** |
| Equivalent throughput | 9.07 million packets/s | **16.05 million packets/s** |
| Processing-cost reduction | — | **42.6%** |
| Equivalent-throughput improvement | — | **1.77×** |
| Sustained complete replay path | — | 316,330 packets/s |
| Observed packet loss | — | approximately 0% |

The XDP benchmark used seven measured runs and approximately 1.46 million replayed packets per run.

### Four-model ensemble result

The strict four-model ensemble prioritized agreement and reduced false alarms:

| Metric | Result |
|---|---:|
| Accuracy | 84.71% |
| Precision | **86.96%** |
| Recall | 81.66% |
| F1 score | 0.8423 |
| False positives | 612 |
| False negatives | 917 |
| False-positive reduction vs Random Forest | **54.3%** |

The ensemble improved precision and reduced false positives, but it also missed more attacks. Random Forest therefore remains the strongest general headline model.

---

## What FlowGuard Does

FlowGuard implements the following pipeline:

1. Read packets from a PCAP file or inspect live ingress traffic.
2. Validate Ethernet and IPv4 headers.
3. Parse TCP, UDP, ICMP, ports, lengths, timestamps, and TCP flags.
4. Convert packets into a structured `PacketInfo` representation.
5. Group packets into flows using a network five-tuple.
6. Calculate duration, traffic volume, rate, and TCP-behaviour features.
7. Emit completed flows as JSON Lines.
8. Load the flows into a FastAPI inference service.
9. Score each flow with one or more detection models.
10. Compare model decisions in shadow mode.
11. Optionally persist alerts in PostgreSQL.
12. Expose flows, alerts, metrics, and health state through REST endpoints.
13. Display operational data through an Nginx-served dashboard.

---

## Architecture

```text
                         ┌──────────────────────────────┐
                         │ PCAP replay or live traffic  │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ C++17/libpcap capture  │              │ Native XDP/eBPF path   │
        │ Userspace packet path  │              │ Kernel ingress path    │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ PacketParser           │              │ BPF maps / ring buffer │
        │ Ethernet/IP/TCP/UDP    │              │ pass/drop/event output │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     └───────────────────┬───────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Five-tuple aggregation │
                            │ Packet/byte/TCP stats  │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ JSONL feature pipeline │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ FastAPI ML service     │
                            │ Normalization/scoring  │
                            └────────────┬───────────┘
                                         ▼
          ┌──────────────────────────────────────────────────────────┐
          │ Random Forest │ Isolation Forest │ Autoencoder │ GraphSAGE │
          └──────────────────────────────┬───────────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Shadow comparison /    │
                            │ voting / alert logic   │
                            └────────────┬───────────┘
                                         ▼
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
        ┌────────────────────────┐                  ┌────────────────────────┐
        │ PostgreSQL + Prisma    │                  │ Redis pub/sub          │
        │ Durable alert storage  │                  │ Internal notifications │
        └────────────┬───────────┘                  └────────────┬───────────┘
                     └───────────────────┬───────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Nginx dashboard        │
                            │ Flows/alerts/metrics   │
                            └────────────────────────┘
```

---

## Project Components

### `capture-cpp`

The C++17 layer is responsible for packet parsing and flow aggregation.

Key responsibilities:

- Open PCAP files through libpcap.
- Parse Ethernet and IPv4 packet structure.
- Extract transport protocol and ports.
- Record packet size and nanosecond timestamp representation.
- Extract TCP SYN, ACK, FIN, and RST flags.
- Send parsed packets through a bounded blocking queue.
- Aggregate packets into flows.
- Write completed flow records to JSONL.

Concurrency model:

```text
Capture thread
    │
    ▼
BlockingQueue<PacketInfo>
    │
    ▼
Aggregation thread
```

The bounded queue provides backpressure when aggregation is slower than capture and prevents unrestricted memory growth.

### `capture-ebpf`

The eBPF layer performs packet inspection at the Linux XDP hook.

Implemented concepts:

- Native XDP attachment.
- Safe packet-bound checks required by the eBPF verifier.
- Ethernet and IPv4 parsing.
- Variable-length IPv4 header handling.
- TCP and UDP port extraction.
- Per-source tracking through BPF maps.
- Demonstration early-drop action.
- BPF ring-buffer event transfer.
- libbpf userspace loader.
- Signal-based cleanup and XDP detach.
- Dedicated silent benchmark program.

### `ml-service`

The Python service provides:

- Flow normalization.
- Feature generation.
- Saved-model loading.
- Legacy ensemble inference.
- Real-data Random Forest inference.
- Operational-threshold selection.
- Shadow-mode scoring.
- Side-by-side model comparison.
- Optional alert persistence.
- Alert lookup.
- Model metric reporting.
- OpenAPI documentation.

### `dashboard`

The verified dashboard is a static HTML/CSS/JavaScript interface served by Nginx.

It is intended to display:

- Recent network flows.
- Detected anomalies.
- Persisted alerts.
- Model and system metrics.
- Basic operational health.

### `docker-compose.yml`

The local stack contains:

- PostgreSQL 16
- Redis 7
- C++ capture service
- FastAPI ML service
- Nginx dashboard

PostgreSQL and Redis are kept inside the Compose network and are not intentionally exposed through host ports.

---

## Network Features

The real-data model pipeline uses 11 flow-level features:

| Feature | Meaning |
|---|---|
| `duration_seconds` | Time between first and last packet |
| `packet_count` | Number of packets in the flow |
| `total_bytes` | Total transferred bytes |
| `bytes_per_sec` | Byte-transfer rate |
| `packets_per_sec` | Packet rate |
| `syn_count` | TCP SYN flags observed |
| `ack_count` | TCP ACK flags observed |
| `fin_count` | TCP FIN flags observed |
| `rst_count` | TCP RST flags observed |
| `syn_ack_ratio` | SYN count relative to ACK activity |
| `rst_ratio` | RST count relative to packet count |

Derived features:

```text
bytes_per_sec   = total_bytes / duration_seconds
packets_per_sec = packet_count / duration_seconds
syn_ack_ratio   = syn_count / (ack_count + 1)
rst_ratio       = rst_count / (packet_count + 1)
```

Zero-duration flows are handled safely to avoid division by zero.

---

## Machine-Learning Models

### Random Forest

A supervised binary attack classifier trained on labelled benign and malicious traffic.

Strengths:

- Best overall real-data F1 score.
- Very high attack recall.
- Direct attack-probability output.
- Feature-importance support.
- Fast CPU inference.

### Isolation Forest

An unsupervised anomaly detector trained on benign traffic.

Strengths:

- Does not require attack labels during fitting.
- Detects outliers that differ from normal behaviour.
- Provides an independent anomaly signal.

Observed limitation:

- Very high recall but excessive false positives on the final real-data test split.

### PyTorch Autoencoder

A neural anomaly detector trained to reconstruct benign feature vectors.

Detection principle:

```text
low reconstruction error  → resembles learned benign behaviour
high reconstruction error → possible anomaly
```

The reconstruction threshold is selected from validation behaviour.

### GraphSAGE

A graph neural network implemented with PyTorch Geometric.

For the real CICIDS2017 experiment:

- Each flow is represented as a node.
- Similar flows are connected through feature-space proximity.
- GraphSAGE aggregates neighbourhood information.
- The correct description is a **flow-similarity graph model**.

The CICIDS2017 CSV files used in this experiment did not provide source and destination IP columns, so this model must not be described as a host-communication graph.

### Legacy three-model ensemble

The original project path combines:

- Isolation Forest
- Random Forest
- Autoencoder

An anomaly is raised when at least two of the three models agree.

This path belongs to the earlier prototype/held-out evaluation.

### Real-data four-model ensemble

The research evaluation combines:

- Random Forest
- Isolation Forest
- Autoencoder
- GraphSAGE

The evaluated strict agreement rule reduced false positives but caused a substantial recall drop.

---

## Dataset and Evaluation Methodology

### CICIDS2017 data

Total labelled records available locally:

| Category | Count |
|---|---:|
| Total | 2,830,743 |
| Benign | 2,273,097 |
| Attack | 557,646 |

Attack families represented in the source collection include:

- DDoS
- PortScan
- Bot
- FTP-Patator
- SSH-Patator
- DoS Hulk
- DoS GoldenEye
- DoS Slowhttptest
- DoS slowloris
- Heartbleed
- Web Attack — Brute Force
- Web Attack — XSS
- Web Attack — SQL Injection
- Infiltration

### Capture-day-separated splits

Instead of randomly mixing rows from the same capture files, FlowGuard separates the data by collection day:

| Split | Capture days | Benign | Attack | Total |
|---|---|---:|---:|---:|
| Training | Monday–Wednesday | 10,000 | 10,000 | 20,000 |
| Validation | Thursday | 2,000 | 2,000 | 4,000 |
| Final test | Friday | 5,000 | 5,000 | 10,000 |

The validation set is used for threshold selection. The Friday test split remains untouched until final evaluation.

### Why day separation matters

Random row splitting can produce overly optimistic results when nearly identical flows from the same capture occur in both training and test data.

Day-separated evaluation provides a more difficult test of:

- Cross-day generalization.
- Traffic-distribution changes.
- Previously unseen or sparsely represented attack families.
- Threshold robustness.
- Resistance to train-test leakage.

---

## Real-Data Model Results

### Binary classification metrics

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Isolation Forest | 62.51% | 57.21% | 99.26% | 72.59% |
| Random Forest | **86.09%** | 78.71% | **98.94%** | **87.67%** |
| Autoencoder | 75.86% | 73.11% | 81.80% | 77.21% |
| GraphSAGE | 55.39% | 52.85% | 99.88% | 69.13% |
| Strict four-model ensemble | 84.71% | **86.96%** | 81.66% | 84.23% |

Random Forest ROC-AUC:

```text
0.9036
```

### Confusion matrices

Format:

```text
[[true negatives, false positives],
 [false negatives, true positives]]
```

Random Forest:

```text
[[3662, 1338],
 [  53, 4947]]
```

Strict four-model ensemble:

```text
[[4388,  612],
 [ 917, 4083]]
```

### Operational trade-off

Compared with Random Forest, the ensemble:

- Reduced false positives from 1,338 to 612.
- Reduced false positives by 54.3%.
- Increased precision from 78.71% to 86.96%.
- Increased false negatives from 53 to 917.
- Reduced attack recall from 98.94% to 81.66%.

The ensemble is useful when false alarms are especially expensive, but Random Forest is the stronger general detector.

### Per-family ensemble recall

| Attack family | Recall | Test flows |
|---|---:|---:|
| DDoS | 84.99% | 2,152 |
| PortScan | 80.35% | 2,804 |
| Bot | 2.27% | 44 |

Bot recall was poor because the final sampling included few Bot flows and the training-day attack data did not provide equivalent Bot coverage.

---

## eBPF/XDP Performance Benchmark

### Workload

- PCAP: infected-Android traffic capture.
- PCAP size: approximately 24 MB.
- Packets per PCAP loop: 29,125.
- XDP replay loops per measured run: 50.
- Expected packets per measured run: 1,456,250.
- Measured runs: 7.
- XDP attachment mode: native.
- C++ build: Release mode with `-O3`.
- XDP benchmark: silent parser using a per-CPU map.
- Runtime measurement: kernel BPF program statistics through `bpftool`.

### Median C++ result

```text
C++ median CPU cost:          108.456 ns/packet
C++ median wall cost:         110.278 ns/packet
C++ equivalent throughput:    9,067,963 packets/s
```

### Median native-XDP result

```text
XDP median kernel cost:       62.301 ns/packet
XDP equivalent throughput:    16,051,175 packets/s
XDP sustained replay rate:    316,330 packets/s
XDP observed packet loss:     approximately 0%
```

### Improvement

```text
Processing-cost speedup:      1.74×
Equivalent-throughput gain:   1.77×
Processing-cost reduction:    42.6%
Equivalent-throughput rise:   approximately 77%
```

### Interpretation

The 16.05 million packets/s result is equivalent throughput calculated from measured kernel execution time.

The 316,330 packets/s result measures the complete replay path:

```text
PCAP
  → tcpreplay
  → virtual Ethernet pair
  → Linux ingress path
  → native XDP program
```

The complete replay rate includes replay generation, veth, scheduling, and other kernel overhead. It should not be described as the XDP parser's maximum theoretical capacity.

A measured delivery rate slightly above 100% was caused by a few additional control/interface packets. It is reported as approximately 100% delivery and approximately 0% loss.

---

## Live Shadow-Mode Evaluation

The selected real-data Random Forest is integrated into FastAPI without replacing the legacy alert pipeline.

### Real-model health example

```json
{
  "status": "ok",
  "model": "real_only_random_forest",
  "threshold": 0.0235,
  "operational_mode": "balanced",
  "flow_file": "data/flows_output.jsonl",
  "mode": "shadow"
}
```

### Operational mode

Select the threshold configuration through:

```bash
RF_OPERATIONAL_MODE=balanced
```

The balanced threshold was selected on the Thursday validation split.

### Model-comparison endpoint

The comparison route runs the legacy ensemble and real-data Random Forest on the same recent flows without writing alerts.

Verified comparison over 100 flows:

| Metric | Result |
|---|---:|
| Analyzed | 100 |
| Errors | 0 |
| Legacy alerts | 85 |
| Real Random Forest alerts | 100 |
| Both alert | 85 |
| Both benign | 0 |
| Legacy only | 0 |
| Real Random Forest only | 15 |
| Agreement | 85% |

The 15 disagreements shared a repeated inbound TCP/source-port-8080 pattern.

These live flows did not contain ground-truth labels. Therefore, the results show model disagreement and alert volume—not verified attacks or live accuracy.

---

## Historical Prototype Result

The earlier synthetic/held-out prototype used 940 rows:

- 830 benign
- 110 attacks

The legacy 2-of-3 ensemble achieved:

| Metric | Result |
|---|---:|
| Accuracy | 98.94% |
| Precision | 96.30% |
| Recall | 94.55% |
| F1 | 95.41% |
| False positives | 4 |
| False negatives | 6 |

This result is retained for project history and regression comparison. It is not the main real-data headline.

---

## Project Layout

Representative layout:

```text
flowguard/
├── capture-cpp/
│   ├── include/
│   │   ├── BlockingQueue.hpp
│   │   ├── FeatureEmitter.hpp
│   │   ├── FlowAggregator.hpp
│   │   ├── FlowKey.hpp
│   │   ├── FlowStats.hpp
│   │   ├── JsonSerializer.hpp
│   │   ├── PacketInfo.hpp
│   │   └── PacketParser.hpp
│   ├── src/
│   │   ├── main.cpp
│   │   ├── PacketParser.cpp
│   │   ├── FlowAggregator.cpp
│   │   ├── FeatureEmitter.cpp
│   │   ├── JsonSerializer.cpp
│   │   ├── benchmark.cpp
│   │   └── parser_benchmark.cpp
│   ├── tests/
│   ├── CMakeLists.txt
│   └── Dockerfile
├── capture-ebpf/
│   ├── xdp_filter.bpf.c
│   ├── xdp_filter.o
│   ├── loader.c
│   ├── loader
│   ├── xdp_parser_benchmark.c
│   └── xdp_parser_benchmark.o
├── ml-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── ml/
│   │   │   ├── ensemble.py
│   │   │   └── real_only_predictor.py
│   │   ├── routes/
│   │   │   └── real_analysis.py
│   │   ├── services/
│   │   └── models/
│   │       └── real_only/
│   ├── data/
│   │   └── real_only/
│   ├── training/
│   │   ├── train_evaluate_real_only.py
│   │   └── tune_real_rf_thresholds.py
│   ├── tests/
│   ├── prisma/
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── index.html
│   └── Dockerfile
├── data/
│   ├── sample/
│   ├── attack_samples/
│   ├── cicids2017/
│   └── flows_output.jsonl
├── docs/
│   ├── cpp_parser_benchmark.txt
│   ├── ebpf_vs_cpp_runs.csv
│   ├── ebpf_vs_cpp_benchmark.json
│   ├── ebpf_vs_cpp_benchmark.md
│   └── model_comparison.json
├── scripts/
│   └── benchmark_ebpf_vs_cpp.sh
├── docker-compose.yml
├── HOW_TO_RUN.md
└── README.md
```

Some generated datasets, model artifacts, PCAPs, and build outputs may be intentionally excluded from Git.

---

## Requirements

### General

- Linux
- Git
- Docker and Docker Compose
- Python 3
- CMake
- A C++17 compiler

### C++ capture

- libpcap
- pthread support

### eBPF/XDP

- Linux kernel with eBPF and XDP support
- Clang/LLVM
- libbpf and development headers
- bpftool
- Linux networking tools (`ip`)
- Root privileges for loading and attaching XDP programs

### Benchmarking

- tcpreplay
- tcpdump
- Python 3
- `kernel.bpf_stats_enabled` support

---

## Quick Start with Docker Compose

From the repository root:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Expected services:

```text
postgres
redis
capture
ml-service
dashboard
```

Check the API:

```bash
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/flows/recent?limit=2"
```

Open:

- Dashboard: `http://127.0.0.1:8080`
- OpenAPI documentation: `http://127.0.0.1:8000/docs`

View logs:

```bash
docker compose logs -f ml-service
```

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

---

## Manual C++ Capture Run

### Configure and compile

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

### Process a PCAP

```bash
./capture-cpp/build/flowguard_capture \
  data/sample/small_sample.pcap \
  data/flows_output.jsonl
```

### Inspect output

```bash
head -n 5 data/flows_output.jsonl
```

Each line represents one aggregated flow.

---

## Manual FastAPI Run

From the repository root:

```bash
cd ml-service
source .venv/bin/activate
```

Run the selected real-data operating mode:

```bash
RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Using `python -m uvicorn` avoids relying on a globally installed `uvicorn` command.

Check the service:

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

Check the real model:

```bash
curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
```

Run shadow inference:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool
```

Compare detectors:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  | python -m json.tool
```

---

## eBPF/XDP Build and Run

### Compile the XDP program

From the repository root:

```bash
clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_filter.bpf.c \
  -o capture-ebpf/xdp_filter.o
```

Verify the object:

```bash
file capture-ebpf/xdp_filter.o
```

Expected type:

```text
ELF 64-bit LSB relocatable, eBPF
```

### Compile the userspace loader

```bash
cc \
  -O2 \
  -g \
  capture-ebpf/loader.c \
  -o capture-ebpf/loader \
  $(pkg-config --cflags --libs libbpf)
```

### Attach to an interface

First identify the interface:

```bash
ip -br link
```

Then run the loader from the directory containing `xdp_filter.o`:

```bash
cd capture-ebpf
sudo ./loader wlan0
```

Replace `wlan0` with the correct interface.

Press `Ctrl+C` to stop the loader and detach the XDP program.

### Warning

The demonstration packet threshold in `xdp_filter.bpf.c` counts packets over the lifetime of the BPF map entry. It is not a time-windowed packets-per-second production rate limiter.

---

## Model Training and Evaluation

### Expected real-data locations

```text
data/cicids2017/
ml-service/data/real_only/
```

### Real-only training/evaluation

From `ml-service`:

```bash
PYTHONPATH=. \
.venv/bin/python \
training/train_evaluate_real_only.py
```

### Operational-threshold tuning

```bash
PYTHONPATH=. \
.venv/bin/python \
training/tune_real_rf_thresholds.py
```

Generated real-model artifacts are stored under:

```text
ml-service/app/models/real_only/
```

Expected artifacts include:

```text
random_forest.joblib
supervised_scaler.joblib
isolation_forest.joblib
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
thresholds.json
rf_operational_thresholds.json
```

### Important reproducibility note

Do not select thresholds using the final Friday test set. The project uses Thursday validation data for threshold selection and Friday data only for final evaluation.

---

## Benchmark Reproduction

### C++ parser benchmark

```bash
./capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
```

### Full XDP versus C++ benchmark

```bash
chmod +x scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh
```

The script:

- Enables BPF runtime statistics temporarily.
- Creates a temporary veth pair.
- Loads and pins the benchmark XDP program.
- Attaches it in native mode when supported.
- Replays the PCAP multiple times.
- Reads BPF runtime and packet counters.
- Calculates median metrics.
- Writes CSV, JSON, and Markdown reports.
- Detaches XDP and removes the temporary interfaces.

Generated output:

```text
docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
```

The benchmark requires `sudo`.

---

## API Reference

### Health

```http
GET /health
```

Basic API health check.

### Recent flows

```http
GET /flows/recent?limit=20
```

Returns the most recent captured flow records.

### Legacy batch analysis

```http
POST /analyze?offset=0&limit=100&persist=false
```

Parameters:

| Parameter | Meaning |
|---|---|
| `offset` | Starting flow index |
| `limit` | Batch size, up to 1,000 |
| `persist` | Save detected anomalies to PostgreSQL |

Use `persist=false` while validating behaviour.

### Alerts

```http
GET /alerts
GET /alerts/{alert_id}
```

Retrieves persisted alerts.

### Historical model metrics

```http
GET /metrics/model
```

Returns the historical held-out prototype metrics. This endpoint does not represent the final real-only Random Forest evaluation.

### Real-data model health

```http
GET /real-model/health
```

Returns:

- Model identifier
- Selected operational threshold
- Operational mode
- Resolved flow file
- Shadow-mode state

### Real-data shadow analysis

```http
POST /real-model/analyze?limit=50
```

Scores recent flows with the real-only Random Forest.

It does not persist alerts.

### Detector comparison

```http
POST /analyze/compare?limit=100
```

Runs the legacy ensemble and real Random Forest on the same recent flows.

Returns:

- Alert totals
- Agreement categories
- Agreement rate
- Real Random Forest probabilities
- Per-flow disagreement information
- Error details

The comparison route never persists alerts.

### Legacy real-capture route

```http
POST /analyse/real
```

This older experimental route is retained for compatibility. Prefer the `/real-model/*` routes for current shadow evaluation.

---

## Testing

### Python tests

```bash
cd ml-service

PYTHONPATH=. \
.venv/bin/python \
-m pytest tests -q
```

Previously verified result:

```text
8 passed
```

Re-run the suite after modifying inference routes or model-loading code.

### C++ tests

Configure and build:

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Debug

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

Run registered tests:

```bash
ctest \
  --test-dir capture-cpp/build \
  --output-on-failure
```

C++ test targets cover areas such as:

- Flow key ordering
- Flow aggregation
- Blocking queue behaviour
- Packet parsing
- JSON serialization

### Syntax checks

Python:

```bash
python -m py_compile \
  ml-service/app/main.py \
  ml-service/app/ml/real_only_predictor.py \
  ml-service/app/routes/real_analysis.py
```

Bash:

```bash
bash -n scripts/benchmark_ebpf_vs_cpp.sh
```

---

## Generated Artifacts

### Model artifacts

```text
ml-service/app/models/real_only/
├── anomaly_scaler.joblib
├── autoencoder.pt
├── graphsage_flow_similarity.pt
├── isolation_forest.joblib
├── random_forest.joblib
├── rf_operational_thresholds.json
├── supervised_scaler.joblib
└── thresholds.json
```

### Evaluation artifacts

```text
docs/
├── cpp_parser_benchmark.txt
├── ebpf_vs_cpp_runs.csv
├── ebpf_vs_cpp_benchmark.json
├── ebpf_vs_cpp_benchmark.md
├── model_comparison.json
└── rf_threshold_tuning.txt
```

### Prepared real-data splits

```text
ml-service/data/real_only/
├── train_real.csv
├── validation_real.csv
└── test_real.csv
```

Large datasets, model files, PCAPs, and generated build files may need Git LFS or external storage rather than ordinary Git commits.

---

## Docker and Infrastructure Notes

### PostgreSQL

PostgreSQL provides durable alert storage.

The Compose configuration uses:

```text
database: flowguard
user: flowguard_user
```

Credentials in the development Compose file are for local use only and must be replaced for deployment.

### Prisma ORM

Prisma provides schema-driven database access.

The ML container startup performs:

1. Wait for PostgreSQL.
2. Wait for Redis.
3. Run `prisma db push`.
4. Run `prisma generate`.
5. Start Uvicorn.

### Redis

Redis is used inside the Compose network for messaging/pub-sub support.

It is not intentionally exposed to the host.

### Capture permissions

The capture container receives:

```text
NET_ADMIN
NET_RAW
```

These capabilities are required for packet-capture and networking operations but should be minimized in production.

### ML image

The ML image installs CPU-only PyTorch packages to avoid pulling unnecessary GPU/CUDA layers for the local CPU inference workflow.

### Dashboard image

The verified dashboard container serves the static dashboard through Nginx.

---

## Design Decisions

### JSONL between C++ and Python

JSON Lines was selected because it is:

- Human-readable.
- Append-friendly.
- Easy to debug with standard shell tools.
- Supported directly by Python.
- Independent of the C++ process lifetime.
- Suitable for replay and offline evaluation.

### Bounded queue instead of an unbounded queue

A bounded queue prevents the capture thread from consuming unlimited memory if the aggregation thread cannot keep pace.

### Model loading at startup

Saved models are loaded once when the API process starts rather than once per request. This reduces inference latency and avoids repeated disk deserialization.

### Shadow deployment

The real-data model does not immediately replace or persist into the existing alert path.

Shadow deployment allows FlowGuard to measure:

- Alert volume.
- Model disagreement.
- Probability distribution.
- Feature-semantic mismatch.
- Domain shift.
- Runtime errors.

### Day-separated evaluation

Capture-day separation was selected to reduce leakage and make the model prove that it can generalize beyond the exact capture distribution used for fitting.

### Median benchmark reporting

Performance results use medians across repeated runs to reduce sensitivity to scheduler noise and occasional outliers.

---

## Limitations and Honest Interpretation

FlowGuard is an engineering and research project, not a production-certified intrusion-detection appliance.

### Live predictions are not ground truth

A live model label of `ATTACK` is a prediction, not confirmation of malicious activity.

Accuracy, precision, and recall require labelled data.

### High live alert rate indicates possible domain shift

The real-only Random Forest produced a high alert rate on the infected-host capture. This can reflect:

- Truly unusual traffic.
- Different feature semantics.
- Dataset-to-live distribution shift.
- Poor probability calibration.
- Incomplete flow reconstruction.

It must not be described as a verified attack rate.

### Balanced final test set

The final test set intentionally contains equal benign and attack counts.

This makes model comparison clear but does not represent the natural attack prevalence of most real networks.

### GraphSAGE limitations

The GraphSAGE model had extremely high recall but very poor benign classification.

It demonstrates graph-learning implementation but requires:

- Better graph construction.
- Calibration.
- Class weighting.
- Additional validation.
- More representative graph data.

### Infected-Android PCAP labels

The infected-Android PCAP does not provide per-flow ground-truth labels.

It is valid for:

- Systems benchmarking.
- Replay.
- End-to-end testing.
- Shadow inference.
- Disagreement analysis.

It is not valid for reporting classification accuracy.

### eBPF benchmark scope

The benchmark compares implemented parser-level cost.

It does not include:

- Flow aggregation parity.
- Machine-learning inference.
- PostgreSQL persistence.
- Redis publication.
- Dashboard latency.
- Complete packet-to-alert latency.

### Demonstration drop threshold

The original XDP source counter is lifetime-based. Production rate limiting requires a time-windowed policy.

---

## Roadmap

### Detection quality

- Probability calibration using isotonic regression or Platt scaling.
- Evaluation on naturally imbalanced traffic.
- Precision-recall curves and confidence intervals.
- Leave-one-attack-family-out testing.
- Better Bot-family coverage.
- Weighted voting or stacking instead of strict agreement.
- Incident-level alert grouping.
- Feature-semantic alignment between C++ flows and CICIDS flow generation.

### Graph learning

- True IP host-communication graphs.
- Temporal graph construction.
- Class-weighted GraphSAGE loss.
- Focal loss.
- Graph mini-batching.
- Validation-based early stopping.
- Neighbourhood and edge-feature ablation studies.

### eBPF/XDP

- Time-windowed packet-rate limiting.
- Production per-CPU counters.
- Ring-buffer loss counters.
- IPv6 parsing.
- VLAN support.
- AF_XDP experiment.
- Multi-core scaling benchmark.
- Physical-NIC benchmark.
- Packet-to-alert latency measurement.

### Backend and operations

- Prometheus metrics.
- Grafana dashboards.
- Authentication and role-based access.
- Model registry and rollback.
- Alert deduplication.
- Deployment-specific secrets.
- CI for Python, C++, Docker, and eBPF verifier checks.
- Structured logging and tracing.

---

## Resume-Ready Summary

### Detailed version

> Built FlowGuard, a full-stack network intrusion detection platform using C++17/libpcap, native XDP/eBPF, FastAPI, PostgreSQL, Redis, Prisma ORM, and Docker Compose. Trained Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE on capture-day-separated CICIDS2017 data; Random Forest achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 on 10,000 real labelled flows. Benchmarked native XDP across seven runs and approximately 1.46 million packets per run, achieving 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than the C++ userspace parser.

### Compact bullets

- Built a C++17/Python network intrusion detection pipeline using libpcap, native XDP/eBPF, five-tuple flow aggregation, FastAPI, PostgreSQL, Redis, and Docker Compose.
- Achieved **86.09% accuracy, 98.94% recall, and 0.8767 F1** with Random Forest on **10,000 real capture-day-separated CICIDS2017 flows**.
- Reduced Random Forest false positives by **54.3%** with a strict four-model ensemble, improving precision to **86.96%** while documenting the recall trade-off.
- Benchmarked native XDP at **62.3 ns/packet and 16.05M equivalent packets/s**, delivering **1.77× higher equivalent throughput** than the C++ parser.

---

## Technology Keywords

### Languages and systems

```text
C++17, C, Python, SQL, Bash, JavaScript, Linux, systems programming,
multithreading, producer-consumer, bounded queue, backpressure, mutex,
condition variable, atomic state, kernel programming
```

### Networking

```text
libpcap, PCAP, tcpreplay, Ethernet, IPv4, TCP, UDP, ICMP, five-tuple,
flow aggregation, TCP flags, packet parsing, network telemetry,
network intrusion detection, NIDS, DDoS, PortScan, Bot detection
```

### eBPF/XDP

```text
eBPF, XDP, native XDP, libbpf, bpftool, BPF maps, per-CPU maps,
ring buffer, kernel-space packet processing, packet filtering,
nanoseconds per packet, packets per second
```

### Machine learning

```text
scikit-learn, PyTorch, PyTorch Geometric, Random Forest,
Isolation Forest, Autoencoder, GraphSAGE, GNN, anomaly detection,
supervised learning, unsupervised learning, feature engineering,
threshold tuning, ensemble learning, ROC-AUC, precision, recall,
F1 score, confusion matrix, domain shift, data leakage,
capture-day separation, model generalization, shadow deployment
```

### Backend and DevOps

```text
FastAPI, REST API, Uvicorn, PostgreSQL, Prisma ORM, Redis, pub/sub,
Docker, Docker Compose, Nginx, CMake, Clang, health checks,
model serving, persistent storage, internal service networking
```

---

## Security and Research Notice

FlowGuard is intended for authorized defensive-security research, learning, benchmarking, and controlled network monitoring.

Only capture, replay, or inspect traffic on systems and networks where you have permission.

Model outputs should be reviewed by a human analyst before being treated as confirmed security incidents.

---

## Current Verified Headline

> **FlowGuard achieved 86.09% accuracy, 98.94% recall, and 0.8767 F1 on 10,000 real capture-day-separated CICIDS2017 flows, while its native XDP parser delivered 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than its C++ userspace parser.**
