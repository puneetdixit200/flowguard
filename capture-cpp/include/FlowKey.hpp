#pragma once
#include <cstdint>
#include <string>
#include <tuple>


//understn the flow key
struct FlowKey {
    std::string src_ip;
    std::string dst_ip;
    uint16_t src_port;
    uint16_t dst_port;
    std::string protocol;

    bool operator<(const FlowKey& other) const {
        return std::tie(src_ip, dst_ip, src_port, dst_port, protocol) < std::tie(other.src_ip, other.dst_ip, other.src_port, other.dst_port, other.protocol);
    }

};