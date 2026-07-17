// SPDX-License-Identifier: GPL-2.0
// This program runs INSIDE THE LINUX KERNEL at the network driver level.
// It inspects every incoming packet before the kernel's normal network
// stack even touches it, and decides: pass it up, or drop it immediately.

#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <linux/tcp.h>
#include <bpf/bpf_helpers.h>  // SEC(), BPF map macros, helper declarations
#include <bpf/bpf_endian.h>



// A BPF map is a kernel-resident data structure our userspace program can
// read. Here we count packets per source IP — this is how we detect a scan
// (one IP touching many others) directly in the kernel, cheaply.
//
//
// BPF hash map:
//
// key   = source IPv4 address
// value = number of packets received from that source
//
// The map lives inside the kernel, but a userspace program can read it.

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 10240);
    __type(key, __u32);      // source IP as key
    __type(value, __u64);    // packet count as value
} pkt_count_map SEC(".maps");


// A ring buffer map lets us stream flow events up to userspace efficiently,
// without the overhead of copying every raw packet like libpcap does.
struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 1 << 20); // 1MB ring buffer
} flow_events SEC(".maps");

struct flow_event {
    __u32 src_ip;
    __u32 dst_ip;
    __u16 src_port;
    __u16 dst_port;
    __u8  protocol;
    __u32 pkt_len;
};

SEC("xdp")
