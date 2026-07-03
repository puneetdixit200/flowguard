cmake_minimum_required(VERSION 3.1)
project(flowguard_capture)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(flowguard_capture 
    src/main.cpp
    src/PacketParser.cpp
    src/FlowGuard.cpp
)

target_link_libraries(flowguard_capture pcap)

