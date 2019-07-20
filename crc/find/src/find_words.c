#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HASH_FILE "hashes.txt"
#define WORD_FILE "eboot.txt"

extern unsigned int crc32(const unsigned char* str);
char test_str[0x80];

// USE_FORCE_FIRST effectively allows you to narrow down the search a lot, while still getting most useful results
//#define USE_FORCE_FIRST 1
#ifdef USE_FORCE_FIRST
#define FORCED_FIRST_LEN 16
char forced_first[FORCED_FIRST_LEN][0x10] = {
    "Actor",
    "Built",
    "Config",
    "Level",
    "Model",
    "Object",
    "Zone",
    "Save",
    "Physics",
    "Asset",
    "Light",
    "Texture",
    "Conduit",  
    "Animset",
    "Anim",
    "Cinematic"
};
#endif

int main(int argc, char** argv) {
    if(argc > 1) {
        printf("Calculating CRC32 for %s... %08X\n", argv[1], crc32(argv[1]));
        return 0;
    }

    FILE* hashesf = fopen(HASH_FILE, "r");
    FILE* wordsf = fopen(WORD_FILE, "r");

    char* hashbuf = malloc(1024 * 1024);
    char* wordbuf = malloc(1024 * 1024 * 8);

    unsigned int* hashes = malloc(1024);
    char** words = malloc(1024 * 1024 * 8);

    size_t num_hash = 0;
    size_t num_word = 0;

    printf("Populating word list...\n");

    fseek(hashesf, 0, SEEK_END);
    size_t hash_file_size = ftell(hashesf);
    fseek(hashesf, 0, SEEK_SET);
    fread(hashbuf, hash_file_size, 1, hashesf);

    fseek(wordsf, 0, SEEK_END);
    size_t word_file_size = ftell(wordsf);
    fseek(wordsf, 0, SEEK_SET);
    fread(wordbuf, word_file_size, 1, wordsf);

    fclose(hashesf);
    fclose(wordsf);

    // get hashes
    hashes[num_hash++] = strtoul(&hashbuf[0], NULL, 16);

    for(int i = 0; i < hash_file_size - 1; i++) {
        if(hashbuf[i] == '\n') {
            hashbuf[i] = '\0';
            hashes[num_hash++] = strtoul(&hashbuf[++i], NULL, 16);
        }
    }

    // get words
    words[num_word++] = &wordbuf[0];

    for(int i = 0; i < word_file_size - 1; i++) {
        if(wordbuf[i] == '_') {
            wordbuf[i] = ' ';
        }
        else if(wordbuf[i] == '\n') {
            wordbuf[i] = '\0';
            words[num_word++] = &wordbuf[++i];
            if(wordbuf[i] > 0x60) wordbuf[i] -= 0x20; // quick and dirty to capitalize first letter
        }
    }

    printf("\nTrying one word (%zu)...\n", num_word);

    for(int i = 0; i < num_word; i++) {
        const unsigned int wordcrc = crc32(words[i]);

        for(int ii = 0; ii < num_hash; ii++) {
            if(wordcrc == hashes[ii]) {
                printf("%08X == %s\n", hashes[ii], words[i]);
            }
        }
    }

    printf("\nTrying two words (%zu)...\n", num_word * num_word);

    #pragma omp parallel for private(test_str)
#ifndef USE_FORCE_FIRST
    for(int i = 0; i < num_word; i++) {
        const unsigned int word_a_len = strlen(words[i]);
        memcpy(test_str, words[i], word_a_len);
#else
    for(int i = 0; i < FORCED_FIRST_LEN; i++) {
        const unsigned int word_a_len = strlen(forced_first[i]);
        memcpy(test_str, forced_first[i], word_a_len);
#endif
        test_str[word_a_len] = ' ';

        for(int ii = 0; ii < num_word; ii++) {
            strcpy(test_str + word_a_len + 1, words[ii]);
            const unsigned int wordcrc = crc32(test_str);

            for(int iii = 0; iii < num_hash; iii++) {
                if(wordcrc == hashes[iii]) {
                    printf("%08X == %s\n", hashes[iii], test_str);
                }
            }
        }
    }

    printf("\nTrying three words (%zu)...\n", num_word * num_word * num_word);
    
    #pragma omp parallel for private(test_str)
#ifndef USE_FORCE_FIRST
    for(int i = 0; i < num_word; i++) {
        const unsigned int word_a_len = strlen(words[i]);
        memcpy(test_str, words[i], word_a_len);
#else
    for(int i = 0; i < FORCED_FIRST_LEN; i++) {
        const unsigned int word_a_len = strlen(forced_first[i]);
        memcpy(test_str, forced_first[i], word_a_len);
#endif
        test_str[word_a_len] = ' ';

        for(int ii = 0; ii < num_word; ii++) {
            const unsigned int word_b_len = strlen(words[ii]);
            memcpy(test_str + word_a_len + 1, words[ii], word_b_len);
            test_str[word_a_len + 1 + word_b_len] = ' ';

            for(int iii = 0; iii < num_word; iii++) {
                strcpy(test_str + word_a_len + 1 + word_b_len + 1, words[iii]);
                const unsigned int wordcrc = crc32(test_str);

                for(int iiii = 0; iiii < num_hash; iiii++) {
                    if(wordcrc == hashes[iiii]) {
                        printf("%08X == %s\n", hashes[iiii], test_str);
                    }
                }
            }
        }
    }

    printf("\nTrying four words (%zu)...\n", num_word * num_word * num_word * num_word);
    
    #pragma omp parallel for private(test_str)
#ifndef USE_FORCE_FIRST
    for(int i = 0; i < num_word; i++) {
        const unsigned int word_a_len = strlen(words[i]);
        memcpy(test_str, words[i], word_a_len);
#else
    for(int i = 0; i < FORCED_FIRST_LEN; i++) {
        const unsigned int word_a_len = strlen(forced_first[i]);
        memcpy(test_str, forced_first[i], word_a_len);
#endif
        test_str[word_a_len] = ' ';

        for(int ii = 0; ii < num_word; ii++) {
            const unsigned int word_b_len = strlen(words[ii]);
            memcpy(test_str + word_a_len + 1, words[ii], word_b_len);
            test_str[word_a_len + 1 + word_b_len] = ' ';

            for(int iii = 0; iii < num_word; iii++) {
                const unsigned int word_c_len = strlen(words[iii]);
                memcpy(test_str + word_a_len + 1 + word_b_len + 1, words[iii], word_c_len);
                test_str[word_a_len + 1 + word_b_len + 1 + word_c_len] = ' ';
                
                for(int iiii = 0; iiii < num_word; iiii++) {
                    strcpy(test_str + word_a_len + 1 + word_b_len + 1 + word_c_len + 1, words[iiii]);
                    const unsigned int wordcrc = crc32(test_str);

                    for(int iiiii = 0; iiiii < num_hash; iiiii++) {
                        if(wordcrc == hashes[iiiii]) {
                            printf("%08X == %s\n", hashes[iiiii], test_str);
                        }
                    }
                }
            }
        }
    }

    printf("Done!\n");
}