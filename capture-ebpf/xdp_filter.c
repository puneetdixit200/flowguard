// SPDX-License-Identifier: GPL-2.0
//
// SPDX = Software Package Data Exchange.
// GPL = GNU General Public License.
//
// This program uses version 2.0 of the GNU General Public License.

/*
===============================================================================
PROGRAM PURPOSE
===============================================================================

This is an eBPF (extended Berkeley Packet Filter) program attached to:

    XDP (eXpress Data Path)

It examines incoming Ethernet packets very early in the Linux networking path.

Incoming packet:

    Network Interface Card
             │
             ▼
    XDP (eXpress Data Path)
             │
             ├── Too many packets from source → XDP_DROP
             │
             └── Otherwise                    → XDP_PASS
                                                     │
                                                     ▼
                                           Linux network stack

The program also sends a small summary of each packet to a userspace program:

    Kernel space
         │
         │ packet_event
         ▼
    BPF ring buffer
         │
         ▼
    Userspace C or C++ program
===============================================================================
*/


// Core BPF (Berkeley Packet Filter) definitions.
#include <linux/bpf.h>

// Ethernet header definitions such as struct ethhdr and ETH_P_IP.
#include <linux/if_ether.h>

// IPv4 (Internet Protocol version 4) header definition: struct iphdr.
#include <linux/ip.h>

// TCP (Transmission Control Protocol) header definition: struct tcphdr.
#include <linux/tcp.h>
#include <linux/in.h>
// UDP (User Datagram Protocol) header definition: struct udphdr.
#include <linux/udp.h>

// Helper functions and macros used by eBPF programs.
#include <bpf/bpf_helpers.h>

// Byte-order conversion helpers such as:
// bpf_htons() = Berkeley Packet Filter host-to-network short
// bpf_ntohs() = Berkeley Packet Filter network-to-host short
#include <bpf/bpf_endian.h>


// Maximum number of different source IPv4 addresses stored in the hash map.
#define MAX_TRACKED_SOURCE_ADDRESSES 10240

// Size of the kernel-to-userspace ring buffer.
//
// 1 << 20 means:
//
//     1 × 2²⁰
//     = 1,048,576 bytes
//     ≈ 1 megabyte
#define RING_BUFFER_SIZE_BYTES (1 << 20)

// Demonstration-only lifetime packet threshold.
//
// Important:
// This is NOT "500 packets per second."
//
// It currently means:
//
//     more than 500 packets since this map entry was created
//
// Therefore, this threshold should not be used in production without
// adding a proper time window.
#define DEMO_PACKET_LIMIT_PER_SOURCE 500


/*
===============================================================================
MAP 1: PACKET COUNTER
===============================================================================

A BPF (Berkeley Packet Filter) map is a data structure stored in the
Linux kernel.

This map works like:

    source IPv4 address  ─────────────► packet count

Example:

    192.168.1.10         ─────────────► 42
    192.168.1.20         ─────────────► 310
    10.0.0.5             ─────────────► 501

The source IPv4 address is the key.
The packet count is the value.
===============================================================================
*/

struct {
    /*
     * BPF_MAP_TYPE_HASH means:
     *
     * Create a normal hash table inside the Linux kernel.
     *
     * It stores:
     *
     *     key → value
     */
    __uint(type, BPF_MAP_TYPE_HASH);

    // Maximum number of unique source IPv4 addresses.
    __uint(max_entries, MAX_TRACKED_SOURCE_ADDRESSES);

    /*
     * Key type:
     *
     * __u32 = unsigned 32-bit integer
     *
     * An IPv4 address contains 32 bits.
     */
    __type(key, __u32);

    /*
     * Value type:
     *
     * __u64 = unsigned 64-bit integer
     *
     * This stores the packet count.
     */
    __type(value, __u64);

} packet_count_by_source_ipv4 SEC(".maps");


/*
===============================================================================
MAP 2: RING BUFFER
===============================================================================

The ring buffer transfers packet summaries from kernel space to userspace.

    eBPF program inside Linux kernel
                  │
                  │ writes packet_event
                  ▼
            BPF ring buffer
                  │
                  │ userspace reads event
                  ▼
             C or C++ program

It is called a "ring" because when memory reaches the end, it logically
continues again from the beginning after old events are consumed.
===============================================================================
*/

struct {
    // Create a BPF (Berkeley Packet Filter) ring-buffer map.
    __uint(type, BPF_MAP_TYPE_RINGBUF);

    // Allocate approximately one megabyte.
    __uint(max_entries, RING_BUFFER_SIZE_BYTES);

} packet_events_to_userspace SEC(".maps");


/*
===============================================================================
PACKET EVENT
===============================================================================

This structure is sent from kernel space to userspace.

Packet:

    [ Ethernet ][ IPv4 ][ TCP or UDP ][ Data ]
                      │
                      └──────── information extracted into packet_event

Important:
Although the original structure was named flow_event, one event represents
one packet. Multiple packet events must later be combined to form a flow.
===============================================================================
*/

struct packet_event {
    // Source IPv4 (Internet Protocol version 4) address.
    __u32 source_ipv4_address;

    // Destination IPv4 (Internet Protocol version 4) address.
    __u32 destination_ipv4_address;

    // Complete packet length in bytes.
    __u32 packet_length_bytes;

    // TCP or UDP source port.
    __u16 source_port;

    // TCP or UDP destination port.
    __u16 destination_port;

    /*
     * IPv4 transport protocol number.
     *
     * Common values:
     *
     * 1  = ICMP, Internet Control Message Protocol
     * 6  = TCP, Transmission Control Protocol
     * 17 = UDP, User Datagram Protocol
     */
    __u8 transport_protocol;

    /*
     * Explicit padding keeps the structure layout predictable.
     *
     * The userspace version of this structure must have exactly
     * the same field order and sizes.
     */
    __u8 reserved_padding[3];
};


/*
===============================================================================
XDP PROGRAM
===============================================================================

SEC("xdp") places this function into the XDP section of the compiled
ELF (Executable and Linkable Format) object file.

The Linux BPF loader understands:

    "This function is an XDP program."
===============================================================================
*/

SEC("xdp")
int inspect_incoming_packet(struct xdp_md *packet_context)
{
    /*
     * packet_context points to XDP metadata supplied by the Linux kernel.
     *
     * packet_context->data
     *     Address of the first packet byte.
     *
     * packet_context->data_end
     *     Address immediately after the final valid packet byte.
     *
     * Memory layout:
     *
     * packet_start                                      packet_end
     *      │                                                 │
     *      ▼                                                 ▼
     *      [ Ethernet ][ IPv4 ][ TCP or UDP ][ Packet data ]
     *
     * Valid memory:
     *
     *     packet_start <= valid address < packet_end
     */

    void *packet_start =
        (void *)(long)packet_context->data;

    void *packet_end =
        (void *)(long)packet_context->data_end;


    /*
    ===========================================================================
    STEP 1: READ THE ETHERNET HEADER
    ===========================================================================

    The first bytes of an ordinary Ethernet frame are:

        ┌───────────────────────────────────────────────┐
        │ Destination Media Access Control address     │ 6 bytes
        ├───────────────────────────────────────────────┤
        │ Source Media Access Control address          │ 6 bytes
        ├───────────────────────────────────────────────┤
        │ EtherType                                    │ 2 bytes
        └───────────────────────────────────────────────┘

        Total Ethernet header size = 14 bytes
    ===========================================================================
    */

    // Treat the first packet bytes as an Ethernet header.
    //
    // No packet data is copied.
    // ethernet_header simply points at packet_start.
    struct ethhdr *ethernet_header = packet_start;


    /*
     * ethernet_header + 1 means:
     *
     *     move forward by one complete struct ethhdr
     *
     * It does NOT mean move forward by one byte.
     *
     * Example:
     *
     * ethernet_header                         ethernet_header + 1
     *       │                                          │
     *       ▼                                          ▼
     *       [------ Ethernet header: 14 bytes --------][ next bytes ]
     *
     * If ethernet_header + 1 is beyond packet_end,
     * the complete Ethernet header does not exist.
     */
    if ((void *)(ethernet_header + 1) > packet_end) {
        // The packet is truncated or malformed.
        //
        // XDP_PASS means:
        // Stop inspecting it here and allow it into the normal network stack.
        return XDP_PASS;
    }


    /*
    ===========================================================================
    STEP 2: CHECK THE ETHERNET PAYLOAD TYPE
    ===========================================================================

    Ethernet can contain several different protocols:

        0x0800 = IPv4, Internet Protocol version 4
        0x86DD = IPv6, Internet Protocol version 6
        0x0806 = ARP, Address Resolution Protocol

    This program currently understands only IPv4.
    ===========================================================================
    */

    /*
     * ethernet_header->h_proto means:
     *
     *     Follow the ethernet_header pointer
     *     and read its h_proto field.
     *
     * The arrow operator:
     *
     *     pointer->field
     *
     * is equivalent to:
     *
     *     (*pointer).field
     */
    if (
        ethernet_header->h_proto
        != bpf_htons(ETH_P_IP)
    ) {
        /*
         * ETH_P_IP represents IPv4.
         *
         * bpf_htons() means:
         *
         *     Berkeley Packet Filter
         *     host-to-network short
         *
         * host:
         *     The computer's native byte order.
         *
         * network:
         *     Big-endian network byte order.
         *
         * short:
         *     A 16-bit integer.
         */
        return XDP_PASS;
    }


    /*
    ===========================================================================
    STEP 3: LOCATE THE IPv4 HEADER
    ===========================================================================

    Packet memory now looks like:

        packet_start
             │
             ▼
        [ Ethernet header ][ IPv4 header ][ TCP/UDP header ][ Data ]
                            ▲
                            │
                     ipv4_header

    ethernet_header + 1 points immediately after the Ethernet header.
    ===========================================================================
    */

    struct iphdr *ipv4_header =
        (void *)(ethernet_header + 1);


    /*
     * Make sure at least one minimum IPv4 header exists.
     *
     * ipv4_header + 1 moves forward by:
     *
     *     sizeof(struct iphdr)
     *
     * which is normally 20 bytes.
     */
    if ((void *)(ipv4_header + 1) > packet_end) {
        return XDP_PASS;
    }


    /*
     * Although the Ethernet EtherType says IPv4, verify that the
     * version field inside the header also says version 4.
     */
    if (ipv4_header->version != 4) {
        return XDP_PASS;
    }


    /*
     * ihl means Internet Header Length.
     *
     * It is measured in groups of four bytes.
     *
     * Examples:
     *
     *     ihl = 5
     *     5 × 4 = 20 bytes
     *
     *     ihl = 6
     *     6 × 4 = 24 bytes
     *
     * The minimum valid IPv4 Internet Header Length is 5.
     */
    if (ipv4_header->ihl < 5) {
        return XDP_PASS;
    }


    __u32 ipv4_header_length_bytes =
        (__u32)ipv4_header->ihl * 4;


    /*
     * Confirm that the complete variable-length IPv4 header exists.
     *
     * IPv4 headers may contain optional fields, so their length is
     * not always exactly 20 bytes.
     *
     * ipv4_header
     *      │
     *      ▼
     *      [---------- IPv4 header ----------][ next header ]
     *                                          ▲
     *                                          │
     *                ipv4_header + header length
     */
    if (
        (void *)ipv4_header + ipv4_header_length_bytes
        > packet_end
    ) {
        return XDP_PASS;
    }


    /*
    ===========================================================================
    STEP 4: READ SOURCE AND DESTINATION IPv4 ADDRESSES
    ===========================================================================
    */

    // saddr means source address.
    __u32 source_ipv4_address =
        ipv4_header->saddr;

    // daddr means destination address.
    __u32 destination_ipv4_address =
        ipv4_header->daddr;


    /*
    ===========================================================================
    STEP 5: UPDATE THE SOURCE PACKET COUNTER
    ===========================================================================

    Map:

        source IPv4 address ───────────────► packet count

    Example:

        Before packet:
            192.168.1.10 ────────────────► 25

        After packet:
            192.168.1.10 ────────────────► 26
    ===========================================================================
    */

    /*
     * Search for this source IPv4 address in the BPF hash map.
     *
     * &packet_count_by_source_ipv4
     *     Address/reference to the map.
     *
     * &source_ipv4_address
     *     Address of the key being searched.
     *
     * Return value:
     *
     *     pointer to counter  → key exists
     *     NULL                → key does not exist
     */
    __u64 *existing_packet_count_pointer =
        bpf_map_lookup_elem(
            &packet_count_by_source_ipv4,
            &source_ipv4_address
        );


    /*
     * Ternary operator:
     *
     *     condition ? value_when_true : value_when_false
     *
     * This:
     *
     *     existing_packet_count_pointer
     *         ? (*existing_packet_count_pointer + 1)
     *         : 1
     *
     * means:
     *
     *     if the source already exists:
     *         new count = previous count + 1
     *
     *     otherwise:
     *         new count = 1
     */
    __u64 updated_packet_count =
        existing_packet_count_pointer
            ? (*existing_packet_count_pointer + 1)
            : 1;


    /*
     * Store the updated value.
     *
     * BPF_ANY means:
     *
     *     Insert the key if it does not exist.
     *     Replace the value if the key already exists.
     */
    bpf_map_update_elem(
        &packet_count_by_source_ipv4,
        &source_ipv4_address,
        &updated_packet_count,
        BPF_ANY
    );


    /*
    ===========================================================================
    STEP 6: OPTIONAL PACKET DROP
    ===========================================================================

    Warning:

    This is only a demonstration threshold.

    It currently means:

        More than 500 packets during the map entry's entire lifetime

    It does not mean:

        More than 500 packets per second
    ===========================================================================
    */

    if (
        updated_packet_count
        > DEMO_PACKET_LIMIT_PER_SOURCE
    ) {
        /*
         * XDP_DROP means:
         *
         *     Discard the packet immediately.
         *
         * The packet will not continue into the normal Linux
         * network stack.
         */
        return XDP_DROP;
    }


    /*
    ===========================================================================
    STEP 7: RESERVE SPACE IN THE RING BUFFER
    ===========================================================================

    The ring buffer contains space for packet_event structures.

        Kernel
          │
          │ reserve memory
          ▼
        [ packet_event slot ]
          │
          │ fill fields
          ▼
        submit event
          │
          ▼
        Userspace reads it
    ===========================================================================
    */

    struct packet_event *reserved_packet_event =
        bpf_ringbuf_reserve(
            &packet_events_to_userspace,
            sizeof(*reserved_packet_event),
            0
        );


    /*
     * Reservation can fail when the ring buffer is full.
     *
     * If it fails:
     *
     *     reserved_packet_event == NULL
     */
    if (reserved_packet_event) {
        /*
         * Initialize every field before submitting the event.
         *
         * This avoids accidentally sending old or uninitialized values.
         */

        reserved_packet_event->source_ipv4_address =
            source_ipv4_address;

        reserved_packet_event->destination_ipv4_address =
            destination_ipv4_address;

        reserved_packet_event->packet_length_bytes =
            (__u32)(
                packet_context->data_end
                - packet_context->data
            );

        reserved_packet_event->source_port = 0;
        reserved_packet_event->destination_port = 0;

        reserved_packet_event->transport_protocol =
            ipv4_header->protocol;

        reserved_packet_event->reserved_padding[0] = 0;
        reserved_packet_event->reserved_padding[1] = 0;
        reserved_packet_event->reserved_padding[2] = 0;


        /*
        =======================================================================
        STEP 8: LOCATE THE TRANSPORT HEADER
        =======================================================================

        Transport protocols include:

            TCP = Transmission Control Protocol
            UDP = User Datagram Protocol

        Packet:

            [ Ethernet ][ IPv4 ][ TCP or UDP ][ Data ]
                                 ▲
                                 │
                       transport_header_start
        =======================================================================
        */

        void *transport_header_start =
            (void *)ipv4_header
            + ipv4_header_length_bytes;


        /*
        =======================================================================
        STEP 9A: PARSE TCP
        =======================================================================
        */

        if (
            ipv4_header->protocol
            == IPPROTO_TCP
        ) {
            /*
             * IPPROTO_TCP means:
             *
             *     Internet Protocol protocol number for
             *     TCP, Transmission Control Protocol.
             *
             * Its protocol number is 6.
             */

            struct tcphdr *tcp_header =
                transport_header_start;


            /*
             * Make sure a complete minimum TCP header exists.
             *
             * tcp_header + 1 moves forward by one complete
             * struct tcphdr.
             */
            if (
                (void *)(tcp_header + 1)
                <= packet_end
            ) {
                /*
                 * TCP port numbers are stored in network byte order.
                 *
                 * bpf_ntohs means:
                 *
                 *     Berkeley Packet Filter
                 *     network-to-host short
                 */

                reserved_packet_event->source_port =
                    bpf_ntohs(tcp_header->source);

                reserved_packet_event->destination_port =
                    bpf_ntohs(tcp_header->dest);
            }
        }


        /*
        =======================================================================
        STEP 9B: PARSE UDP
        =======================================================================
        */

        else if (
            ipv4_header->protocol
            == IPPROTO_UDP
        ) {
            /*
             * IPPROTO_UDP means:
             *
             *     Internet Protocol protocol number for
             *     UDP, User Datagram Protocol.
             *
             * Its protocol number is 17.
             */

            struct udphdr *udp_header =
                transport_header_start;


            /*
             * Make sure the complete UDP header exists.
             */
            if (
                (void *)(udp_header + 1)
                <= packet_end
            ) {
                reserved_packet_event->source_port =
                    bpf_ntohs(udp_header->source);

                reserved_packet_event->destination_port =
                    bpf_ntohs(udp_header->dest);
            }
        }


        /*
        =======================================================================
        STEP 10: SUBMIT THE EVENT
        =======================================================================

        Before submit:

            Kernel owns reserved event memory.

        After submit:

            Userspace is allowed to read the event.

        Do not modify reserved_packet_event after submitting it.
        =======================================================================
        */

        bpf_ringbuf_submit(
            reserved_packet_event,
            0
        );
    }


    /*
     * XDP_PASS means:
     *
     *     Allow the packet to continue into the normal Linux
     *     networking stack.
     */
    return XDP_PASS;
}


/*
===============================================================================
LICENSE DECLARATION
===============================================================================

The Linux kernel reads this value when loading the eBPF program.

GPL means GNU General Public License.

Some BPF helper functions are only available to programs that declare
a GPL-compatible license.
===============================================================================
*/

char program_license[] SEC("license") = "GPL";
