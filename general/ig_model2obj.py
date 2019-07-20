#!/usr/bin/python3.5

from sys import argv
from igdat1 import *

dat1 = Igdat1.from_file(argv[1])

verts = []
faces = []
for section in dat1.sections:
    if section.type_hash == dat1.Types.model_index.value:
        for face in section.data.indices:
            faces.append("f {} {} {}".format(face.index_a + 1, face.index_b + 1, face.index_c + 1))
    elif section.type_hash == dat1.Types.model_std_vert.value:
        for vert in section.data.verts:
            verts.append("v {:f} {:f} {:f}".format(vert.unk_00 * 0.0001, vert.unk_04 * 0.0001, vert.unk_02 * 0.0001))

with open("testout.obj", "w") as objf:
    for vert in verts:
        objf.write(vert + "\n")
    
    objf.write("\n")

    for face in faces:
        objf.write(face + "\n")