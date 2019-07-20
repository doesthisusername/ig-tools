from sys import argv
import re
import os
import csv

src_folder = None
dst_folder = None

# not enough
if len(argv) < 2:
    print("Usage: ig_csvext.py <csv/assets folder> [output folder]")
    quit()
# no dst folder, so use implicit
elif len(argv) == 2:
    src_folder = argv[1]
    dst_folder = src_folder + os.sep + "built"
# dst folder exists, use that
else:
    src_folder = argv[1]
    dst_folder = argv[2]

print("Writing files from archives (this will take a while!)...")
os.makedirs(dst_folder, exist_ok=True)

non_existent_arcs = []
cur_arc_name = ""
cur_arc = None
i = 0
with open(src_folder + os.sep + "layout.csv", "r") as csvf:
    reader = csv.DictReader(csvf)
    pattern = re.compile(r"0x([\da-fA-F]+)(\.built|\.wem|\.stream)")

    for row in reader:
        match = pattern.search(row["Built Path"])
        if match:
            asset_id = "0x" + match.group(1).upper()
            archive = row["Archive File"]
            archive_ofs = int(row["Segment Offset"])
            file_size = int(row["File Size"])
            asset_name = row["Asset Path"].strip("\"")

            if archive != cur_arc_name:
                if cur_arc != None:
                    cur_arc.close()

                # for example, it still assigns files to a00s010.jp on non-jp versions, without having the archive file
                try:
                    cur_arc = open(src_folder + os.sep + archive, "rb")
                    cur_arc_name = archive
                except FileNotFoundError:
                    if archive not in non_existent_arcs:
                        non_existent_arcs.append(archive)
                        print("Warning: {} doesn't actually exist, yet is referenced".format(archive))
                    continue

            if (i & 0x7FF) == 0:
                print("Still working, please hang on tight... ({} out of probably 250000 or so)".format(i + 1))

            cur_arc.seek(archive_ofs, 0)

            folder_name, file_name = os.path.split(asset_name)
            os.makedirs(dst_folder + os.sep + folder_name, exist_ok=True)

            with open(dst_folder + os.sep + asset_name, "wb") as f:
                f.write(cur_arc.read(file_size))

            i += 1

if cur_arc != None:
    cur_arc.close()

print("Done, wrote {} files!".format(i))