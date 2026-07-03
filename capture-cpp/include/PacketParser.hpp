#pragma once
#include "PacketInfo.hpp"
#include <optional>
#include <pcap.h>

class PacketParser{
    public:
        std::optiona<PacketInfo> parse (const pcap_pkthdr* header , const u_chair* packet);
        
};
