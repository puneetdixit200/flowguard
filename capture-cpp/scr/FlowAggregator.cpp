#include "FlowAggregator.hpp"
#include "JsonSerializer.hpp"
#include <iostream>

void FlowAggregator::processPacket(const PacketInfo& pkt) {
    FlowKey key{pkt.src_ip, pkt.dst_ip, pkt.src_port, pkt.dst_port, pkt.protocol};
    flows[key].update(pkt);
}

void FlowAggregator::printAllFlows() const {
    std::cout << "\n===== FLOW SUMMARY =====\n";
    for (const auto& [key, stats] : flows) {
        std::cout << key.src_ip << ":" << key.src_port << " -> "
                   << key.dst_ip << ":" << key.dst_port << " [" << key.protocol << "]"
                   << " packets=" << stats.packet_count
                   << " bytes=" << stats.total_bytes << "\n";
    }
}

void FlowAggregator::flushAllAsJson() {
    for (const auto& [key, stats] : flows) {
        emitter_.emit(JsonSerializer::toJsonLine(key, stats));
    }
}
