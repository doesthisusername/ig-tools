'''
please never use this, it's outdated and orders of magnitude slower than the C version
'''

import subprocess

hashes = []
with open("target_hashes.txt", "r") as target:
    hashes = target.readlines()

for i in range(len(hashes)):
    hashes[i] = hashes[i].rstrip()

words = []
with open("english.txt", "r") as english:
    words = english.readlines()

# try single words
print("Trying one word")
for word in words:
    test = word.rstrip().replace("_", " ").title()
    result = subprocess.run(["./crc32", test], stdout=subprocess.PIPE).stdout.decode().rstrip()

    if result in hashes:
        print("{} from {}".format(result, test))

# try two words
print("Trying two words")
for word_a in words:
    for word_b in words:
        test = (word_a.rstrip().replace("_", " ") + " " + word_b.rstrip().replace("_", " ")).title()
        result = subprocess.run(["./crc32", test], stdout=subprocess.PIPE).stdout.decode().rstrip()

        if result in hashes:
            print("{} from {}".format(result, test))

# Try three words (never gonna finish lol)
print("Trying three words")
for word_a in words:
    for word_b in words:
        for word_c in words:
            test = (word_a.rstrip().replace("_", " ") + " " + word_b.rstrip().replace("_", " ") + " " + word_c.rstrip().replace("_", " ")).title()
            result = subprocess.run(["./crc32", test], stdout=subprocess.PIPE).stdout.decode().rstrip()

            if result in hashes:
                print("{} from {}".format(result, test))