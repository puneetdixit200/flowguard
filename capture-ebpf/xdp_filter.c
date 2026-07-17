// SPDX-License-Identifier: GPL-2.0
//
// SPDX = Software Package Data Exchange.
// This line declares that the source code uses the
// GPL-2.0 = GNU General Public License version 2.0.

// Linux kernel definitions for BPF (Berkeley Packet Filter).
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>

// Helper functions and macros used by eBPF programs,
#include <bpf/bpf_helpers.h>

// Byte-order conversion helpers such as:
// bpf_htons() and bpf_ntohs().
#include <bpf/bpf_endian.h>


// BPF (Berkeley Packet Filter) hash map.
//
// Key:
//     source IPv4 address
//
// Value:
//     number of packets received from that source address
struct {
    // __uint() is a libbpf macro used to describe an integer map property.
    //
    // BPF_MAP_TYPE_HASH means a normal kernel hash table.
    __uint(type, BPF_MAP_TYPE_HASH);

    // Maximum number of unique source IPv4 addresses stored.
    __uint(max_entries, 10240);

    // __type() describes the C type used for the key.
    //
    // __u32 = unsigned 32-bit integer.
    // An IPv4 address is 32 bits.
    __type(key, __u32);

    // __u64 = unsigned 64-bit integer.
    // It stores the packet counter.
    __type(value, __u64);

} pkt_count_map SEC(".maps");


// BPF (Berkeley Packet Filter) ring-buffer map.
// A ring buffer transfers events from kernel space to userspace.
struct {
    // BPF_MAP_TYPE_RINGBUF means ring-buffer map.
    __uint(type, BPF_MAP_TYPE_RINGBUF);

    // 1 << 20 means 1 shifted left by 20 bits:
    // 1,048,576 bytes, approximately 1 MB.
    __uint(max_entries, 1 << 20);

} flow_events SEC(".maps");


// Small event copied from kernel space to userspace.
struct flow_event {
    __u32 src_ip;     // Source IPv4 address.
    __u32 dst_ip;     // Destination IPv4 address.

    __u16 src_port;   // Source port: unsigned 16-bit integer.
    __u16 dst_port;   // Destination port: unsigned 16-bit integer.

    __u8 protocol;    // Protocol number: unsigned 8-bit integer.
    __u32 pkt_len;    // Full packet length.
};


// SEC("xdp") places this function in the XDP
// (eXpress Data Path) ELF section.
//
// ELF = Executable and Linkable Format.
//
// The Linux loader uses this section to recognize it as an
// XDP (eXpress Data Path) program.
SEC("xdp")
int xdp_flow_monitor(struct xdp_md *ctx)
{
    // ctx = context.
    //
    // struct xdp_md contains packet metadata supplied by the kernel.
    //
    // ctx->data:
    //     address where packet data starts
    //
    // ctx->data_end:
    //     address immediately after the packet ends

    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;


    // Treat the beginning of the packet as an Ethernet header.
    struct ethhdr *eth = data;

    // Bounds check:
    // Ensure the complete Ethernet header exists inside the packet.
    //
    // The eBPF verifier requires this check before header memory is read.
    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;


    // h_proto stores the Ethernet protocol type.
    //
    // ETH_P_IP means IPv4.
    //
    // bpf_htons() converts a 16-bit number from host byte order
    // to network byte order.
    if (eth->h_proto != bpf_htons(ETH_P_IP))
        return XDP_PASS;


    // The IPv4 header starts immediately after the Ethernet header.
    struct iphdr *ip = data + sizeof(struct ethhdr);
ch
    // Confirm that the complete minimum IPv4 header is available.
    if ((void *)(ip + 1) > data_end)
        return XDP_PASS;


    // IPv4 addresses are stored as 32-bit integers.
    __u32 src_ip = ip->saddr;
    __u32 dst_ip = ip->daddr;


    // Look up the existing counter for this source IPv4 address.
    //
    // Returns:
    //     pointer to the value when the key exists
    //     NULL when the key does not exist
    __u64 *count =
        bpf_map_lookup_elem(&pkt_count_map, &src_ip);


    // Ternary expression:
    //
    // If count exists:
    //     old count + 1
    //
    // Otherwise:
    //     start at 1
    __u64 new_count = count ? (*count + 1) : 1;


    // Insert or replace the map value.
    //
    // BPF_ANY means:
    //     create the key if it does not exist
    //     replace it if it already exists
    bpf_map_update_elem(
        &pkt_count_map,
        &src_ip,
        &new_count,
        BPF_ANY
    );


    // Important:
    // This is a lifetime counter, not a rate counter.
    //
    // Once a source has sent more than 500 packets,
    // all later packets from that source are dropped until
    // the map entry is deleted or the program is restarted.
    if (new_count > 500) {
        return XDP_DROP;
    }


    // Reserve memory for one event inside the BPF ring buffer.
    struct flow_event *evt =
        bpf_ringbuf_reserve(
            &flow_events,
            sizeof(*evt),
            0
        );


    // Reserve can fail when the ring buffer is full.
    if (evt) {
        // Initialize transport ports so UDP/TCP parsing failure does
        // not leave uninitialized memory.
        evt->src_port = 0;
        evt->dst_port = 0;

        evt->src_ip = src_ip;
        evt->dst_ip = dst_ip;

        // Calculate complete packet length.
        evt->pkt_len = (__u32)(
            ctx->data_end - ctx->data
        );

        // IPv4 protocol field:
        //
        // IPPROTO_TCP = Transmission Control Protocol
        // IPPROTO_UDP = User Datagram Protocol
        evt->protocol = ip->protocol;


        // ip->ihl = Internet Header Length.
        //
        // It is measured in 32-bit words.
        // Multiplying by 4 converts it into bytes.
        __u32 ip_header_length = ip->ihl * 4;


        // Validate that the Internet Header Length is at least
        // the normal minimum IPv4 header length: 20 bytes.
        if (ip_header_length < sizeof(struct iphdr)) {
            bpf_ringbuf_discard(evt, 0);
            return XDP_PASS;
        }


        if (ip->protocol == IPPROTO_TCP) {
            // Locate the TCP (Transmission Control Protocol) header.
            struct tcphdr *tcp =
                (void *)ip + ip_header_length;

            // Ensure the TCP header is inside packet bounds.
            if ((void *)(tcp + 1) <= data_end) {
                // TCP ports are stored in network byte order.
                //
                // bpf_ntohs() converts network byte order
                // to host byte order.
                evt->src_port = bpf_ntohs(tcp->source);
                evt->dst_port = bpf_ntohs(tcp->dest);
            }

        } else if (ip->protocol == IPPROTO_UDP) {
            // Locate the UDP (User Datagram Protocol) header.
            struct udphdr *udp =
                (void *)ip + ip_header_length;

            // Ensure the UDP header is inside packet bounds.
            if ((void *)(udp + 1) <= data_end) {
                evt->src_port = bpf_ntohs(udp->source);
                evt->dst_port = bpf_ntohs(udp->dest);
            }
        }


        // Mark the reserved event as complete.
        //
        // Userspace can now read it from the ring buffer.
        bpf_ringbuf_submit(evt, 0);
    }


    // Let the packet continue into the normal Linux networking stack.
    return XDP_PASS;
}


// The kernel requires eBPF programs to declare their license.
//
// GPL = GNU General Public License.
//
// Some eBPF helper functions are only available to programs
// declaring a GPL-compatible license.
char _license[] SEC("license") = "GPL";
