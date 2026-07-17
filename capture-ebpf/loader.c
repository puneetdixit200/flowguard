/*
===============================================================================
XDP USERSPACE LOADER
===============================================================================

This program performs five main jobs:

    1. Receive a network-interface name from the command line.
    2. Open and load the compiled eBPF object file.
    3. Attach the XDP program to the network interface.
    4. Read packet events from the BPF ring buffer.
    5. Detach the XDP program when Ctrl+C is pressed.

Overall flow:

    Network Interface Card
              │
              ▼
       XDP program in kernel
              │
              │ writes packet_event
              ▼
         BPF ring buffer
              │
              ▼
       This userspace program
              │
              ▼
        Terminal / JSON file
===============================================================================
*/


#include <stdio.h>      // printf(), fprintf(), perror()
#include <signal.h>     // signal(), SIGINT, SIGTERM
#include <stdbool.h>    // bool, true, false
#include <errno.h>      // EINTR
#include <string.h>     // strerror()
#include <inttypes.h>   // PRIu32
#include <unistd.h>     // Standard Unix definitions

// Converts binary IPv4 addresses into readable text.
#include <arpa/inet.h>

// Converts network-interface names into interface indexes.
#include <net/if.h>

// Linux fixed-size integer types:
// __u8, __u16, __u32 and __u64.
#include <linux/types.h>

// libbpf functions used to load and control eBPF programs.
#include <bpf/libbpf.h>
#include <bpf/bpf.h>


/*
===============================================================================
CONFIGURATION
===============================================================================
*/

// Compiled eBPF object file.
//
// This file is produced by Clang:
//
//     xdp_filter.bpf.c
//             │
//             ▼
//       xdp_filter.o
#define BPF_OBJECT_FILE_PATH "xdp_filter.o"


// This must exactly match the name of the XDP function
// inside the kernel eBPF source:
//
//     SEC("xdp")
//     int inspect_incoming_packet(...)
#define XDP_PROGRAM_NAME "inspect_incoming_packet"


// This must exactly match the ring-buffer map name
// inside the kernel eBPF source:
//
//     packet_events_to_userspace SEC(".maps")
#define RING_BUFFER_MAP_NAME "packet_events_to_userspace"


/*
===============================================================================
EVENT STRUCTURE
===============================================================================

This structure must exactly match the structure in the kernel eBPF program.

Kernel:

    struct packet_event {
        __u32 source_ipv4_address;
        __u32 destination_ipv4_address;
        __u32 packet_length_bytes;
        __u16 source_port;
        __u16 destination_port;
        __u8  transport_protocol;
        __u8  reserved_padding[3];
    };

Userspace must use the same:

    - field order
    - field type
    - field size
    - padding

Otherwise userspace will interpret the bytes incorrectly.
===============================================================================
*/

struct packet_event {
    // Source IPv4 address stored in network byte order.
    __u32 source_ipv4_address;

    // Destination IPv4 address stored in network byte order.
    __u32 destination_ipv4_address;

    // Complete packet length in bytes.
    __u32 packet_length_bytes;

    // Source TCP or UDP port.
    //
    // The kernel program already converts this to host byte order.
    __u16 source_port;

    // Destination TCP or UDP port.
    __u16 destination_port;

    /*
     * Internet Protocol transport protocol number:
     *
     * 1  = ICMP, Internet Control Message Protocol
     * 6  = TCP, Transmission Control Protocol
     * 17 = UDP, User Datagram Protocol
     */
    __u8 transport_protocol;

    // Explicit padding to keep the memory layout identical.
    __u8 reserved_padding[3];
};


/*
===============================================================================
PROGRAM RUNNING FLAG
===============================================================================

sig_atomic_t is a small integer type that can safely be changed inside
a signal handler.

Initially:

    keep_program_running = 1

When Ctrl+C is pressed:

    keep_program_running = 0

The main loop then stops.
===============================================================================
*/

static volatile sig_atomic_t keep_program_running = 1;


/*
===============================================================================
SIGNAL HANDLER
===============================================================================

Ctrl+C sends:

    SIGINT = Signal Interrupt

The operating system calls this function when SIGINT is received.
===============================================================================
*/

static void handle_shutdown_signal(int signal_number)
{
    // We do not need the actual signal number.
    (void)signal_number;

    // Tell the main polling loop to stop.
    keep_program_running = 0;
}


/*
===============================================================================
RING-BUFFER CALLBACK
===============================================================================

This function is automatically called by libbpf whenever one packet_event
arrives from the kernel ring buffer.

Kernel:

    bpf_ringbuf_submit(event, 0);

             │
             ▼

Userspace:

    handle_packet_event(...)

The callback receives:

    callback_context
        Optional custom data provided by userspace.

    event_data
        Pointer to the event bytes in the ring buffer.

    event_size
        Number of bytes contained in the event.
===============================================================================
*/

static int handle_packet_event(
    void *callback_context,
    void *event_data,
    size_t event_size
)
{
    // No custom callback context is being used.
    (void)callback_context;


    /*
     * Validate that the ring-buffer event contains at least one
     * complete packet_event structure.
     */
    if (event_size < sizeof(struct packet_event)) {
        fprintf(
            stderr,
            "Received an event that is too small: %zu bytes\n",
            event_size
        );

        // Returning zero tells libbpf to continue processing events.
        return 0;
    }


    /*
     * event_data is originally a generic void pointer:
     *
     *     void *event_data
     *
     * We tell C:
     *
     *     Treat the bytes at this address as a packet_event.
     *
     * No event data is copied.
     */
    const struct packet_event *packet =
        (const struct packet_event *)event_data;


    /*
     * struct in_addr is the standard structure used to store
     * one IPv4 address.
     */
    struct in_addr source_address;
    struct in_addr destination_address;


    /*
     * The eBPF program copied ip->saddr and ip->daddr directly.
     *
     * These values are still in network byte order, which is exactly
     * what inet_ntop() expects.
     */
    source_address.s_addr =
        packet->source_ipv4_address;

    destination_address.s_addr =
        packet->destination_ipv4_address;


    /*
     * INET_ADDRSTRLEN provides enough space for an IPv4 address:
     *
     *     255.255.255.255
     *
     * including the final null character.
     */
    char source_address_text[INET_ADDRSTRLEN];
    char destination_address_text[INET_ADDRSTRLEN];


    /*
     * inet_ntop means:
     *
     *     Internet network-to-presentation
     *
     * It converts:
     *
     *     binary IPv4 address
     *
     * into:
     *
     *     readable dotted-decimal text
     *
     * Example:
     *
     *     C0 A8 01 0A
     *          ↓
     *     192.168.1.10
     */
    if (
        inet_ntop(
            AF_INET,
            &source_address,
            source_address_text,
            sizeof(source_address_text)
        ) == NULL
    ) {
        perror("Failed to convert source IPv4 address");
        return 0;
    }


    if (
        inet_ntop(
            AF_INET,
            &destination_address,
            destination_address_text,
            sizeof(destination_address_text)
        ) == NULL
    ) {
        perror("Failed to convert destination IPv4 address");
        return 0;
    }


    /*
     * Print one packet event:
     *
     *     source IP:port -> destination IP:port
     *
     * Example:
     *
     *     192.168.1.10:54321 -> 142.250.183.14:443
     *     protocol=6 length=74
     */
    printf(
        "%s:%u -> %s:%u protocol=%u length=%" PRIu32 "\n",

        source_address_text,
        (unsigned int)packet->source_port,

        destination_address_text,
        (unsigned int)packet->destination_port,

        (unsigned int)packet->transport_protocol,
        packet->packet_length_bytes
    );


    /*
     * Ensure the line is immediately written to the terminal.
     */
    fflush(stdout);


    // Zero means that the event was handled successfully.
    return 0;
}


/*
===============================================================================
MAIN FUNCTION
===============================================================================
*/

int main(int argument_count, char **argument_values)
{
    /*
     * argument_count means the number of command-line arguments.
     *
     * argument_values is an array containing the arguments.
     *
     * Example command:
     *
     *     sudo ./xdp_loader eth0
     *
     * argument_values[0] = "./xdp_loader"
     * argument_values[1] = "eth0"
     */
    if (argument_count != 2) {
        fprintf(
            stderr,
            "Usage: %s <network-interface>\n",
            argument_values[0]
        );

        fprintf(
            stderr,
            "Example: sudo %s eth0\n",
            argument_values[0]
        );

        return 1;
    }


    // Easier-to-understand name for the selected interface.
    const char *network_interface_name =
        argument_values[1];


    /*
    ===========================================================================
    STEP 1: CONVERT INTERFACE NAME TO INTERFACE INDEX
    ===========================================================================

    Linux internally identifies a network interface using a number.

    Example:

        Interface name       Interface index

        lo                   1
        eth0                 2
        wlan0                3

    if_nametoindex() means:

        interface name → interface index
    ===========================================================================
    */

    unsigned int network_interface_index =
        if_nametoindex(network_interface_name);


    // Zero means the interface name was not found.
    if (network_interface_index == 0) {
        fprintf(
            stderr,
            "Unknown network interface: %s\n",
            network_interface_name
        );

        return 1;
    }


    printf(
        "Interface: %s\n"
        "Interface index: %u\n",
        network_interface_name,
        network_interface_index
    );


    /*
     * Variables used during loading and cleanup.
     *
     * They begin as NULL because no resources have been created yet.
     */
    struct bpf_object *bpf_object = NULL;
    struct bpf_program *xdp_program = NULL;
    struct bpf_map *ring_buffer_map = NULL;
    struct ring_buffer *ring_buffer_reader = NULL;

    bool xdp_program_is_attached = false;

    int program_exit_code = 1;


    /*
    ===========================================================================
    STEP 2: OPEN THE COMPILED eBPF OBJECT FILE
    ===========================================================================

    bpf_object__open_file() opens and reads the ELF object file.

    ELF = Executable and Linkable Format.

    At this point, the program is only opened in userspace.

    It has not yet been loaded into the kernel.
    ===========================================================================
    */

    bpf_object =
        bpf_object__open_file(
            BPF_OBJECT_FILE_PATH,
            NULL
        );


    /*
     * libbpf may represent an error using a special pointer.
     *
     * libbpf_get_error() checks whether the returned pointer
     * represents an error.
     */
    long open_error =
        libbpf_get_error(bpf_object);


    if (open_error != 0) {
        fprintf(
            stderr,
            "Failed to open %s: %s\n",
            BPF_OBJECT_FILE_PATH,
            strerror((int)-open_error)
        );

        bpf_object = NULL;
        goto cleanup;
    }


    /*
    ===========================================================================
    STEP 3: LOAD THE eBPF PROGRAM INTO THE KERNEL
    ===========================================================================

    bpf_object__load() performs important operations:

        1. Creates the BPF maps.
        2. Sends the eBPF bytecode to the kernel.
        3. Runs the eBPF verifier.
        4. Loads the program if verification succeeds.

    Flow:

        xdp_filter.o
             │
             ▼
        Linux eBPF verifier
             │
             ├── Unsafe → reject
             │
             └── Safe   → load into kernel
    ===========================================================================
    */

    int load_result =
        bpf_object__load(bpf_object);


    if (load_result < 0) {
        fprintf(
            stderr,
            "Failed to load the eBPF object: %s\n",
            strerror(-load_result)
        );

        goto cleanup;
    }


    /*
    ===========================================================================
    STEP 4: FIND THE XDP PROGRAM
    ===========================================================================

    One ELF object file can contain multiple eBPF programs.

    We search for the function named:

        inspect_incoming_packet
    ===========================================================================
    */

    xdp_program =
        bpf_object__find_program_by_name(
            bpf_object,
            XDP_PROGRAM_NAME
        );


    if (xdp_program == NULL) {
        fprintf(
            stderr,
            "Could not find XDP program: %s\n",
            XDP_PROGRAM_NAME
        );

        goto cleanup;
    }


    /*
     * fd means file descriptor.
     *
     * A file descriptor is a small integer Linux uses to identify
     * an opened kernel resource.
     *
     * Here it identifies the loaded eBPF program.
     */
    int xdp_program_file_descriptor =
        bpf_program__fd(xdp_program);


    if (xdp_program_file_descriptor < 0) {
        fprintf(
            stderr,
            "Could not obtain the XDP program file descriptor.\n"
        );

        goto cleanup;
    }


    /*
    ===========================================================================
    STEP 5: ATTACH THE PROGRAM TO THE NETWORK INTERFACE
    ===========================================================================

    Before attachment:

        Network packet
              │
              ▼
        Normal Linux stack

    After attachment:

        Network packet
              │
              ▼
        XDP program
              │
              ├── XDP_DROP
              └── XDP_PASS
                        │
                        ▼
                  Linux network stack
    ===========================================================================
    */

    int attach_result =
        bpf_xdp_attach(
            network_interface_index,
            xdp_program_file_descriptor,
            0,
            NULL
        );


    if (attach_result < 0) {
        fprintf(
            stderr,
            "Failed to attach the XDP program to %s: %s\n",
            network_interface_name,
            strerror(-attach_result)
        );

        goto cleanup;
    }


    xdp_program_is_attached = true;


    printf(
        "\nXDP program attached to %s.\n"
        "Press Ctrl+C to stop.\n\n",
        network_interface_name
    );


    /*
    ===========================================================================
    STEP 6: FIND THE RING-BUFFER MAP
    ===========================================================================

    This finds the map that the kernel program uses here:

        bpf_ringbuf_reserve(...)
        bpf_ringbuf_submit(...)

    Kernel map name:

        packet_events_to_userspace
    ===========================================================================
    */

    ring_buffer_map =
        bpf_object__find_map_by_name(
            bpf_object,
            RING_BUFFER_MAP_NAME
        );


    if (ring_buffer_map == NULL) {
        fprintf(
            stderr,
            "Could not find ring-buffer map: %s\n",
            RING_BUFFER_MAP_NAME
        );

        goto cleanup;
    }


    /*
     * Obtain the Linux file descriptor representing the ring-buffer map.
     */
    int ring_buffer_map_file_descriptor =
        bpf_map__fd(ring_buffer_map);


    if (ring_buffer_map_file_descriptor < 0) {
        fprintf(
            stderr,
            "Could not obtain the ring-buffer map file descriptor.\n"
        );

        goto cleanup;
    }


    /*
    ===========================================================================
    STEP 7: CREATE A USERSPACE RING-BUFFER READER
    ===========================================================================

    ring_buffer__new() creates a userspace reader.

    It does not create another kernel map.

    It connects this userspace program to the existing kernel map.

    Arguments:

        ring_buffer_map_file_descriptor
            Identifies the kernel ring-buffer map.

        handle_packet_event
            Callback called whenever an event arrives.

        NULL
            No custom callback context.

        NULL
            Use default ring-buffer options.
    ===========================================================================
    */

    ring_buffer_reader =
        ring_buffer__new(
            ring_buffer_map_file_descriptor,
            handle_packet_event,
            NULL,
            NULL
        );


    long ring_buffer_error =
        libbpf_get_error(ring_buffer_reader);


    if (ring_buffer_error != 0) {
        fprintf(
            stderr,
            "Failed to create the ring-buffer reader: %s\n",
            strerror((int)-ring_buffer_error)
        );

        ring_buffer_reader = NULL;
        goto cleanup;
    }


    /*
    ===========================================================================
    STEP 8: REGISTER SIGNAL HANDLERS
    ===========================================================================

    Ctrl+C sends SIGINT.

    SIGTERM may be sent by commands such as:

        kill <process-id>
    ===========================================================================
    */

    signal(SIGINT, handle_shutdown_signal);
    signal(SIGTERM, handle_shutdown_signal);


    /*
    ===========================================================================
    STEP 9: POLL THE RING BUFFER
    ===========================================================================

    Polling loop:

        Wait for events
              │
              ▼
        Event arrives
              │
              ▼
        handle_packet_event() runs
              │
              ▼
        Print event
              │
              ▼
        Wait again

    ring_buffer__poll(..., 100):

        Wait for up to 100 milliseconds.

    It may return sooner when an event arrives.
    ===========================================================================
    */

    while (keep_program_running) {
        int poll_result =
            ring_buffer__poll(
                ring_buffer_reader,
                100
            );


        /*
         * EINTR means:
         *
         *     Interrupted system call
         *
         * This commonly happens when Ctrl+C interrupts the poll.
         */
        if (poll_result == -EINTR) {
            continue;
        }


        if (poll_result < 0) {
            fprintf(
                stderr,
                "Ring-buffer polling failed: %s\n",
                strerror(-poll_result)
            );

            goto cleanup;
        }


        /*
         * poll_result can mean:
         *
         *     0  → timeout; no events arrived
         *     >0 → one or more events were processed
         */
    }


    // The program ended normally.
    program_exit_code = 0;


    /*
    ===========================================================================
    CLEANUP
    ===========================================================================

    Cleanup happens both when:

        - Ctrl+C is pressed
        - an error occurs
    ===========================================================================
    */

cleanup:

    /*
     * Detach the XDP program before closing the object.
     */
    if (xdp_program_is_attached) {
        int detach_result =
            bpf_xdp_detach(
                network_interface_index,
                0,
                NULL
            );


        if (detach_result < 0) {
            fprintf(
                stderr,
                "Failed to detach the XDP program: %s\n",
                strerror(-detach_result)
            );

            program_exit_code = 1;
        } else {
            printf(
                "\nXDP program detached from %s.\n",
                network_interface_name
            );
        }
    }


    /*
     * Free the userspace ring-buffer reader.
     */
    if (ring_buffer_reader != NULL) {
        ring_buffer__free(ring_buffer_reader);
    }


    /*
     * Close the eBPF object and its associated file descriptors.
     */
    if (bpf_object != NULL) {
        bpf_object__close(bpf_object);
    }


    return program_exit_code;
}
