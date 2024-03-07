#include <stdio.h>
#include <assert.h>

// Unit 1: Function to add two numbers
int add(int a, int b) {
    return a + b;
}

// Unit 2: Function to subtract two numbers
int subtract(int a, int b) {
    return a - b;
}

// Test function for addition
void test_addition() {
    int result = add(5, 3);
    assert(result == 8);
}

// Test function for subtraction
void test_subtraction() {
    int result = subtract(10, 7);
    assert(result == 3);
}

int main() {
    // Run tests
    test_addition();
    test_subtraction();
    
    printf("All tests passed.\n");
    
    return 0;
}

