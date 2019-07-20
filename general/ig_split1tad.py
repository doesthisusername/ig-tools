from sys import argv
import os

from igdat1 import *

dat1 = Igdat1.from_file(argv[1])
dat1f = open(argv[1], "rb")

outdir = argv[1].split(".")[0] # bad
os.makedirs(outdir, exist_ok=True)
type_vals = set(item.value for item in dat1.Types)

for section in dat1.sections:
    dat1f.seek(section.ofs_section, 0)

    with open(outdir + os.sep + (dat1.Types(section.type_hash).name if section.type_hash in type_vals else hex(section.type_hash)), "wb") as outf:
        outf.write(dat1f.read(section.len_section))

dat1f.close()
print("Finished!")