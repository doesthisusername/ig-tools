## crc find
This is an attempt at a bruteforcer for the numerous strings whose only remnants are their hashes (`CRC32`).

Never use `find_words.py` unless you're prepared to modify it, and to wait between ten and a hundred times as long. Maybe even longer.

### Building
First, read `prep`'s [README](../prep/README.md) if you haven't already, and follow those instructions. You should then copy the resultant text files to this directory, and create a `hashes.txt` with a list of target hashes (`%08X` on each line, with just `\n` line endings).

You can then build the bruteforcer with `make`, hopefully. If it doesn't work, try removing the `-fopenmp` flag.

By default, it will copy `.txt` (using `--update`) files to the output directory as well, as `make clean` will delete the entire output directory.

### Usage
- `./find_words` (no arguments, however it expects `eboot.txt` and `hashes.txt` in the current working directory)
- `./find_words <string>` calculates the `CRC32` for the specified string

Some collisions will happen, so if a result sounds weird, it probably is.