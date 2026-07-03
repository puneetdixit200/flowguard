#pragma once
#include "PacketInfo.hpp"
#include <cstdint>

struct FlowStats{
    uint64_t first_ts = 0;
    uint64_t last_ts = 0;
    uint64_t packet_count = 0;
    uint64_t total_bytes = 0;  

    uint64_t syn_count = 0;
    uint64_t ack_count = 0;
    uint64_t fin_count = 0;
    uint64_t rst_count = 0;

    void update(const PacketInfo& pkt){
        if(packet_count==0){
            first_ts=pkt.timestamp_ns;
        }
        last_ts=pkt.timestamp_ns;
        packet_count++;
        total_bytes+=pkt.packet_length;

        //basic flag

        if(pkt.protocol =="TCP"){
        if(pkt.tcp_flags & 0x02) syn_count++; //SYN
        if(pkt.tcp_flags & 0x10) ack_count++; //ACK
        if(pkt.tcp_flags & 0x01) fin_count++; //FIN
        if(pkt.tcp_flags & 0x04) rst_count++; //RST
        }

        double duration_seconds() const 
        {
            if(last_ts<first_ts) return 0.0;
            return static_cast<double>(last_ts - first_ts) / 1'000'000'000.0;
        }
};
    