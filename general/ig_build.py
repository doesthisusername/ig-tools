from sys import argv
import struct
import json
import os

src_file = None
built_folder = None
output_folder = None
all_archives = False
archive_name = ""

# slower than it could be, but it's used so sparsely
def align(barray, alignment):
    pos = len(barray)
    while pos % alignment != 0:
        barray += b"\x00"
        pos += 1

# not enough
if len(argv) < 4:
    print("Usage: ig_build.py <toc.json file> <built folder> <output folder> [archive = all | toc | <archive name>]")
    quit()
# no archive specified, assume all
elif len(argv) == 4:
    src_file = argv[1]
    built_folder = argv[2]
    output_folder = argv[3]
    all_archives = True
    archive_name = "all"
    print("All archives specified, creating a new toc\n")
# archive specified, use it
else:
    src_file = argv[1]
    built_folder = argv[2]
    output_folder = argv[3]
    archive_name = argv[4]

    if archive_name == "toc":
        print("Archive not specified, creating a new toc\n")
        all_archives = True
    elif archive_name == "all":
        print("All archives specified, creating a new toc\n")
        all_archives = True
    else:
        print("Archive specified, updating toc to the best of my ability\n")

# load json
jsonf = open(src_file, "r")
tocjs = json.load(jsonf)
jsonf.close()

# build per-section, then join together at the end
spans_section = bytearray()
asset_id_section = bytearray()
key_assets_section = bytearray()
offsets_section = bytearray()
sizes_section = bytearray()
archives_section = bytearray()

# so we can iterate the same way
archive_names = tocjs["archives"].keys() if all_archives else [archive_name]

asset_to_arcidx = dict()
archive_indices = []
archive_map = dict()

# stuff we always want filled
for name in tocjs["archives"].keys():
    archive_indices.append(tocjs["archives"][name]["index"])
    archive_map[tocjs["archives"][name]["index"]] = name

    archives_section += struct.pack("<II16s", 0x00000000, tocjs["archives"][name]["chunkmap"], name.encode())

# stuff that's only for the targeted archives
for name in archive_names:
    try:
        for filename in tocjs["archives"][name]["files"].keys():
            asset_to_arcidx[int(filename, base=0)] = tocjs["archives"][name]["index"]

    except KeyError:
        print("Warning: {} doesn't exist in {}!".format(name, src_file))
        quit()

archive_indices.sort()

# intoc, only used when rebuilding a single archive
intoc = None
in_asset_id_pos = None
in_asset_id_len = None
in_sizes_pos = None
in_sizes_len = None
in_offsets_pos = None
in_offsets_len = None
asset_id_map = dict()
if not all_archives:
    intocf = open("{}{}..{}{}".format(built_folder, os.sep, os.sep, "toc"), "rb")
    intoc = bytearray(intocf.read())
    intocf.close()

    # yikes
    in_asset_id_pos, in_asset_id_len, in_sizes_pos, in_sizes_len, in_offsets_pos, in_offsets_len = struct.unpack_from("<II4xII16xII", intoc, 0x20)
    for i in range(in_asset_id_len // 8):
        asset_id_map["0x{:016X}".format(struct.unpack_from("<Q", intoc, in_asset_id_pos + i * 8)[0])] = i

# build archive files first, and build "free" parts of the toc
os.makedirs(output_folder, exist_ok=True)
file_ctr = 0
prev_span_start = 0
prev_asset_id = 0xFFFFFFFFFFFFFFFF
arc_fds = dict()
arc_sizes = dict()

for arcname in archive_names:
    if archive_name != "toc":
        arc_fds[arcname] = open("{}{}{}".format(output_folder, os.sep, arcname), "wb")

    arc_sizes[arcname] = 0

for asset in sorted(asset_to_arcidx.keys()):
    arcname = archive_map[asset_to_arcidx[asset]]
    arc = tocjs["archives"][arcname]

    if archive_name != "toc":
        if (file_ctr & 0xFFF) == 0:
            print("Building... ({} out of {})".format(file_ctr + 1, len(asset_to_arcidx)))
        
        try:
            assetname = "0x{:016X}".format(asset)
            with open("{}{}{}".format(built_folder, os.sep, arc["files"][assetname]), "rb") as f:
                data = f.read()

                if all_archives:
                    asset_id_section += struct.pack("<Q", asset)
                    sizes_section += struct.pack("<III", 0x00000001, len(data), file_ctr)
                    offsets_section += struct.pack("<II", asset_to_arcidx[asset], arc_sizes[arcname])

                    # whether it's a new span (should hopefully never happen)
                    if asset < prev_asset_id:
                        spans_section += struct.pack("<I", file_ctr) if prev_asset_id == 0xFFFFFFFFFFFFFFFF else struct.pack("<II", file_ctr - prev_span_start, file_ctr)
                        prev_span_start = file_ctr

                    prev_asset_id = asset

                elif archive_name != "all":
                    # update offsets and sizes in toc
                    struct.pack_into("<I", intoc, in_sizes_pos + asset_id_map[assetname] * 0x0C + 4, len(data))
                    struct.pack_into("<II", intoc, in_offsets_pos + asset_id_map[assetname] * 0x08, arc["index"], arc_sizes[arcname])
                else:
                    continue

                arc_sizes[arcname] += len(data)
                arc_fds[arcname].write(data)
                file_ctr += 1

        except FileNotFoundError:
            print("Warning: did not find 0x{:016X}, belonging to {}".format(asset, arcname))

    else:
        if (file_ctr & 0xFFF) == 0:
            print("Building... ({} out of {})".format(file_ctr, len(asset_to_arcidx)))

        try:
            assetname = "0x{:016X}".format(asset)
            file_size = os.stat("{}{}{}".format(built_folder, os.sep, arc["files"][assetname])).st_size

            asset_id_section += struct.pack("<Q", asset)
            sizes_section += struct.pack("<III", 0x00000001, file_size, file_ctr)
            offsets_section += struct.pack("<II", asset_to_arcidx[asset], arc_sizes[arcname])

            # whether it's a new span (should hopefully never happen)
            if asset < prev_asset_id:
                spans_section += struct.pack("<I", file_ctr) if prev_asset_id == 0xFFFFFFFFFFFFFFFF else struct.pack("<II", file_ctr - prev_span_start, file_ctr)
                prev_span_start = file_ctr

            arc_sizes[arcname] += file_size
            file_ctr += 1
            prev_asset_id = asset

        except FileNotFoundError:
            print("Warning: did not find 0x{:016X}, belonging to {}".format(asset, arcname))
        
if archive_name != "toc":
    for fd in arc_fds:
        arc_fds[fd].close()

if all_archives:
    # ensure there are enough spans (not sure where the exact threshold is)
    while (len(spans_section) // 8) < 40:
        if len(spans_section) % 8 == 0:
            spans_section += spans_section[-8:]
        else:
            spans_section += struct.pack("<I", file_ctr - prev_span_start)

    # extend last span if needed
    if len(spans_section) % 8 != 0:
        spans_section += struct.pack("<I", file_ctr - prev_span_start)

    # key assets
    for asset in tocjs["meta"]["key_assets"]:
        key_assets_section += struct.pack("<I", int(asset, base=0))

    # toc creation stuff
    print("Creating toc...")
    templatef = open("{}{}..{}{}".format(built_folder, os.sep, os.sep, "toc.template"), "rb")
    template = bytearray(templatef.read())
    templatef.close()

    spans_section_len = len(spans_section)
    asset_id_section_len = len(asset_id_section)
    key_assets_section_len = len(key_assets_section)
    sizes_section_len = len(sizes_section)
    offsets_section_len = len(offsets_section)
    archives_section_len = len(archives_section) # not needed as it's the last section, but it's prettier

    align(spans_section, 0x10)
    align(asset_id_section, 0x10)
    align(key_assets_section, 0x10)
    align(sizes_section, 0x10)
    align(offsets_section, 0x10)

    spans_section_pos = len(template)
    asset_id_section_pos = spans_section_pos + len(spans_section)
    key_assets_section_pos = asset_id_section_pos + len(asset_id_section)
    sizes_section_pos = key_assets_section_pos + len(key_assets_section)
    offsets_section_pos = sizes_section_pos + len(sizes_section)
    archives_section_pos = offsets_section_pos + len(offsets_section)

    struct.pack_into("<II", template, 0x50, spans_section_pos, spans_section_len)
    struct.pack_into("<II", template, 0x20, asset_id_section_pos, asset_id_section_len)
    struct.pack_into("<II", template, 0x38, key_assets_section_pos, key_assets_section_len)
    struct.pack_into("<II", template, 0x2C, sizes_section_pos, sizes_section_len)
    struct.pack_into("<II", template, 0x44, offsets_section_pos, offsets_section_len)
    struct.pack_into("<II", template, 0x14, archives_section_pos, archives_section_len)

    with open("{}{}{}".format(output_folder, os.sep, "toc"), "wb") as tocf:
        tocf.write(template)
        tocf.write(spans_section)
        tocf.write(asset_id_section)
        tocf.write(key_assets_section)
        tocf.write(sizes_section)
        tocf.write(offsets_section)
        tocf.write(archives_section)

        file_size = tocf.tell()
        tocf.seek(0x08, 0)
        tocf.write(struct.pack("<I", file_size))
        
else:
    print("Updating toc...")
    with open("{}{}{}".format(output_folder, os.sep, "toc"), "wb") as tocf:
        # assumes archives section is last...
        toc_size, archives_section_pos = struct.unpack_from("<I8xI", intoc, 0x08)
        
        # remove old
        toc_size -= toc_size - archives_section_pos
        intoc = intoc[:archives_section_pos]
        
        # add new
        intoc += archives_section
        toc_size += len(archives_section)

        struct.pack_into("<I", intoc, 0x08, toc_size)
        struct.pack_into("<I", intoc, 0x18, len(archives_section))
        tocf.write(intoc)

print("Done, finally! Make sure to compress your toc!")