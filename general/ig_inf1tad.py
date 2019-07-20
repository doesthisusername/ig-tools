from sys import argv
import struct #temp

from igdat1 import *

dat1 = Igdat1.from_file(argv[1])

print(dat1.file_type_str)

for top_section in dat1.sections:
    print("{:08X} at {:08X}".format(top_section.type_hash, top_section.ofs_section))

def print_section_r(section, name=None, level=1):
    tabs = "\t" * level

    if name:
        print("\n{}{}:".format("\t" * (level - 1), name))
    else:
        print()

    for sub in section.items:
        for i in range(sub.num_items):
            if type(sub.items.item_values[i]) == dat1.SubSection:
                print_section_r(sub.items.item_values[i], sub.items.item_names[i].name, level + 1)
            elif type(sub.items.item_values[i]) == dat1.StrLit:
                print("{}{}: {}".format(tabs, sub.items.item_names[i].name, sub.items.item_values[i].str))
            elif type(sub.items.item_values[i]) == dat1.ByteF32:
                print("{}{}: {}".format(tabs, sub.items.item_names[i].name, sub.items.item_values[i].value))
            elif type(sub.items.item_values[i]) == dat1.ActorHash:
                print("{}{}: (actor) {}".format(tabs, sub.items.item_names[i].name, sub.items.item_values[i].hash))
            else:
                print("{}{}: {}".format(tabs, sub.items.item_names[i].name, sub.items.item_values[i]))
    

for section in dat1.sections:
    # config built
    if section.type_hash == dat1.Types.config_built.value or section.type_hash == dat1.Types.level_some_data.value:
        print_section_r(section.data)
    elif section.type_hash == 0x50EDC53D:
        for var in section.data.zone_vars:
            print("\n{}:".format(var.name))
            print_section_r(var.data)



'''
buf = None
with open(argv[1], "rb") as f:
    buf = f.read()

last_pos = buf.find(b"\x44\x00\x15\x03")

while last_pos != -1:
    num_items, body_len = struct.unpack_from("<II", buf, last_pos + 4)

    item_types = [None] * num_items
    item_keys = [None] * num_items

    for i in range(num_items):
        key_pos = struct.unpack_from("<I", buf, last_pos + 0x0C + num_items * 8 + i * 4)[0]
        key_end = buf.find(b"\x00", key_pos)

        item_types[i] = struct.unpack_from("<I", buf, last_pos + 0x0C + i * 8 + 4)[0]
        item_keys[i] = buf[key_pos : key_end].decode("ascii")

        print("{}: {:08X}".format(item_keys[i], item_types[i]))

    print("\n{:08X}\n\n".format(last_pos))

    last_pos = buf.find(b"\x44\x00\x15\x03", last_pos + 4)
'''
