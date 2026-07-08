#include "FlowKey.hpp"
#include<cassert>
#include <iostream>

void test_flow_key_equality() {
    FlowKey a{"10.0.0.1","10.0.0.2",1234,80,"TCP"};
    FlowKey b{"10.0.0.1","10.0.0.2",1234,80,"TCP"};
    FlowKey c{"10.0.0.1","10.0.0.2",1234,443,"TCP"};

    // Same 5-tuple must compare equal under operator< (neither a<b nor b<a).
    assert(!(a < b) && !(b < a));
    // Different port must make them distinct keys.
    assert((a < c) || (c < a));

    std::cout << "test_flow_key_equality PASSED\n";
}


int main() {
    test_flow_key_equality();
    return 0;
}
