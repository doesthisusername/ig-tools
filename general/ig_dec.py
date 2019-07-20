#!/usr/bin/python3.5

from sys import argv
import struct

def read08(buffer, offset):
    return struct.unpack("<B", buffer[offset : offset + 1])[0]

def read16(buffer, offset):
    return struct.unpack("<H", buffer[offset : offset + 2])[0]

def read32(buffer, offset):
    return struct.unpack("<I", buffer[offset : offset + 4])[0]

src_file = None
dst_file = None

# not enough
if len(argv) < 2:
    print("Usage: ig_dec.py <compressed file> [output file]")
    quit()
# no dst file, so use implicit
elif len(argv) == 2:
    src_file = argv[1]
    dst_file = src_file + ".dec"
# dst file exists, use that
else:
    src_file = argv[1]
    dst_file = argv[2]

com = None
with open(src_file, "rb") as comfile:
    com = comfile.read()

dec_size = read32(com, 0x04)
dec = bytearray(dec_size)

dec_i = 0x00
com_i = 0x24

token_a = None
token_b = None
backref_turn = False # alternate

literal_len = 0
backref_dis = 0
backref_len = 0

next_small = 0

# decompress
while dec_i <= dec_size and com_i < len(com):
    if dec_i >= 0x2A00 and dec_i <= 0x2D00:
        print("{:04X} : {:04X}".format(com_i, dec_i))

    token_a = read08(com, com_i)
    com_i += 1

    if not backref_turn:
        if (token_a & 0xF0) == 0xF0:
            token_b = read08(com, com_i)
            com_i += 1
        else:
            token_b = 0
    else:
        token_b = read08(com, com_i)
        com_i += 1

    # literal
    if not backref_turn:
        literal_len = (token_a >> 4) + token_b

        # add on for each 0xFF
        while literal_len >= 0x10E and (literal_len - 0x0F) % 0xFF == 0:
            literal_len += read08(com, com_i)
            com_i += 1
            
            # todo: implement more gracefully
            if read08(com, com_i - 1) == 0x00:
                break

        dec[dec_i : dec_i + literal_len] = com[com_i : com_i + literal_len]
        print("Made a literal of size {:02X} ({})".format(literal_len, dec[dec_i : dec_i + literal_len]))

        com_i += literal_len
        dec_i += literal_len

        backref_len = (token_a & 0x0F) + 4
    # backref
    else:
        backref_dis = token_a + (token_b << 8)

        # 0x0F + 4
        if backref_len == 0x13:
            backref_len += read08(com, com_i)
            com_i += 1

            # add on for each 0xFF
            while backref_len >= 0x112 and (backref_len - 0x13) % 0xFF == 0:
                backref_len += read08(com, com_i)
                com_i += 1

                # todo: implement more gracefully
                if read08(com, com_i - 1) == 0x00:
                    break

        for i in range(backref_len):
            dec[dec_i + i] = dec[dec_i - backref_dis + i]

        #print("Copied {:02X} from {:04X}".format(backref_len, backref_dis))
        
        dec_i += backref_len

    # alternate
    backref_turn = not backref_turn

# write results
with open(dst_file, "wb") as decfile:
    decfile.write(dec)

print("Done, wrote to {}!".format(dst_file))