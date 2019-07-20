## general
`general` is the main assortment of scripts here. I cannot guarantee that all of them will always work properly.

### Usage
All the scripts starting with `ig_` are for direct use. `.ksy` and `.py` pairs are for [Kaitai Struct](https://kaitai.io), which you will need for some of them to work (`pip3 install kaitaistruct`). `igtoc.py` may need to be fixed up manually if you re-generate it with `ksc`.

All of the scripts for direct use take arguments, and will print a short usage text when not enough are given. Alternatively, you can just open them in a text editor.

#### ig_build.py
Used to either rebuild the entire set of asset archive files and the `toc`, just the `toc`, or a single archive file, updating offsets in the `toc` as well. May need some fiddling around with to understand. You will need a `toc.template` as well -- just copy the first `0x70` bytes from a `toc` to their own file.

#### ig_com.py
Very minimal compressor for the game's assets (it actually makes the file bigger). Use this to make the game accept your modified asset.

#### ig_csvext.py
Uses `layout.csv` to extract compressed assets from the asset archives. Takes a while to write all of the files.

#### ig_csvjs.py
Uses `layout.csv` and `chunkmap.txt` to create a `toc.json`, which `ig_build.py` uses to rebuild.

#### ig_dec.py
Decompressor for game assets (most files extracted from the big archives).

#### ig_inf1tad.py
Attempts to print some info about a decompressed `.config` file, and some other files too. Quite experimental.

#### ig_model2obj.py
Attempts to create a `.obj` file from a decompressed `.model`. Rarely works properly, but some files are compatible.

#### ig_split1tad.py
Attempts to create split files for every section in a decompressed asset file. Does not have usage text, and I'm too lazy to add it right now.

#### ig_tocext.py
Like `ig_csvext.py`, except it uses a _compressed_ `toc` instead, and won't have actual file names. May be deprecated at some point.

#### ig_tocjs.py
Like `ig_csvjs.py`, except it uses a _compressed_ `toc` instead. May not be compatible with `ig_build.py`.

#### ig_unzip.py
Inflates `toc` or `dag` files. They're pretty much just `zlib` but with a few header bytes.

#### ig_zip.py
Defaltes `toc` or `dag` files. Adds the small amount of required header bytes as mentioned above.