#include "PacketParser.hpp"

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <pcap.h>
#include <string>
#include <time.h>
#include <vector>

struct StoredPacket {
    pcap_pkthdr header{};
    std::vector<u_char> data;
};

static std::uint64_t process_cpu_time_ns()
{
    timespec value{};
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &value);

    return (
        static_cast<std::uint64_t>(value.tv_sec) * 1'000'000'000ULL
        + static_cast<std::uint64_t>(value.tv_nsec)
    );
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        std::cerr
            << "Usage: " << argv[0]
            << " <pcap-file> [repetitions]\n";
        return 1;
    }

    const std::string pcap_path = argv[1];
    const int repetitions = argc >= 3
        ? std::max(1, std::stoi(argv[2]))
        : 7;

    char error_buffer[PCAP_ERRBUF_SIZE]{};

    pcap_t *handle = pcap_open_offline(
        pcap_path.c_str(),
        error_buffer
    );

    if (handle == nullptr) {
        std::cerr << "Could not open PCAP: "
                  << error_buffer << "\n";
        return 1;
    }

    std::vector<StoredPacket> packets;

    pcap_pkthdr *header = nullptr;
    const u_char *packet_data = nullptr;

    while (true) {
        const int result = pcap_next_ex(
            handle,
            &header,
            &packet_data
        );

        if (result == 1) {
            StoredPacket packet;
            packet.header = *header;

            packet.data.assign(
                packet_data,
                packet_data + header->caplen
            );

            packets.push_back(std::move(packet));
        } else if (result == -2) {
            break;
        } else if (result == -1) {
            std::cerr << "PCAP read error: "
                      << pcap_geterr(handle) << "\n";
            pcap_close(handle);
            return 1;
        }
    }

    pcap_close(handle);

    if (packets.empty()) {
        std::cerr << "PCAP contains no packets.\n";
        return 1;
    }

    PacketParser parser;

    // Warm-up run, excluded from measurements.
    std::uint64_t warmup_checksum = 0;

    for (const StoredPacket &packet : packets) {
        const auto parsed = parser.parse(
            &packet.header,
            packet.data.data()
        );

        if (parsed.has_value()) {
            warmup_checksum += parsed->packet_length;
            warmup_checksum += parsed->src_port;
            warmup_checksum += parsed->dst_port;
        }
    }

    std::vector<double> wall_ns_per_packet;
    std::vector<double> cpu_ns_per_packet;
    std::vector<double> packets_per_second;
    std::vector<double> cpu_percentages;

    std::uint64_t final_checksum = warmup_checksum;
    std::size_t parsed_packets = 0;

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Packets loaded: " << packets.size() << "\n";
    std::cout << "Repetitions: " << repetitions << "\n\n";

    for (int run = 1; run <= repetitions; ++run) {
        std::uint64_t checksum = 0;
        std::size_t parsed = 0;

        const std::uint64_t cpu_start =
            process_cpu_time_ns();

        const auto wall_start =
            std::chrono::steady_clock::now();

        for (const StoredPacket &packet : packets) {
            const auto result = parser.parse(
                &packet.header,
                packet.data.data()
            );

            if (result.has_value()) {
                ++parsed;

                checksum += result->packet_length;
                checksum += result->src_port;
                checksum += result->dst_port;
                checksum += result->tcp_flags;
                checksum += result->src_ip.size();
                checksum += result->dst_ip.size();
            }
        }

        const auto wall_end =
            std::chrono::steady_clock::now();

        const std::uint64_t cpu_end =
            process_cpu_time_ns();

        const double wall_ns =
            std::chrono::duration<double, std::nano>(
                wall_end - wall_start
            ).count();

        const double cpu_ns =
            static_cast<double>(cpu_end - cpu_start);

        const double inspected =
            static_cast<double>(packets.size());

        const double wall_cost =
            wall_ns / inspected;

        const double cpu_cost =
            cpu_ns / inspected;

        const double throughput =
            inspected * 1'000'000'000.0 / wall_ns;

        const double cpu_percentage =
            100.0 * cpu_ns / wall_ns;

        wall_ns_per_packet.push_back(wall_cost);
        cpu_ns_per_packet.push_back(cpu_cost);
        packets_per_second.push_back(throughput);
        cpu_percentages.push_back(cpu_percentage);

        parsed_packets = parsed;
        final_checksum ^= checksum;

        std::cout
            << "Run " << run
            << ": inspected=" << packets.size()
            << " parsed=" << parsed
            << " wall_ns_per_packet=" << wall_cost
            << " cpu_ns_per_packet=" << cpu_cost
            << " packets_per_second=" << throughput
            << " cpu_percent=" << cpu_percentage
            << "\n";
    }

    auto median = [](std::vector<double> values) {
        std::sort(values.begin(), values.end());
        return values[values.size() / 2];
    };

    std::cout << "\n===== C++ PARSER MEDIAN =====\n";
    std::cout
        << "CPP_TOTAL_PACKETS=" << packets.size() << "\n";
    std::cout
        << "CPP_PARSED_PACKETS=" << parsed_packets << "\n";
    std::cout
        << "CPP_MEDIAN_WALL_NS_PER_PACKET="
        << median(wall_ns_per_packet) << "\n";
    std::cout
        << "CPP_MEDIAN_CPU_NS_PER_PACKET="
        << median(cpu_ns_per_packet) << "\n";
    std::cout
        << "CPP_MEDIAN_PACKETS_PER_SECOND="
        << median(packets_per_second) << "\n";
    std::cout
        << "CPP_MEDIAN_CPU_PERCENT="
        << median(cpu_percentages) << "\n";
    std::cout
        << "CHECKSUM=" << final_checksum << "\n";

    return 0;
}
