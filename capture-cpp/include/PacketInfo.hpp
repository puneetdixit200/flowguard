#pragma once

#include <cstdint>
#include <string>

struct PacketInfo {
    std::string src_ip;
    std::string dst_ip;
    uint16_t src_port = 0;
    uint16_t dst_port = 0;
    std::string protocol;
    uint32_t packet_length = 0;
    uint64_t timestamp_ns = 0;
    uint8_t tcp_flags = 0;
};
