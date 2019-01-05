#include <stdio.h>

struct Vector {
    float x;
    float y;
    float z;
};

struct Color {
    unsigned short int red;
    unsigned short int green;
    unsigned short int blue;
};

struct Vertex {
    struct Vector position;
    struct Color color;
};

int main(int argc, char** argv) {
    struct Vertex vertices[] = {
        {.position = {1111.111, 2222.222, 3333.333},
         .color = {150, 222, 17}},
        {.position = {1121.111, 2212.222, 3312.333},
         .color = {50, 212, 217}},
        {.position = {4121.111, 4212.222, 4312.333},
         .color = {31, 110, 41}},
        {.position = {1199.111, 2299.222, 3399.333},
         .color = {219, 119, 49}}};

    FILE* file = fopen("colors.bin", "wb");

    if (file == NULL) {
        return -1;
    }

    fwrite(vertices, sizeof(struct Vertex), 4, file);
    fclose(file);

    return 0;
}