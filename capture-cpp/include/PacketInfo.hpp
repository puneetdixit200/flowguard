#pragma once
#include <cstdint>
#include <string>

//struct to understand packets

struct PacketInfo{
    std::string scr_ip;
    std::string dst_ip;
    uint16_t src_port;
    uint16_t dst_port;
    std::string protocol;
    uint32_t packet_length=0;
    uint64_t timestamp_ns=0 ;
    uint8_t tcp_flags=0;
};