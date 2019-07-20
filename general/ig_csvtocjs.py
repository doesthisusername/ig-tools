from sys import argv
import re
import os
import csv
import json

from igtoc import *

src_folder = None
dst_file = None

# not enough
if len(argv) < 2:
    print("Usage: ig_csvtocjs.py <folder with layout.csv, chunkmap.txt, and toc> [output file]")
    quit()
# no dst file, so use implicit
elif len(argv) == 2:
    src_folder = argv[1]
    dst_file = src_folder + os.sep + "toc.json"
# dst file exists, use that
else:
    src_folder = argv[1]
    dst_file = argv[2]

print("Initializing...")
toc = Igtoc.from_file(src_folder + os.sep + "toc").dec_toc

toc_map = dict()
toc_map["meta"] = dict()
toc_map["archives"] = dict()
toc_map["spans"] = []

toc_map["meta"]["real_file_count"] = 0
toc_map["meta"]["full_file_count"] = 0
toc_map["meta"]["key_assets"] = []

print("Adding chunkmaps...")
with open(src_folder + os.sep + "chunkmap.txt", "r") as cmf:
    i = 0
    for line in cmf.readlines():
        if line != "":
            name, chunkmap = line.split(" ", 1)
            toc_map["archives"][name] = dict()
            archive = toc_map["archives"][name]

            archive["index"] = i
            archive["chunkmap"] = int(chunkmap)
            archive["real_file_count"] = 0
            archive["full_file_count"] = 0
            archive["files"] = dict()

            i += 1

print("Reading CSV...")
with open(src_folder + os.sep + "layout.csv", "r") as csvf:
    reader = csv.DictReader(csvf)
    pattern = re.compile(r"0x([\da-fA-F]+)(\.built|\.wem|\.stream)")

    for row in reader:
        match = pattern.search(row["Built Path"])
        if match:
            asset_id = "0x" + match.group(1).upper()
            archive = toc_map["archives"][row["Archive File"]]

            toc_map["meta"]["real_file_count"] += 1
            toc_map["meta"]["full_file_count"] += 1
            archive["real_file_count"] += 1
            archive["full_file_count"] += 1

            if row["Key Asset"] == "Yes":
                toc_map["meta"]["key_assets"].append("0x" + asset_id[-8:])

            archive["files"][asset_id] = row["Asset Path"].strip("\"")

print("Reading spans from toc...")
for span in toc.span_entries:
    span_list = []
    
    for i in range(span.asset_index, span.asset_index + span.count):
        span_list.append("0x{:016X}".format(toc.asset_ids[i].built_hash))

    toc_map["spans"].append(span_list)

print("Done, writing to {}!".format(dst_file))
with open(dst_file, "w") as dstf:
    json.dump(toc_map, dstf, indent=2)
