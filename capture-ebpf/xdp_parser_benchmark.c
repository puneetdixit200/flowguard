#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>

#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>


struct benchmark_stats {
    __u64 packets;
    __u64 bytes;
    __u64 checksum;
};


/*
 * Per-CPU storage avoids lock contention while ensuring that parsed
 * values have an observable side effect and cannot be optimized away.
 */
struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct benchmark_stats);
} parser_benchmark_stats SEC(".maps");


SEC("xdp")
int xdp_parser_benchmark(struct xdp_md *context)
{
    void *packet_start =
        (void *)(long)context->data;

    void *packet_end =
        (void *)(long)context->data_end;

    struct ethhdr *ethernet_header =
        packet_start;

    if ((void *)(ethernet_header + 1) > packet_end) {
        return XDP_PASS;
    }

    if (
        ethernet_header->h_proto
        != bpf_htons(ETH_P_IP)
    ) {
        return XDP_PASS;
    }

    struct iphdr *ipv4_header =
        (void *)(ethernet_header + 1);

    if ((void *)(ipv4_header + 1) > packet_end) {
        return XDP_PASS;
    }

    if (
        ipv4_header->version != 4
        || ipv4_header->ihl < 5
    ) {
        return XDP_PASS;
    }

    __u32 ipv4_header_length =
        (__u32)ipv4_header->ihl * 4;

    if (
        (void *)ipv4_header + ipv4_header_length
        > packet_end
    ) {
        return XDP_PASS;
    }

    __u16 source_port = 0;
    __u16 destination_port = 0;

    void *transport_header =
        (void *)ipv4_header + ipv4_header_length;

    if (ipv4_header->protocol == IPPROTO_TCP) {
        struct tcphdr *tcp_header =
            transport_header;

        if ((void *)(tcp_header + 1) <= packet_end) {
            source_port =
                bpf_ntohs(tcp_header->source);

            destination_port =
                bpf_ntohs(tcp_header->dest);
        }
    } else if (
        ipv4_header->protocol == IPPROTO_UDP
    ) {
        struct udphdr *udp_header =
            transport_header;

        if ((void *)(udp_header + 1) <= packet_end) {
            source_port =
                bpf_ntohs(udp_header->source);

            destination_port =
                bpf_ntohs(udp_header->dest);
        }
    }

    __u32 stats_key = 0;

    struct benchmark_stats *stats =
        bpf_map_lookup_elem(
            &parser_benchmark_stats,
            &stats_key
        );

    if (stats != NULL) {
        stats->packets += 1;

        stats->bytes +=
            (__u64)(
                context->data_end
                - context->data
            );

        stats->checksum +=
            (__u64)ipv4_header->saddr
            + (__u64)ipv4_header->daddr
            + (__u64)source_port
            + (__u64)destination_port
            + (__u64)ipv4_header->protocol;
    }

    return XDP_PASS;
}


char program_license[] SEC("license") = "GPL";
