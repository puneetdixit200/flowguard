# FlowGuard Diagrams

Open `flowguard-study-diagrams.drawio` in draw.io / diagrams.net. The file
contains eight editable pages. Each rendered PNG also embeds the Draw.io XML.

Recommended revision order:

1. System Overview: project purpose, users, inputs, outputs, and dependencies.
2. Runtime Architecture: Docker services and runtime handoff points.
3. C++ Capture Components: parser, data types, queue, aggregation, and JSONL output.
4. Capture Threading: producer, bounded queue, consumer, and shutdown behavior.
5. Packet To Alert Flow: intended end-to-end processing sequence.
6. ML Training And Inference: artifacts, legacy ensemble, real-only RF, and comparison mode.
7. API And Dashboard Wiring: what is connected, available, missing, or not mounted.
8. Persistence ERD: Prisma entities, Redis data, and application-level relationships.

## System Overview

![System Overview](system-overview.drawio.png)

## Runtime Architecture

![Runtime Architecture](runtime-architecture.drawio.png)

## C++ Capture Components

![C++ Capture Components](cpp-capture-components.drawio.png)

## Capture Threading

![Capture Threading](capture-threading.drawio.png)

## Packet To Alert Flow

![Packet To Alert Flow](packet-to-alert-flow.drawio.png)

## ML Training And Inference

![ML Training And Inference](ml-training-and-inference.drawio.png)

## API And Dashboard Wiring

![API And Dashboard Wiring](api-dashboard-wiring.drawio.png)

## Persistence ERD

![Persistence ERD](persistence-erd.drawio.png)

Not included:

- Full file tree: already covered in `docs/app-tree.md`.
- Every Python/JavaScript import: too noisy for revision.
- Detailed eBPF internals: experimental and not part of the primary runtime path.
