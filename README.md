## Assortment of tools for some recent Insomniac Games titles

This is basically a dumping ground for my stuff, due to people asking for sources, and I don't want to constantly zip them up. May work with Sunset Overdrive, though I've mainly been testing RACPS4 stuff myself.

Still, I would like to document general structure and use, at the least. I'll provide a high-level overview here, but you should read their respective `README`s for more info.

### general
`general` is probably the most interesting, it has some Python (3.4+, due to `Enum`) scripts for extracting, decompressing, building, and (minimally) compressing game files.

### crc
`crc` has some stuff for "bruteforcing" labels from the game (helps with reversing file sections). In C.

### igt
`igt` has (as of now) a C rewrite of the general decompressor. It's a lot faster than the Python version, but it doesn't do much else. And the Python version only takes like two seconds anyway.

## Stuff that needs doing
- Increase `ig_model2obj.py` compatibilty. Will need to reverse more of the vertex structure.
- Expand `igt` with more functionality.
- Remove need for `toc.template` in `ig_build.py`. Will need to edit the script a little bit, but not much.
- Write guides. I am pretty bad at this.
- General streamlining.
- Improve `.ksy` files.