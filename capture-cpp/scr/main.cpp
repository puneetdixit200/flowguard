#include "PacketParser.hpp"
#include "FlowAggregator.hpp"
#include "BlockingQueue.hpp"
#include "FeatureEmitter.hpp"
#include <iostream>
#include <pcap>
#include <atomic>
#include <thread>



// This is the concurrency layer your dossier requires:
// capture thread (producer) -> bounded queue -> aggregator thread (consumer). [file:1]

std::atomic<bool> capture_done{false};

void captureThread(const std::string& pcap_path,BlockingQueue<PacketInfo>& queue){
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t* handle = pcap_open_offline(pcap_path.c_str(),errbuf);
    if(!handle){
        std::cerr << "Failed to open file: " << errbuf << "\n";
        capture_done= true;
        return;
    }

    PacketParser parser;
    const u_char*packet;
    struct pcap_pkthdr* header;
    while (true){
        int result = pcap_next_ex(handle,&header,&packet);
        if(result == 1){
            auto parsed = parser.parse(header,packet);
            if(parsed.has_value()){
                queue.push(parsed.value());
            }
        }else if(result == -2){
            break;    //end of file
        }else if(result == -1){
            std::cerr << "Error reading packet: " << pcap_geterr(handle) << "\n";
            break;
        }
    }
    pcap_close(handle);
    capture_done = true;
}

void aggregator_Thread(BlockingQueue<PacketInfo>& queue , FlowAggregator& aggregator){
    PacketInfo pkt;
    while(queue.pop(pkt)){
        aggregator.processPacket(pkt);
    }
}

int main() {

    const char* pcap_path ="../data/sample/small_sample.pcap";
    const std::string output_path = "../data/flows_output.jsonl";


    pcap_t* handle =pcap_oprn_offline(pcap_path,errbuf);
    if(!handle){
        std::cerr <<"Failed to open file" <<errbuf << "\n";
        return 1;
    }
    PacketParser parser;
    FlowAggregator aggregator;

    const u_char* packet;
    struct pcap_pkthdr* header;

    while(true){
        int result = pcap_next_ex(handle,&header,&packet);
        if(result == 1){
            auto parsed =parsed.parse(header,packet);
            if(parsed.has_value()){
                aggregator.processPacket(parsed.value());
            }
        }
        else if(result == -2) break; //end of the file
        else if(result == -1) {
            std::cerr << "Error reading packet: " << pcap_geterr(handle) << "\n";
            return 1;
        }
    }
    pcap_close(handle);
    aggregator.printAllFlows();
    return 0;
}
