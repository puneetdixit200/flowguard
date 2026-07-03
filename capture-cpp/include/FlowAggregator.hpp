#pragma once
#include "FlowKey.hpp"
#include "FlowStats.hpp"
#include <map>        

// This class groups packets into flows.
class FlowAggregator {
public:
    void processPacket(const PacketInfo& pkt);
    void printAllFlows() const;

private:
    std::map<FlowKey, FlowStats> flows;
};
