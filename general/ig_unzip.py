from sys import argv
import zlib

src_file = None
dst_file = None

# not enough
if len(argv) < 2:
    print("Usage: ig_unzip.py <compressed file> [output file]")
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
dec = None
with open(src_file, "rb") as srcf:
    file_type = srcf.read(4)

    if file_type == b"\xAF\x12\xAF\x77":
        print("Detected a \"toc\" file, skipping 8 bytes...")
        srcf.seek(0x08, 0)
    else:
        print("Did not detect a \"toc\" file, skipping 12 bytes...")
        srcf.seek(0x0C, 0)

    com = srcf.read()

with open(dst_file, "wb") as dstf:
    zobj = zlib.decompressobj()
    data = zobj.decompress(com)
    data += zobj.flush()

    dstf.write(data)

print("Done decompressing {}!".format(src_file))