#include "PackeParser.hpp"
#include <arpa/inet.h>
#include <cstring>
#include <netinet/ifether.h>
#include <netinet/ip_.h>
#include <netinet/udp.h>
#include <netinet/tcp.h>

//parse etehrnet to IP to UDP/TCP

std::optional<PacketInfo>PacketParser::parse(const pcap_pkthdr * header,const u_char* packet){
    if(!header || !packet) return std::nullopt;
    if(header->caplen <sizeof(ether_header)) return std::nullopt;
    const auto
}