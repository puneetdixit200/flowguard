#!/usr/bin/env bash

set -Eeuo pipefail


ROOT="/home/pd/Downloads/flowguard"

PCAP="$ROOT/data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap"

CPP_RESULTS="$ROOT/docs/cpp_parser_benchmark.txt"

BPF_OBJECT="$ROOT/capture-ebpf/xdp_parser_benchmark.o"

CSV_OUTPUT="$ROOT/docs/ebpf_vs_cpp_runs.csv"
JSON_OUTPUT="$ROOT/docs/ebpf_vs_cpp_benchmark.json"
MARKDOWN_OUTPUT="$ROOT/docs/ebpf_vs_cpp_benchmark.md"

LOG_DIRECTORY="$ROOT/docs/benchmark-logs"

TX_INTERFACE="fgbench_tx"
RX_INTERFACE="fgbench_rx"

PIN_PATH="/sys/fs/bpf/flowguard_xdp_parser_benchmark"

RUNS=7
PCAP_LOOPS=50

ATTACH_MODE="unknown"

OLD_BPF_STATS="$(
    cat /proc/sys/kernel/bpf_stats_enabled
)"


cleanup()
{
    set +e

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdp off \
        >/dev/null 2>&1

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdpgeneric off \
        >/dev/null 2>&1

    sudo rm -f "$PIN_PATH"

    sudo ip link delete \
        "$TX_INTERFACE" \
        >/dev/null 2>&1

    sudo sysctl -q -w \
        kernel.bpf_stats_enabled="$OLD_BPF_STATS" \
        >/dev/null 2>&1
}


trap cleanup EXIT


read_program_stats()
{
    sudo bpftool -j prog show pinned "$PIN_PATH" |
        python -c '
import json
import sys

data = json.load(sys.stdin)

if isinstance(data, list):
    data = data[0]

print(
    int(data.get("run_time_ns", 0)),
    int(data.get("run_cnt", 0)),
)
'
}


mkdir -p "$LOG_DIRECTORY"

for required_file in \
    "$PCAP" \
    "$CPP_RESULTS" \
    "$BPF_OBJECT"
do
    if [[ ! -f "$required_file" ]]; then
        echo "Missing required file: $required_file" >&2
        exit 1
    fi
done


for required_command in \
    bpftool \
    clang \
    ip \
    python \
    tcpreplay
do
    if ! command -v "$required_command" >/dev/null 2>&1; then
        echo "Missing command: $required_command" >&2
        exit 1
    fi
done


CPP_TOTAL_PACKETS="$(
    awk -F= '
        /^CPP_TOTAL_PACKETS=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_CPU_NS="$(
    awk -F= '
        /^CPP_MEDIAN_CPU_NS_PER_PACKET=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_WALL_NS="$(
    awk -F= '
        /^CPP_MEDIAN_WALL_NS_PER_PACKET=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_PPS="$(
    awk -F= '
        /^CPP_MEDIAN_PACKETS_PER_SECOND=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"


if [[ -z "$CPP_TOTAL_PACKETS" ]]; then
    echo "Could not read C++ packet count." >&2
    exit 1
fi


EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))


echo "C++ packets per PCAP: $CPP_TOTAL_PACKETS"
echo "PCAP loops per run: $PCAP_LOOPS"
echo "Expected packets per run: $EXPECTED_PACKETS"
echo "eBPF measured runs: $RUNS"
echo


sudo -v

sudo sysctl -q -w \
    kernel.bpf_stats_enabled=1


if ! mountpoint -q /sys/fs/bpf; then
    echo "/sys/fs/bpf is not mounted." >&2
    exit 1
fi


sudo ip link delete \
    "$TX_INTERFACE" \
    >/dev/null 2>&1 || true

sudo rm -f "$PIN_PATH"


sudo ip link add \
    "$TX_INTERFACE" \
    type veth \
    peer name "$RX_INTERFACE"

sudo ip link set "$TX_INTERFACE" up
sudo ip link set "$RX_INTERFACE" up


sudo bpftool prog load \
    "$BPF_OBJECT" \
    "$PIN_PATH" \
    type xdp


if sudo ip link set \
    dev "$RX_INTERFACE" \
    xdp pinned "$PIN_PATH" \
    2>"$LOG_DIRECTORY/native-attach-error.txt"
then
    ATTACH_MODE="native"
else
    echo "Native XDP attach failed; trying generic XDP."

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdpgeneric pinned "$PIN_PATH"

    ATTACH_MODE="generic"
fi


echo "XDP attach mode: $ATTACH_MODE"
echo


printf '%s\n' \
    "run,expected_packets,xdp_run_count,runtime_ns,wall_seconds,kernel_ns_per_packet,kernel_equivalent_pps,replay_pps,delivery_percent" \
    > "$CSV_OUTPUT"


for run_number in $(seq 1 "$RUNS"); do
    read -r runtime_before count_before \
        < <(read_program_stats)

    start_time_ns="$(date +%s%N)"

    sudo tcpreplay \
        --intf1="$TX_INTERFACE" \
        --topspeed \
        --preload-pcap \
        --loop="$PCAP_LOOPS" \
        "$PCAP" \
        >"$LOG_DIRECTORY/tcpreplay-run-${run_number}.txt" \
        2>&1

    end_time_ns="$(date +%s%N)"

    # Allow final ingress processing to complete before reading counters.
    sleep 0.2

    read -r runtime_after count_after \
        < <(read_program_stats)

    runtime_delta=$((runtime_after - runtime_before))

    count_delta=$((count_after - count_before))

    wall_time_ns=$((end_time_ns - start_time_ns))

    if (( count_delta <= 0 )); then
        echo "Run $run_number received zero XDP packets." >&2
        exit 1
    fi

    metrics="$(
        awk \
            -v runtime="$runtime_delta" \
            -v packets="$count_delta" \
            -v wall="$wall_time_ns" \
            -v expected="$EXPECTED_PACKETS" \
            'BEGIN {
                kernel_ns = runtime / packets
                kernel_pps = 1000000000 / kernel_ns
                wall_seconds = wall / 1000000000
                replay_pps = packets / wall_seconds
                delivery = 100 * packets / expected

                printf "%.9f %.3f %.3f %.3f %.6f",
                    wall_seconds,
                    kernel_ns,
                    kernel_pps,
                    replay_pps,
                    delivery
            }'
    )"

    read -r \
        wall_seconds \
        kernel_ns_per_packet \
        kernel_equivalent_pps \
        replay_pps \
        delivery_percent \
        <<< "$metrics"

    printf '%s\n' \
        "$run_number,$EXPECTED_PACKETS,$count_delta,$runtime_delta,$wall_seconds,$kernel_ns_per_packet,$kernel_equivalent_pps,$replay_pps,$delivery_percent" \
        >> "$CSV_OUTPUT"

    echo \
        "Run $run_number: " \
        "xdp_packets=$count_delta " \
        "kernel_ns_per_packet=$kernel_ns_per_packet " \
        "kernel_equivalent_pps=$kernel_equivalent_pps " \
        "replay_pps=$replay_pps " \
        "delivery=$delivery_percent%"
done


python - \
    "$CSV_OUTPUT" \
    "$JSON_OUTPUT" \
    "$MARKDOWN_OUTPUT" \
    "$CPP_TOTAL_PACKETS" \
    "$CPP_CPU_NS" \
    "$CPP_WALL_NS" \
    "$CPP_PPS" \
    "$ATTACH_MODE" \
    "$PCAP_LOOPS" \
    <<'PY'
import csv
import json
import statistics
import sys
from pathlib import Path


(
    csv_path,
    json_path,
    markdown_path,
    cpp_packets,
    cpp_cpu_ns,
    cpp_wall_ns,
    cpp_pps,
    attach_mode,
    pcap_loops,
) = sys.argv[1:]


with Path(csv_path).open(
    "r",
    encoding="utf-8",
    newline="",
) as file:
    rows = list(csv.DictReader(file))


def values(column: str) -> list[float]:
    return [
        float(row[column])
        for row in rows
    ]


ebpf_kernel_ns = statistics.median(
    values("kernel_ns_per_packet")
)

ebpf_kernel_pps = statistics.median(
    values("kernel_equivalent_pps")
)

ebpf_replay_pps = statistics.median(
    values("replay_pps")
)

delivery_percent = statistics.median(
    values("delivery_percent")
)

cpp_cpu_ns_value = float(cpp_cpu_ns)
cpp_wall_ns_value = float(cpp_wall_ns)
cpp_pps_value = float(cpp_pps)

cpu_cost_speedup = (
    cpp_cpu_ns_value / ebpf_kernel_ns
)

wall_cost_speedup = (
    cpp_wall_ns_value / ebpf_kernel_ns
)

equivalent_throughput_speedup = (
    ebpf_kernel_pps / cpp_pps_value
)

packet_loss_percent = max(
    0.0,
    100.0 - delivery_percent,
)


report = {
    "workload": {
        "pcap": (
            "2025-10-02-traffic-from-infected-Android-phone.pcap"
        ),
        "packets_per_loop": int(cpp_packets),
        "pcap_loops_per_run": int(pcap_loops),
        "measured_runs": len(rows),
    },
    "cpp_parser": {
        "median_cpu_ns_per_packet": cpp_cpu_ns_value,
        "median_wall_ns_per_packet": cpp_wall_ns_value,
        "median_packets_per_second": cpp_pps_value,
    },
    "ebpf_xdp_parser": {
        "attach_mode": attach_mode,
        "median_kernel_ns_per_packet": ebpf_kernel_ns,
        "median_kernel_equivalent_pps": ebpf_kernel_pps,
        "median_sustained_replay_pps": ebpf_replay_pps,
        "median_delivery_percent": delivery_percent,
        "median_packet_loss_percent": packet_loss_percent,
    },
    "comparison": {
        "cpu_cost_speedup_x": cpu_cost_speedup,
        "wall_cost_speedup_x": wall_cost_speedup,
        "equivalent_throughput_speedup_x": (
            equivalent_throughput_speedup
        ),
        "kernel_cost_reduction_percent": (
            100.0
            * (
                1.0
                - ebpf_kernel_ns / cpp_cpu_ns_value
            )
        ),
    },
}


Path(json_path).write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)


markdown = f"""# FlowGuard eBPF/XDP vs C++ Parser Benchmark

## Workload

- PCAP packets: {int(cpp_packets):,}
- PCAP loops per eBPF run: {int(pcap_loops)}
- Measured runs: {len(rows)}
- XDP attachment mode: `{attach_mode}`

## Median results

| Metric | C++ parser | eBPF/XDP parser |
|---|---:|---:|
| Processing cost | {cpp_cpu_ns_value:,.3f} ns/packet | {ebpf_kernel_ns:,.3f} ns/packet |
| Equivalent throughput | {cpp_pps_value:,.0f} packets/s | {ebpf_kernel_pps:,.0f} packets/s |
| Sustained replay throughput | Not measured | {ebpf_replay_pps:,.0f} packets/s |
| Packet delivery | Not applicable | {delivery_percent:.4f}% |
| Packet loss | Not applicable | {packet_loss_percent:.4f}% |

## Comparison

- eBPF processing-cost speedup: **{cpu_cost_speedup:.2f}×**
- Equivalent-throughput speedup: **{equivalent_throughput_speedup:.2f}×**
- Kernel processing-cost reduction: **{report["comparison"]["kernel_cost_reduction_percent"]:.2f}%**

## Interpretation

The processing-cost comparison measures the average runtime of the
XDP parser in the kernel against the measured CPU cost of the C++
userspace packet parser.

The sustained replay value measures the complete test path, including
tcpreplay, the virtual Ethernet pair, kernel scheduling and XDP.

These metrics do not include FlowGuard ML inference or database work.
"""


Path(markdown_path).write_text(
    markdown,
    encoding="utf-8",
)


print("\n===== FINAL BENCHMARK =====")
print(
    f"C++ CPU cost:            "
    f"{cpp_cpu_ns_value:.3f} ns/packet"
)
print(
    f"eBPF kernel cost:        "
    f"{ebpf_kernel_ns:.3f} ns/packet"
)
print(
    f"eBPF cost speedup:       "
    f"{cpu_cost_speedup:.2f}x"
)
print(
    f"C++ equivalent PPS:      "
    f"{cpp_pps_value:,.0f}"
)
print(
    f"eBPF equivalent PPS:     "
    f"{ebpf_kernel_pps:,.0f}"
)
print(
    f"Throughput speedup:      "
    f"{equivalent_throughput_speedup:.2f}x"
)
print(
    f"Sustained replay PPS:    "
    f"{ebpf_replay_pps:,.0f}"
)
print(
    f"Delivery rate:           "
    f"{delivery_percent:.4f}%"
)
print(
    f"Packet-loss rate:        "
    f"{packet_loss_percent:.4f}%"
)

print(f"\nSaved CSV:      {csv_path}")
print(f"Saved JSON:     {json_path}")
print(f"Saved Markdown: {markdown_path}")
PY
