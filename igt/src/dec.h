#pragma once

// performs a single literal + backref decompression operation,
// updating both `*dst` and `*src`.
static inline void dec_op(unsigned char** dst, unsigned char** src);

// decompresses `src` to previously-allocated `dst`,
// with `max` bytes.
void ndec(unsigned char* dst, unsigned char* src, unsigned int max);