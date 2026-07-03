#include "FlowAggregator.hpp"
#include <iostream>

void FlowAggregator::processPacket(const PacketInfo& pkt) {
    FlowKey key{
        pkt.src_ip,
        pkt.dst_ip,
        pkt.src_port,
        pkt.dst_port,
        pkt.protocol
    };

    flows[key].update(pkt);
}

void FlowAggregator::printAllFlows() const {
    std::cout << "\n===== FLOW SUMMARY =====\n";

    for (const auto& [key, stats] : flows) {
        std::cout
            << key.src_ip << ":" << key.src_port
            << " -> "
            << key.dst_ip << ":" << key.dst_port
            << " [" << key.protocol << "]"
            << " packets=" << stats.packet_count
            << " bytes=" << stats.total_bytes
            << " duration=" << stats.duration_seconds()
            << " syn=" << stats.syn_count
            << " ack=" << stats.ack_count
            << " fin=" << stats.fin_count
            << " rst=" << stats.rst_count
            << "\n";
    }
}

