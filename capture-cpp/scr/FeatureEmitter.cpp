#include "FeatureEmitter.hpp"

FeatureEmitter::FeatureEmitter(const std::string& output_path) {
    //open file in open mode so restrst dont wipe out history
    out_.open(output_path , std::ios::app);
}

void FeatureEmitter::emit(const std::string& json_line) {
    std::lock_guard<std::mutex> lock(mutex_);
    out_ << json_line << std::endl //flush each line so python can read it live
}
