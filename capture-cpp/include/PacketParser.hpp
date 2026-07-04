#pragma once

#include "PacketInfo.hpp"
#include <optional>
#include <pcap.h>

class PacketParser {
public:
    std::optional<PacketInfo> parse(const pcap_pkthdr* header, const u_char* packet);
};
