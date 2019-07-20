.intel_syntax noprefix
.extern crc32_table

# 0xEDB88320
.global crc32
crc32:
    .start:
        xor     eax, eax
        test    rdi, rdi
        jz      .return
        mov     dl, [rdi]
        mov     esi, 0xEDB88320
        test    dl, dl
        jz      .return
        inc     rdi
        lea     rcx, [crc32_table]

    .loop:
        movzx   edx, dl
        mov     eax, esi
        shr     eax, 0x08
        movzx   esi, sil
        xor     esi, edx
        xor     eax, [rcx + rsi * 4]
        mov     dl, [rdi]
        inc     rdi
        mov     esi, eax
        test    dl, dl
        jnz     .loop

    .return:
        ret
