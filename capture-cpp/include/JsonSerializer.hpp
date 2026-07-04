#pragma once
#include "FlowKey.hpp"
#include "FlowStats.hpp"
#include <string>



// Converts one flow (key + stats) into a single JSON line.

class JsonSerializer {
public:
    static std::string toJson(const FlowKey& key , const FlowStats &stats);
};
