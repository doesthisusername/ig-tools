from sys import argv
import struct
import zlib

src_file = None
dst_file = None

# not enough
if len(argv) < 2:
    print("Usage: ig_zip.py <decompressed file> [output file]")
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
com = None
file_type = ""

with open(src_file, "rb") as srcf:
    srcf.seek(0x58, 0)
    if srcf.read(10).decode() == "ArchiveTOC":
        file_type = "toc"
    else:
        file_type = "dag"

    srcf.seek(0x00, 0)
    dec = srcf.read()

with open(dst_file, "wb") as dstf:
    zobj = zlib.compressobj(9)
    data = zobj.compress(dec)
    data += zobj.flush()

    if file_type == "toc":
        print("Detected a \"toc\" file, writing toc header...")
        dstf.write(struct.pack("<II", 0x77AF12AF, len(dec))) # magic, decompressed length
    # assume dag
    else:
        print("Did not detect a \"toc\" file, writing dag header...")
        dstf.write(struct.pack("<III", 0x891F77AF, len(dec), len(data))) # magic, decompressed length, compressed length

    dstf.write(data)

print("Done compressing {}!".format(src_file))
