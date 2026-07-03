#pragma once
#include <string>
#include <fstream>
#include<mutex>

//write flow json in a file that python will read

class FeatureEmitter {
public:
    explicit FeatureEmitter(const std::string& otput_path);
    void emit(const std::string& json_line);

private:
    std::ofstream out_;
    std::mutex mutex_;
}