cmake_minimum_required(VERSION 3.10)
project(flowguard_capture)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

find_package(Threads REQUIRED)

add_executable(flowguard_capture
    src/main.cpp
    src/PacketParser.cpp
    src/FlowAggregator.cpp
    src/JsonSerializer.cpp
    src/FeatureEmitter.cpp
)

target_link_libraries(flowguard_capture pcap Threads::Threads)
