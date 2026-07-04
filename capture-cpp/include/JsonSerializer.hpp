#pragma once

#include "FlowKey.hpp"
#include "FlowStats.hpp"
#include <string>

class JsonSerializer {
public:
    static std::string toJsonLine(const FlowKey& key, const FlowStats& stats);
};
