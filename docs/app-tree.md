# FlowGuard App Tree

This document shows the current application structure as of Friday, July 17,
2026, with a short comment on what each major file or directory does.

To keep this readable, very large generated directories such as
`ml-service/.venv/` and `capture-cpp/build/` are summarized instead of expanded
line by line.

## Repository Tree

```text
flowguard/
├── .gitignore                          # Root ignore rules
├── docker-compose.yml                  # Main local stack: Postgres, Redis, capture, API, dashboard
├── README.md                           # High-level project overview and verified run path
├── HOW_TO_RUN.md                       # Detailed runbook for Docker and manual execution
│
├── data/                               # Shared runtime/sample data at repo level
│   ├── flows_output.jsonl              # Captured flow records consumed by the API
│   └── sample/
│       ├── real_attack.pcap            # Real attack capture sample
│       └── small_sample.pcap           # Small demo capture for local testing
│
├── dashboard/                          # Frontend UI served as static HTML
│   ├── Dockerfile                      # Nginx image that serves the dashboard
│   ├── index.html                      # Main shipped dashboard page
│   └── src/                            # Partial React-style source kept in repo
│       ├── App.jsx                     # Top-level dashboard app component
│       ├── api.js                      # Browser-side API helpers
│       ├── components/
│       │   ├── AlertFeed.jsx           # Alert list / feed component
│       │   ├── GnnGraphView.jsx        # Graph visualization component
│       │   └── StatusStrip.jsx         # Service/status summary UI
│       └── hooks/
│           └── useLiveAlerts.js        # Hook for live alert updates
│
├── capture-cpp/                        # C++ packet capture and flow aggregation service
│   ├── .dockerignore                   # Keeps build artifacts out of Docker context
│   ├── CMakeLists.txt                  # CMake build definition
│   ├── Dockerfile                      # Container build for the capture binary
│   ├── include/                        # Public headers for capture pipeline pieces
│   │   ├── BlockingQueue.hpp           # Thread-safe queue used by worker pipeline
│   │   ├── FeatureEmitter.hpp          # Emits normalized features/flow output
│   │   ├── FlowAggregator.hpp          # Aggregates packets into flow records
│   │   ├── FlowKey.hpp                 # Hashable flow identity key
│   │   ├── FlowStats.hpp               # Per-flow metrics data structure
│   │   ├── JsonSerializer.hpp          # Writes flow records as JSON/JSONL
│   │   ├── PacketInfo.hpp              # Parsed packet metadata structure
│   │   └── PacketParser.hpp            # Packet decode/parsing interface
│   ├── src/
│   │   ├── FeatureEmitter.cpp          # Feature output implementation
│   │   ├── FlowAggregator.cpp          # Flow aggregation logic
│   │   ├── JsonSerializer.cpp          # JSON serialization logic
│   │   ├── PacketParser.cpp            # Packet parsing implementation
│   │   └── main.cpp                    # Capture process entrypoint
│   ├── tests/
│   │   ├── test_blocking_queue.cpp     # Unit tests for queue behavior
│   │   ├── test_flow_aggregator.cpp    # Unit tests for flow aggregation
│   │   └── test_flow_key.cpp           # Unit tests for flow key semantics
│   └── build/                          # Generated CMake build output and binaries
│       ├── flowguard_capture           # Built capture executable
│       ├── test_blocking_queue         # Built queue test binary
│       ├── test_flow_aggregator        # Built aggregator test binary
│       ├── test_flow_key               # Built key test binary
│       └── ...                         # Remaining generated CMake metadata/files
│
├── capture-ebpf/                       # Experimental eBPF/XDP capture path
│   ├── loader                          # Built loader artifact
│   ├── loader.c                        # eBPF/XDP loader program
│   ├── xdp_filter.c                    # XDP filter source
│   └── xdp_filter.o                    # Compiled eBPF object
│
├── ml-service/                         # Python ML inference and API service
│   ├── .dockerignore                   # Excludes venv/cache from Docker context
│   ├── .env                            # Local environment variables
│   ├── .gitignore                      # Service-local ignore rules
│   ├── Dockerfile                      # ML service image with CPU-only PyTorch
│   ├── docker-entrypoint.sh            # Waits for DB/cache, syncs Prisma, starts API
│   ├── requirements.txt                # Python dependencies
│   ├── prepare_cicids_data.py          # Shared feature column/data prep helper
│   │
│   ├── app/                            # FastAPI application package
│   │   ├── __init__.py                 # Package marker
│   │   ├── db.py                       # Prisma client factory
│   │   ├── main.py                     # FastAPI routes and API entrypoint
│   │   ├── api/
│   │   │   └── websocket.py            # WebSocket support for live alerts
│   │   ├── ml/
│   │   │   ├── __init__.py             # Package marker
│   │   │   ├── autoencoder_def.py      # PyTorch autoencoder definition
│   │   │   ├── ensemble.py             # Loads saved models and scores flows
│   │   │   ├── gnn_model.py            # GraphSAGE / GNN model definition
│   │   │   └── graph_builder.py        # Converts flows into graph structures
│   │   ├── models/                     # Saved model artifacts used at inference time
│   │   │   ├── autoencoder.pt          # Autoencoder weights
│   │   │   ├── autoencoder_meta.joblib # Autoencoder threshold/input metadata
│   │   │   ├── gnn_graphsage.pt        # Trained GNN weights
│   │   │   ├── gnn_meta.pt             # GNN metadata
│   │   │   ├── isolation_forest.joblib # Trained Isolation Forest
│   │   │   ├── label_encoder.joblib    # Label encoder for RF output classes
│   │   │   ├── random_forest.joblib    # Trained Random Forest
│   │   │   └── scaler.joblib           # Feature scaler shared by models
│   │   ├── services/
│   │   │   ├── __init__.py             # Package marker
│   │   │   ├── alert_service.py        # Creates/reads alerts in Postgres and Redis
│   │   │   ├── detector.py             # Auxiliary detection service logic
│   │   │   ├── feature_normalizer.py   # Converts raw flow JSON into model feature rows
│   │   │   ├── flow_reader.py          # Reads flow JSONL files from known locations
│   │   │   ├── flow_reader.py.bak      # Backup copy of older flow reader logic
│   │   │   ├── gnn_service.py          # Batch/window scoring path for graph model
│   │   │   └── threat_intel_service.py # Looks up IPs in local threat intel data
│   │   └── storage/
│   │       └── redis_client.py         # Redis publish/cache helper
│   │
│   ├── data/                           # ML-service-local datasets and outputs
│   │   ├── flows_output.jsonl          # Alternate local flow output path
│   │   ├── raw/                        # Raw imported training data
│   │   ├── sample/
│   │   │   ├── sample_features.csv     # Generated feature dataset
│   │   │   └── test_holdout.csv        # Held-out evaluation dataset
│   │   └── threat_intel.csv            # Seed threat-intel CSV
│   ├── prisma/
│   │   ├── schema.prisma               # DB schema for Flow, Alert, ThreatIntelEntry
│   │   └── migrations/                 # Generated Prisma migration history
│   ├── tests/
│   │   ├── test_alert_severity.py      # Severity mapping tests
│   │   ├── test_feature_normalizer.py  # Feature normalization tests
│   │   └── test_inference_api.py       # API contract tests
│   ├── training/                       # Offline model training/evaluation scripts
│   │   ├── evaluate_models.py          # Held-out evaluation across all models
│   │   ├── generate_sample_dataset.py  # Builds synthetic/sample dataset
│   │   ├── honest_report.py            # Writes analysis-oriented evaluation notes
│   │   ├── prepare_cicids_data.py      # Training-side feature prep
│   │   ├── train_autoencoder.py        # Trains autoencoder
│   │   ├── train_gnn.py                # Trains GraphSAGE/GNN model
│   │   ├── train_isolation_forest.py   # Trains Isolation Forest
│   │   └── train_random_forest.py      # Trains Random Forest
│   ├── .pytest_cache/                  # Generated pytest cache
│   ├── __pycache__/                    # Generated Python bytecode cache
│   └── .venv/                          # Local virtual environment, intentionally collapsed
│
├── docs/                               # Project documentation
│   ├── app-tree.md                     # This file
│   ├── case-study.md                   # Narrative project write-up
│   ├── evaluation_report.txt           # Saved held-out model evaluation output
│   ├── false-positive-analysis.md      # Discussion of ensemble error cases
│   ├── ml-models.md                    # Model inventory and metrics
│   └── threading-model.md              # Concurrency model for capture pipeline
│
└── .git/                               # Git metadata, intentionally omitted from detail
```

## How The Pieces Fit Together

1. `capture-cpp` parses packet captures and writes aggregated flow JSON.
2. `data/flows_output.jsonl` becomes the main handoff file to the API layer.
3. `ml-service/app/services/feature_normalizer.py` converts each flow into the
   exact feature order expected by the trained models.
4. `ml-service/app/ml/ensemble.py` loads the saved models and scores each flow.
5. `ml-service/app/services/alert_service.py` stores anomalous results in
   PostgreSQL and publishes alert updates to Redis.
6. `dashboard/` displays service state and alert data through the FastAPI API.

## Important Generated Directories

These exist in the repo or local workspace, but they are not core source code:

- `ml-service/.venv/`: local Python environment
- `ml-service/__pycache__/`: Python bytecode cache
- `ml-service/.pytest_cache/`: pytest cache
- `capture-cpp/build/`: generated CMake output and binaries
- `capture-ebpf/xdp_filter.o`: compiled eBPF object
- `capture-ebpf/loader`: built loader artifact

## Recommended Reading Order

If someone is new to the codebase, start here:

1. [README.md](/home/pd/Downloads/flowguard/README.md)
2. [docker-compose.yml](/home/pd/Downloads/flowguard/docker-compose.yml)
3. [ml-service/app/main.py](/home/pd/Downloads/flowguard/ml-service/app/main.py)
4. [ml-service/app/ml/ensemble.py](/home/pd/Downloads/flowguard/ml-service/app/ml/ensemble.py)
5. [capture-cpp/src/main.cpp](/home/pd/Downloads/flowguard/capture-cpp/src/main.cpp)
6. [docs/threading-model.md](/home/pd/Downloads/flowguard/docs/threading-model.md)
