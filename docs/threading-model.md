# Threading Model

Capture Thread (producer)
  - reads packets via libpcap
  - pushes PacketInfo into BlockingQueue

Main/Aggregator Thread (consumer)
  - pops PacketInfo from BlockingQueue
  - updates FlowStats per FlowKey
  - on shutdown, flushes all flows to JSON via FeatureEmitter

Synchronization primitives used:
  - std::mutex          -> protects the shared queue
  - std::condition_variable -> not_empty / not_full signaling
  - bounded queue size   -> prevents unbounded memory growth if capture outpaces aggregation
  - shutdown flag        -> lets producer signal "no more data" so consumer can exit cleanly
