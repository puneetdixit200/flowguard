# FlowGuard eBPF/XDP vs C++ Parser Benchmark

## Workload

- PCAP packets: 29,125
- PCAP loops per eBPF run: 50
- Measured runs: 7
- XDP attachment mode: `native`

## Median results

| Metric | C++ parser | eBPF/XDP parser |
|---|---:|---:|
| Processing cost | 108.456 ns/packet | 62.301 ns/packet |
| Equivalent throughput | 9,067,963 packets/s | 16,051,175 packets/s |
| Sustained replay throughput | Not measured | 316,330 packets/s |
| Packet delivery | Not applicable | 100.0001% |
| Packet loss | Not applicable | 0.0000% |

## Comparison

- eBPF processing-cost speedup: **1.74×**
- Equivalent-throughput speedup: **1.77×**
- Kernel processing-cost reduction: **42.56%**

## Interpretation

The processing-cost comparison measures the average runtime of the
XDP parser in the kernel against the measured CPU cost of the C++
userspace packet parser.

The sustained replay value measures the complete test path, including
tcpreplay, the virtual Ethernet pair, kernel scheduling and XDP.

These metrics do not include FlowGuard ML inference or database work.
