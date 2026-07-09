// Tests that BlockingQueue blocks when full and unblocks on pop.
// Per dossier: "queue blocks when full" is a required concurrency test. [file:1]
#include "BlockingQueue.hpp"
#include <cassert>
#include <iostream>
#include <thread>
#include <chrono>

void test_queue_blocks_when_full() {
    BlockingQueue<int> queue(2); // capacity of 2

    queue.push(1);
    queue.push(2);

    bool third_push_completed = false;

    // This push should BLOCK because the queue is full.
    // We run it on a separate thread so we can prove it's still blocked
    // after a short sleep, then unblock it by popping.
    std::thread pusher([&]() {
        queue.push(3);
        third_push_completed = true;
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    assert(!third_push_completed); // must still be blocked

    int value;
    queue.pop(value); // frees one slot, unblocks the pusher thread
    pusher.join();

    assert(third_push_completed); // now it should have completed
    std::cout << "test_queue_blocks_when_full PASSED\n";
}

int main() {
    test_queue_blocks_when_full();
    return 0;
}
