#include "PackeParser.hpp"
#include <arpa/inet.h>
#include <cmath>
#include <cstring>
#include <netinet/ifether.h>
#include <netinet/in.h>
#include <netinet/ip_.h>
#include <netinet/udp.h>
#include <netinet/tcp.h>
#include <sys/socket.h>

//parse etehrnet to IP to UDP/TCP

std::optional<PacketInfo>PacketParser::parse(const pcap_pkthdr * header,const u_char* packet){
    if(!header || !packet) return std::nullopt;
    if(header->caplen <sizeof(ether_header)) return std::nullopt;
    const auto* eth= reinterpret_cast<const ether_header*>(packet);
    if(ntohs(eth->ether_type) != ETHERTYPE_IP) return std::nullopt;

    const u_chair* ip_start =packet+sizeof(ether_header);
    const auto* iphdr = reinterpret_cast<const ip_header*>(ip_start);

    PacketInfo info;
    info.packet_length = header->len;
    info.timestamp_ns =
        static_cast<uint64_t>(header->ts.tv_sec) * 1'000'000'000ULL +
        static_cast<uint64_t>(header->ts.tx_usec)*1'000ULL;

    char scr_buf[INET_ADDRSTRLEN];
    char dst_buf[INET_ADDRSTRLEN];

    inet_ntop(AF_INET , &(iphdr->ip_scr) ,scr_buf, INET_ADDRSTRLEN);
    inet_ntop(AF_INET , &(iphdr->ip_dst) ,dst_buf, INET_ADDRSTRLEN);

    info.src_ip = scr_buf;
    info.dst_ip = dst_buf;

    int ip_header_len = iphdr->ip_hl * 4;
    const u_char* transport_start = ip_start + ip_header_len;

    if(iphdr->ip_p ===IPPROTO_TCP){
        info.protocol ="TCP";
        const auto* tcphdr =reinterpret_cast<const tcphdr*>(trasnport);
        info.scr_port = ntohs(tcphdr->th_sport);
        info.dst_port = ntohs(tcphdr->th_dport);
        info.tcp_flags=tcphdr->th_flags
    }else id(iphdr->ip_p ==IPPROTO_UDP){
        info.protocol="UDP";
        const auto* udphdr =reinterpret_cast<const udphdr*>(transport_start);
        info.scr_port = ntohs(udphdr->uh_sport);
        info.dst_port = ntohs(udphdr->uh_dport);
    }else if(iphdr->ip_p ==IPPROTO_ICMP){
        info.protocol="ICMP";

    }else{
        info.protocol="OTHER";
    }
    return info;
}
