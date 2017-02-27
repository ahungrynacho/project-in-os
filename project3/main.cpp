#include <string>
#include <iostream>
#define PM_SIZE 524288
#define BM_SIZE 32
#define INT_SIZE 32

/*

1 byte = 8 bits
unsigned int = 32 bits = 4 bytes range -2 billion to +2 billion

*/

void init_array(int * array, int length, int value) {
    
    for (int i = 0; i < length; ++i) {
        array[i] = value;
    }
}

void init_mask(int * mask0, int * mask1, int length) {
    
    int value = 1;
    for (int i = 0; i < length; ++i) {
        mask1[i] = value;
        mask0[i] = ~mask1[i];
        value = value << 1;
    }
}

int main(int argc, char * argv[]) {
    int physical_mem[PM_SIZE];
    int bit_map[BM_SIZE];
    int mask0[BM_SIZE];
    int mask1[BM_SIZE];
    
    init_array(physical_mem, PM_SIZE, 0);
    init_array(bit_map, BM_SIZE, 0);
    init_mask(mask0, mask1, INT_SIZE);
    
    for (int i = 0; i < BM_SIZE; ++i) {
        std::cout << mask1[i] << " " << mask0[i] << std::endl;
    }
    
    std::string result = Convert.ToString(5, 2).PadLeft(8, '0');
    std::cout << result << std::endl;
    return 0;
}