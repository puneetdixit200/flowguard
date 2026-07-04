#include "PacketParser.hpp"

#include <arpa/inet.h>
#include <netinet/if_ether.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>

// Parse Ethernet -> IP -> TCP/UDP/ICMP
std::optional<PacketInfo> PacketParser::parse(
    const pcap_pkthdr* header,
    const u_char* packet
) {
    if (!header || !packet) {
        return std::nullopt;
    }

    if (header->caplen < sizeof(ether_header)) {
        return std::nullopt;
    }

    const auto* eth = reinterpret_cast<const ether_header*>(packet);

    if (ntohs(eth->ether_type) != ETHERTYPE_IP) {
        return std::nullopt;
    }

    const u_char* ip_start = packet + sizeof(ether_header);
    const auto* iphdr = reinterpret_cast<const ip*>(ip_start);

    PacketInfo info;

    info.packet_length = header->len;

    info.timestamp_ns =
        static_cast<uint64_t>(header->ts.tv_sec) * 1'000'000'000ULL +
        static_cast<uint64_t>(header->ts.tv_usec) * 1'000ULL;

    char src_buf[INET_ADDRSTRLEN];
    char dst_buf[INET_ADDRSTRLEN];

    inet_ntop(AF_INET, &(iphdr->ip_src), src_buf, INET_ADDRSTRLEN);
    inet_ntop(AF_INET, &(iphdr->ip_dst), dst_buf, INET_ADDRSTRLEN);

    info.src_ip = src_buf;
    info.dst_ip = dst_buf;

    int ip_header_len = iphdr->ip_hl * 4;
    const u_char* transport_start = ip_start + ip_header_len;

    if (iphdr->ip_p == IPPROTO_TCP) {
        info.protocol = "TCP";

        const auto* tcp_header =
            reinterpret_cast<const tcphdr*>(transport_start);

        info.src_port = ntohs(tcp_header->th_sport);
        info.dst_port = ntohs(tcp_header->th_dport);
        info.tcp_flags = tcp_header->th_flags;

    } else if (iphdr->ip_p == IPPROTO_UDP) {
        info.protocol = "UDP";

        const auto* udp_header =
            reinterpret_cast<const udphdr*>(transport_start);

        info.src_port = ntohs(udp_header->uh_sport);
        info.dst_port = ntohs(udp_header->uh_dport);

    } else if (iphdr->ip_p == IPPROTO_ICMP) {
        info.protocol = "ICMP";

    } else {
        info.protocol = "OTHER";
    }

    return info;
}
