// Standalone benchmark: measures how fast the C++ layer parses packets
// and aggregates flows. Run this separately from main.cpp for clean timing.
#include "PacketParser.hpp"
#include "FlowAggregator.hpp"
#include <chrono>
#include <iostream>
#include <pcap.h>

int main(int argc, char** argv) {
    const char* filename = argc > 1 ? argv[1] : "../data/sample/small_sample.pcap";
    char errbuf[PCAP_ERRBUF_SIZE];

    pcap_t* handle = pcap_open_offline(filename, errbuf);
    if (!handle) {
        std::cerr << "Failed to open: " << errbuf << "\n";
        return 1;
    }

    PacketParser parser;
    FlowAggregator aggregator;
    const u_char* packet;
    struct pcap_pkthdr* header;

    long packet_count = 0;

    // Start the clock right before processing begins.
    auto start = std::chrono::high_resolution_clock::now();

    while (pcap_next_ex(handle, &header, &packet) == 1) {
        auto parsed = parser.parse(header, packet);
        if (parsed.has_value()) {
            aggregator.processPacket(parsed.value());
            packet_count++;
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    double elapsed_ms = std::chrono::duration<double, std::milli>(end - start).count();

    pcap_close(handle);

    // These are your resume numbers: total packets, total time, packets/sec.
    std::cout << "===== CAPTURE BENCHMARK =====\n";
    std::cout << "Packets processed: " << packet_count << "\n";
    std::cout << "Total time: " << elapsed_ms << " ms\n";
    std::cout << "Throughput: " << (packet_count / (elapsed_ms / 1000.0)) << " packets/sec\n";
    std::cout << "Avg time per packet: " << (elapsed_ms * 1000.0 / packet_count) << " microseconds\n";

    return 0;
}
