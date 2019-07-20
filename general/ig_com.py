from sys import argv
import struct

src_file = None
dst_file = None

# not enough
if len(argv) < 2:
    print("Usage: ig_com.py <decompressed file> [output file]")
    quit()
# no dst file, so use implicit
elif len(argv) == 2:
    src_file = argv[1]
    dst_file = src_file + ".com"
# dst file exists, use that
else:
    src_file = argv[1]
    dst_file = argv[2]

dec = None
with open(src_file, "rb") as decfile:
    dec = decfile.read()

# VERY lazy, just making it one big literal
with open(dst_file, "wb") as comfile:
    comfile.write(dec[4 : 12]) # these bytes are the same
    comfile.write(b"\x00" * 0x1C)

    declen = len(dec)
    comfile.write(struct.pack("<B", 0xF0))
    declen -= 0x0F
    while declen > 0:
        comfile.write(struct.pack("<B", min(declen, 0xFF)))
        declen -= 0xFF
    
    comfile.write(dec)
