from sys import argv
import json

from igtoc import *

src_file = None
dst_file = None

# not enough
if len(argv) < 2:
    print("Usage: ig_tocjs.py <toc> [output file]")
    quit()
# no dst file, so use implicit
elif len(argv) == 2:
    src_file = argv[1]
    dst_file = src_file + ".json"
# dst file exists, use that
else:
    src_file = argv[1]
    dst_file = argv[2]

print("Initializing...")
toc = Igtoc.from_file(src_file).dec_toc

for archive in toc.archive_files:
    print("{}: {:04X}-{:02X}-{:02X}".format(archive.filename, archive.unknown_00, archive.install_bucket, archive.unknown_03))
quit()

full_archive_counts = [0] * len(toc.archive_files)
real_archive_counts = [0] * len(toc.archive_files)
index_map = [0] * len(toc.sizes)

toc_map = dict()
toc_map["meta"] = dict()
toc_map["archives"] = dict()

toc_map["meta"]["real_file_count"] = 0
toc_map["meta"]["full_file_count"] = 0
toc_map["meta"]["key_assets"] = []

# fill index map, as the offsets section has more items than the rest
i = 0
print("Populating index map and counting files...")
for size_entry in toc.sizes:
    # `file_ctr` corresponds to the offsets section; `i` everything else
    index_map[i] = size_entry.file_ctr
    real_archive_counts[toc.offsets[size_entry.file_ctr].archive_index] += 1
    full_archive_counts[toc.offsets[size_entry.file_ctr].archive_index] += size_entry.file_ctr_inc
    i += 1

i = 0
print("Creating archive entries...")
for archive in toc.archive_files:
    toc_map["archives"][archive.filename] = dict()
    arc = toc_map["archives"][archive.filename]

    arc["index"] = i
    arc["chunkmap"] = archive.chunkmap
    arc["real_file_count"] = real_archive_counts[arc["index"]]
    arc["full_file_count"] = full_archive_counts[arc["index"]]
    arc["files"] = []

    toc_map["meta"]["real_file_count"] += arc["real_file_count"]
    toc_map["meta"]["full_file_count"] += arc["full_file_count"]

    i += 1

print("Creating file entries...")
for i in range(len(toc.asset_ids)):
    archive_idx = toc.offsets[index_map[i]].archive_index
    toc_map["archives"][toc.archive_files[archive_idx].filename]["files"].append("0x{:016X}".format(toc.asset_ids[i].built_hash))

print("Adding key assets...")
for key_asset in toc.key_assets:
    toc_map["meta"]["key_assets"].append("0x{:08X}".format(key_asset.asset_id_lo))

import os
tocf = open(src_file, "rb")
os.makedirs("toc_out")
for span in toc.span_entries:
    if span.count == 0:
        continue 
        
    with open("toc_out\\{:08X}_{:08X}".format(span.asset_index, span.count), "wb") as f:
        tocf.seek(toc.asset_ids_hdr.offset + span.asset_index * 8, 0)
        f.write(tocf.read(span.count * 8))

tocf.close()
quit()
print("Writing to file...")
with open(dst_file, "w") as dstf:
    json.dump(toc_map, dstf, indent=2)
