#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dec.h"

#define DAT1_SIZE_POS 0x04
#define DAT1_HDR_SIZE 0x24

int main(int argc, char** argv) {
    if(argc < 2) {
        printf("Please specify a valid operation (choices: dec)\n");
        return 0;
    }

    if(strcmp(argv[1], "dec") == 0) {
        if(argc < 4) {
            printf("The \"dec\" operation requires a source filename argument, as well as a destination filename argument\n");
            return 0;
        }
        
        printf("Preparing to decompress %s...\n", argv[2]);

        // get srcf size, and allocate buffer for it
        FILE* srcf = fopen(argv[2], "rb");
        fseek(srcf, 0, SEEK_END);
        const long src_size = ftell(srcf);
        unsigned char* srcb = malloc(src_size - DAT1_HDR_SIZE);

        // get dst_size, and allocate buffer for it
        fseek(srcf, DAT1_SIZE_POS, SEEK_SET);
        const long dst_size;
        fread((void*)&dst_size, sizeof(dst_size), 1, srcf);
        unsigned char* dstb = malloc(dst_size);

        // read srcf to srcb
        fseek(srcf, DAT1_HDR_SIZE, SEEK_SET);
        fread(srcb, src_size - DAT1_HDR_SIZE, 1, srcf);

        printf("Decompressing... ");
        fflush(stdout);

        // decompress
        ndec(dstb, srcb, dst_size);

        printf("done!\nWriting to %s...\n", argv[3]);

        FILE* dstf = fopen(argv[3], "wb");
        fwrite(dstb, dst_size, 1, dstf);
    }
    else {
        printf("Please specify a valid operation (choices: dec)\n");
    }
    
    return 0;
}