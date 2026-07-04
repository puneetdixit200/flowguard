#pragma once
#include "FlowKey.hpp"
#include "FlowStats.hpp"
#include "FeatureEmitter.hpp"
#include <map>

// Now emits JSON whenever a flow is updated, instead of only printing at the end.
class FlowAggregator {
public:
    explicit FlowAggregator(FeatureEmitter& emitter) : emitter_(emitter) {}

    void processPacket(const PacketInfo& pkt);
    void printAllFlows() const;
    void flushAllAsJson(); // emits every flow as JSON at shutdown

private:
    std::map<FlowKey, FlowStats> flows;
    FeatureEmitter& emitter_;
};
