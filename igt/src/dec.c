#include <string.h>
#include "dec.h"

static inline void dec_op(unsigned char** dst, unsigned char** src) {
    unsigned int n_lit = **src >> 4;
    unsigned int n_ref = (**src & 0x0F) + 0x04;
    (*src)++;

    // get literal length
    if(n_lit == 0x0F) {
        do {
            n_lit += **src;
        }
        while(*((*src)++) == 0xFF);
    }

    // do the literal
    memcpy(*dst, *src, n_lit);
    *dst += n_lit;
    *src += n_lit;

    // get backref distance
    const unsigned int ref_dis = *(unsigned short*)*src;
    *src += 2;

    // get backref length
    if(n_ref == 0x0F + 0x04) {
        do {
            n_ref += **src;
        }
        while(*((*src)++) == 0xFF);
    }

    // do the backref
    // can be optimized, but memcpy doesn't really work
    while(n_ref--) {
        **dst = *(*dst - ref_dis);
        (*dst)++;
    }
}

void ndec(unsigned char* dst, unsigned char* src, unsigned int max) {
    const unsigned char* end = dst + max;
    while(dst < end) {
        dec_op(&dst, &src);
    }
}