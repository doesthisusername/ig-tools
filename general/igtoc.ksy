meta:
  id: igtoc
  title: IG TOC
  encoding: ASCII
  endian: le
seq:
  - id: magic
    contents: [0xAF, 0x12, 0xAF, 0x77]
  - id: len_decompressed
    type: u4
  - id: dec_toc
    size-eos: true
    type: toc
    process: zlib
types:
  header_section:
    seq:
      - id: const_hash
        type: u4
      - id: offset
        type: u4
      - id: len
        type: u4
  span_entry:
    seq:
      - id: asset_index
        type: u4
      - id: count
        type: u4
  archive_file:
    seq:
      - id: unknown_00
        type: u2
      - id: install_bucket
        type: u1
      - id: unknown_03
        type: u1
      - id: chunkmap
        type: u4
      - id: filename
        type: strz
      - id: unknown_10
        size-eos: true
  asset_id:
    seq:
      - id: built_hash
        type: u8
  key_asset:
    seq:
      - id: asset_id_lo
        type: u4
  size_entry:
    seq:
      - id: file_ctr_inc
        type: u4
      - id: file_size
        type: u4
      - id: file_ctr
        type: u4
  offset_entry:
    seq:
      - id: archive_index
        type: u4
      - id: archive_offset
        type: u4
  toc:
    seq:
      - id: dat1
        contents: '1TAD'
      - id: toc_const
        type: u4
      - id: len_file
        type: u4
      - id: num_sections
        type: u4
      - id: archive_files_hdr
        type: header_section
      - id: asset_ids_hdr
        type: header_section
      - id: sizes_hdr
        type: header_section
      - id: key_assets_hdr
        type: header_section
      - id: offsets_hdr
        type: header_section
      - id: spans_hdr
        type: header_section
      - id: file_type_str
        type: strz
    instances:
      archive_files:
        pos: archive_files_hdr.offset
        type: archive_file
        size: 0x18
        repeat: expr
        repeat-expr: archive_files_hdr.len / 0x18
      span_entries:
        pos: spans_hdr.offset
        type: span_entry
        size: 0x08
        repeat: expr
        repeat-expr: spans_hdr.len / 0x08
      asset_ids:
        pos: asset_ids_hdr.offset
        type: asset_id
        size: 0x08
        repeat: expr
        repeat-expr: asset_ids_hdr.len / 0x08
      key_assets:
        pos: key_assets_hdr.offset
        type: key_asset
        size: 0x04
        repeat: expr
        repeat-expr: key_assets_hdr.len / 0x04
      sizes:
        pos: sizes_hdr.offset
        type: size_entry
        size: 0x0C
        repeat: expr
        repeat-expr: sizes_hdr.len / 0x0C
      offsets:
        pos: offsets_hdr.offset
        type: offset_entry
        size: 0x08
        repeat: expr
        repeat-expr: offsets_hdr.len / 0x08
