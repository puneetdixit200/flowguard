# Builds the C++ packet capture service in an isolated Linux container.
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential cmake libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN mkdir -p build && cd build && cmake .. && make

# The capture binary needs the data folder mounted at runtime for pcap input/output.
CMD ["./build/flowguard_capture"]
