cmake_minimum_required(VERSION 3.10)
project(flowguard_capture)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# Main capture executable
add_executable(flowguard_capture
    src/main.cpp
    src/PacketParser.cpp
    src/FlowAggregator.cpp
    src/JsonSerializer.cpp
    src/FeatureEmitter.cpp
)
target_link_libraries(flowguard_capture pcap)

# Test executables — each test file becomes its own small binary.
# This keeps tests isolated and easy to run individually.
add_executable(test_flow_key
    tests/test_flow_key.cpp
)

add_executable(test_flow_aggregator
    tests/test_flow_aggregator.cpp
    src/FlowAggregator.cpp
    src/JsonSerializer.cpp
    src/FeatureEmitter.cpp
)

add_executable(test_blocking_queue
    tests/test_blocking_queue.cpp
)
target_link_libraries(test_blocking_queue pthread)

# "make test" runs all three at once.
enable_testing()
add_test(NAME FlowKeyTest COMMAND test_flow_key)
add_test(NAME FlowAggregatorTest COMMAND test_flow_aggregator)
add_test(NAME BlockingQueueTest COMMAND test_blocking_queue)
