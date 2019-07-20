## crc prep
This is the preparer for `crc find`. Its purpose is to modify and filter a CSV of strings, `eboot.csv`, to `eboot.txt`, such that obvious non-words are removed, and to be easier to parse.

`eboot.csv` can be created by exporting the `String View` column from the strings view in [Ghidra](https://ghidra-sre.org).

### Usage
`./ecsv2txt.py` (there are no arguments).