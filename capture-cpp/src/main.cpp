#include "PacketParser.hpp"
#include "FlowAggregator.hpp"
#include "FeatureEmitter.hpp"
#include "BlockingQueue.hpp"
#include <iostream>
#include <thread>
#include <atomic>
#include <pcap.h>

// This is the concurrency layer your dossier requires:
// capture thread (producer) -> bounded queue -> aggregator thread (consumer). [file:1]
std::atomic<bool> capture_done{false};

void captureThread(const std::string& pcap_path, BlockingQueue<PacketInfo>& queue) {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t* handle = pcap_open_offline(pcap_path.c_str(), errbuf);
    if (!handle) {
        std::cerr << "Failed to open pcap: " << errbuf << "\n";
        capture_done = true;
        return;
    }

    PacketParser parser;
    const u_char* packet;
    struct pcap_pkthdr* header;

    while (true) {
        int result = pcap_next_ex(handle, &header, &packet);
        if (result == 1) {
            auto parsed = parser.parse(header, packet);
            if (parsed.has_value()) {
                queue.push(parsed.value()); // blocks if queue is full
            }
        } else if (result == -2) {
            break; // end of file
        } else if (result == -1) {
            std::cerr << "Read error: " << pcap_geterr(handle) << "\n";
            break;
        }
    }

    pcap_close(handle);
    capture_done = true;
}

void aggregatorThread(BlockingQueue<PacketInfo>& queue, FlowAggregator& aggregator) {
    PacketInfo pkt;
    while (queue.pop(pkt)) {
        aggregator.processPacket(pkt);
    }
}
int main(int argc, char* argv[]) {
    std::string pcap_path = (argc > 1) ? argv[1] : "../data/sample/small_sample.pcap";
    std::string output_path = (argc > 2) ? argv[2] : "../data/flows_output.jsonl";

    std::cout << "Reading: " << pcap_path << "\nWriting: " << output_path << "\n";

    BlockingQueue<PacketInfo> queue(1000);
    FeatureEmitter emitter(output_path);
    FlowAggregator aggregator(emitter);

    std::thread producer(captureThread, pcap_path, std::ref(queue));

    std::thread consumer([&]() {
        PacketInfo pkt;
        while (queue.pop(pkt)) aggregator.processPacket(pkt);
    });

    producer.join();
    queue.shutdown();
    consumer.join();

    aggregator.printAllFlows();
    aggregator.flushAllAsJson();

    std::cout << "\nFlows written to " << output_path << "\n";
    return 0;
}
