from sys import argv
import os

from igtoc import *

src_folder = None
dst_folder = None

# not enough
if len(argv) < 2:
    print("Usage: ig_tocext.py <toc/assets folder> [output folder]")
    quit()
# no dst folder, so use implicit
elif len(argv) == 2:
    src_folder = argv[1]
    dst_folder = src_folder + os.sep + "built"
# dst folder exists, use that
else:
    src_folder = argv[1]
    dst_folder = argv[2]

print("Initializing...")
toc = Igtoc.from_file("{}{}{}".format(src_folder, os.sep, "toc")).dec_toc

index_map = [0] * len(toc.sizes)
real_file_count = 0
full_file_count = 0

# fill index map, as the offsets section has more items than the rest
i = 0
print("Populating index map and counting files...")
for size_entry in toc.sizes:
    # `file_ctr` corresponds to the offsets section; `i` everything else
    index_map[i] = size_entry.file_ctr
    real_file_count += 1
    full_file_count += size_entry.file_ctr_inc
    i += 1

print("Writing files from archives (this will take a while!)...")
os.makedirs(dst_folder, exist_ok=True)

non_existent_arcs = []
cur_arc_idx = -1
cur_arc = None
for i in range(real_file_count):
    if (i & 0x7FF) == 0:
        print("Still working, please hang on tight... ({} out of {})".format(i + 1, real_file_count))

    arc_idx = toc.offsets[index_map[i]].archive_index
    if arc_idx != cur_arc_idx:
        if cur_arc != None:
            cur_arc.close()

        # for example, it still assigns files to a00s010.jp on non-jp versions, without having the archive file
        try:
            cur_arc = open("{}{}{}".format(src_folder, os.sep, toc.archive_files[arc_idx].filename), "rb")
            cur_arc_idx = arc_idx
        except FileNotFoundError:
            if toc.archive_files[arc_idx].filename not in non_existent_arcs:
                non_existent_arcs.append(toc.archive_files[arc_idx].filename)
                print("Warning: {} doesn't actually exist, yet is referenced".format(toc.archive_files[arc_idx].filename))
            continue

    file_size = toc.sizes[i].file_size
    cur_arc.seek(toc.offsets[index_map[i]].archive_offset, 0)

    with open("{}{}0x{:016X}".format(dst_folder, os.sep, toc.asset_ids[i].built_hash), "wb") as f:
        f.write(cur_arc.read(file_size))

if cur_arc != None:
    cur_arc.close()

print("Done!")