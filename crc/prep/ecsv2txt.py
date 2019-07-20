lines = []
outlines = []
with open("eboot.csv", "r") as csvf:
    lines = csvf.readlines()

for line in lines:
    line = line.replace("\"", "").replace("\n", "").replace("_", " ")

    for word in line.split(" "):
        sub_words = []
        last_up = 0
        index = 0
        for char in word:
            if index == 0:
                char = char.upper()
            elif char.isupper():
                sub_words.append(word[last_up : index])
                last_up = index

            index += 1

        sub_words.append(word[last_up : index])

        for sub_word in sub_words:
            if len(sub_word) > 0x10 or len(sub_word) < 2 or not sub_word.isalpha():
                continue

            sub_word = sub_word[0].upper() + sub_word[1:]

            if sub_word in outlines:
                continue
            
            outlines.append(sub_word)


with open("eboot.txt", "w") as txtf:
    for line in sorted(outlines):
        txtf.write(line + "\n")
