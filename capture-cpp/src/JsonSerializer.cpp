#include "JsonSerializer.hpp"
#include <sstream>

std::string JsonSerializer::toJsonLine(const FlowKey& key, const FlowStats& stats) {
    std::ostringstream out;

    out << "{"
        << "\"src_ip\":\"" << key.src_ip << "\","
        << "\"dst_ip\":\"" << key.dst_ip << "\","
        << "\"src_port\":" << key.src_port << ","
        << "\"dst_port\":" << key.dst_port << ","
        << "\"protocol\":\"" << key.protocol << "\","
        << "\"packet_count\":" << stats.packet_count << ","
        << "\"total_bytes\":" << stats.total_bytes << ","
        << "\"duration_seconds\":" << stats.duration_seconds() << ","
        << "\"syn_count\":" << stats.syn_count << ","
        << "\"ack_count\":" << stats.ack_count << ","
        << "\"fin_count\":" << stats.fin_count << ","
        << "\"rst_count\":" << stats.rst_count
        << "}";

    return out.str();
}
