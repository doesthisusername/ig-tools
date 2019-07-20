meta:
  id: igdat1
  title: 1TAD/DAT1
  application: Ratchet & Clank (PS4), Sunset Overdrive
  encoding: ASCII
  endian: le
seq:
  - id: magic
    contents: '1TAD'
  - id: type_hash
    type: u4
  - id: len_file
    type: u4
  - id: num_sections
    type: u2
  - id: unk_0e
    type: u2
  - id: sections
    type: section
    repeat: expr
    repeat-expr: num_sections
  - id: file_type_str
    type: strz
    size-eos: true
types:
  section:
    seq:
      - id: type_hash
        type: u4
      - id: ofs_section
        type: u4
      - id: len_section
        type: u4
    instances:
      data:
        pos: ofs_section
        size: len_section
        type:
          switch-on: type_hash
          cases:
            #0x06ABCAB2: zone_scene_objects        # Zone Scene Objects
            0x0859863D: model_indices             # Model Index
            0x2236C47A: str_ref_section           # Level Link Names
            0x2BA33702: str_ref_section           # Level Zone Names
            0x2EE91673: sub_section(0x0010)       # ### has to do with save data
            0x339C970E: sub_section(0x0010)       # ### has to do with levels
            0x4130D903: str_ref_section           # Level Region Names
            0x4A128222: sub_section(0x0010)       # Config Type
            0x50EDC53D: zone_var_section          # ### has to do with zone config
            0x58B8558A: str_ref_section           # Config Asset Refs
            0x78684035: str_ref_section           # ### has to do with actors in zones 
            0x7CA7267D: sub_section(0x0010)       # Level Built
            0x9629C287: str_ref_section           # ### has to do with zone physics
            0xA98BE69B: model_std_verts           # Model Std Verts
            0xC6A5905E: str_ref_section           # Zone Model Names
            0xD101A6CC: str_ref_section           # ### str refs in dag
            0xD436A987: sub_section(0x0010)       # ### has to do with save data
            0xDC625B3D: str_ref_section           # Zone Actor Names
            0xE501186F: sub_section(0x0010)       # Config Built
            0xEF8637D5: str_ref_section           # Zone Script Strings

  # a section containing a dictionary of items, including more potential sub-dictionaries
  # used by:
  # ...
  # Config Built
  # Config Type
  # Level Built
  # ...
  sub_section:
    params:
      - id: attr
        type: u2
    seq:
      - id: items
        type: sub_section_item
        repeat: expr
        repeat-expr: (attr & 0x0FF0) >> 4
    doc: A section containing a dictionary of items, including more potential sub-dictionaries.
  sub_section_item:
    seq:
      - id: unk_00
        type: u4
      - id: type_hash
        type: u4
      - id: num_items
        type: u4
      - id: body_size
        type: u4
      - id: items
        type:
          switch-on: type_hash
          cases:
            0x03150044: item_dict # ???
            0x07201969: item_dict # ???
            #_: item_dict
        size: body_size
  
  # a section containing file-relative string offsets
  # used by:
  # ...
  # Config Asset Ref
  # Level Link Names
  # Level Region Names
  # Level Zone Names
  # Zone Actor Names
  # Zone Model Names
  # Zone Script Strings
  # ...
  str_ref_section:
    seq:
      - id: refs
        type: str_ref
        repeat: eos
    doc: A section containing file-relative string offsets.
  str_ref:
    seq:
      - id: ofs_ref
        type: u4
    instances:
      ref:
        io: _root._io
        pos: ofs_ref
        type: strz
        size-eos: true

  zone_var_section:
    seq:
      - id: zone_vars
        type: zone_var
        repeat: eos
  zone_var:
    seq:
      - id: ofs_name
        type: u4
      - id: name_hash
        type: u4
      - id: ofs_data
        type: u4
      - id: len_data
        type: u4
    instances:
      name:
        io: _root._io
        pos: ofs_name
        type: strz
        size-eos: true
      data:
        io: _root._io
        pos: ofs_data
        type: sub_section(0x0010)
        size: len_data

  zone_scene_objects:
    seq:
      - id: scene_objects
        type: scene_object
        repeat: eos
  scene_object:
    seq:
      - id: unk_00
        size: 0x30
      - id: position
        type: vec4
      # todo

  model_indices:
    seq:
      - id: indices
        type: model_index
        repeat: eos
  model_index:
    seq:
      - id: index_a
        type: u2
      - id: index_b
        type: u2
      - id: index_c
        type: u2
  
  model_std_verts:
    seq:
      - id: verts
        type: vert
        repeat: eos
  vert:
    seq:
      - id: unk_00
        type: s2
      - id: unk_02
        type: s2
      - id: unk_04
        type: s2
      - id: unk_06
        type: u2
      - id: unk_08
        type: u4
      - id: unk_0c
        type: u4

  vec4:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
      - id: z
        type: f4
      - id: w
        type: f4

  # ################### #
  # --- basic types --- #
  # ################### #

  # 0000
  byte_f32:
    params:
      - id: attr
        type: u2
    seq:
      - id: value
        type: u1
        repeat: expr
        repeat-expr: (attr & 0x0FF0) >> 4

  # 000A
  str_lit:
    seq:
      - id: align__
        type: align(4)
      - id: len_str
        type: u4
      - id: str_hash
        type: u4
      - id: unk_hash_a
        type: u4
      - id: unk_hash_b
        type: u4
      - id: str
        type: strz
        size: (len_str & ~3) + 4 # align
    
  # 0011
  actor_hash:
    seq:
      - id: hash
        type: u8

  # ################# #
  # --- container --- #
  # ################# #

  item_hdr:
    seq:
      - id: key_hash
        type: u4
      - id: key_attr
        type: u2
      - id: key_type
        type: u2

  item_name:
    seq:
      - id: ofs_name
        type: u4
    instances:
      name:
        io: _root._io
        pos: ofs_name
        type: strz
        size-eos: true

  # ???
  item_dict:
    seq:
      - id: item_hdrs
        type: item_hdr
        repeat: expr
        repeat-expr: _parent.num_items
      - id: item_names
        type: item_name
        repeat: expr
        repeat-expr: _parent.num_items
      - id: item_values
        type:
          switch-on: item_hdrs[_index].key_type
          cases:
            0x1300: sub_section(item_hdrs[_index].key_attr)
            0x1100: actor_hash
            0x0F00: b1 # bool
            0x0D00: sub_section(item_hdrs[_index].key_attr)
            0x0A00: str_lit
            0x0800: f4
            0x0400: s1 # maybe converted to float as well
            0x0200: s4 # may also be u4
            0x0100: u2 # broooo
            0x0000: byte_f32(item_hdrs[_index].key_attr) # byte converted to float at runtime?
            _: u1
        repeat: expr
        repeat-expr: _parent.num_items
      - id: align__
        type: 
          switch-on: item_hdrs.last.key_type
          cases:
            0x0F00: align(2)
            _: align(4)
        if: _parent.num_items > 0

  # ############# #
  # --- dummy --- #
  # ############# #

  align:
    params:
      - id: num
        type: u4
    seq:
      - id: align__
        size: (num - _root._io.pos) % num

# ################### #
# --- helper enum --- #
# ################### #

enums:
  types:
    0x03150044: dict              # exact name unknown
    0x06ABCAB2: zone_scene_objects
    0x06EB7EFC: model_look
    0x0859863D: model_index
    0x0CF58A6E: zone_actor_groups
    0x135832C8: actor_prius_built
    0x15DF9D3B: model_joint
    0x16F3BA18: model_tex_vert
    0x2236C47A: level_link_names
    0x283D0383: model_built
    0x2BA33702: level_zone_names
    0x2F4056CE: conduit_asset_refs
    0x30DADA09: zone_asset_references
    0x3250BB80: model_material
    0x339C970E: level_some_data   # exact name unknown
    0x364A6C7C: actor_object_built
    0x396F9418: level_regions_built
    0x4130D903: level_region_names
    0x4A128222: config_type
    0x4AD86765: model_parent_ids
    0x4E023760: level_zones_built
    0x58B8558A: config_asset_refs
    0x5E54ACCF: zone_script_actions
    0x657512BB: zone_decal_geometry
    0x6987F172: zone_model_insts
    0x70682CB8: zone_actors
    0x731CBC2E: model_locator_lookup
    0x78D9CBDE: model_subset
    0x7CA7267D: level_built
    0x96D77BBD: light_grid_probes
    0x9989BB49: light_grid_data
    0x9F614FAB: model_locator
    0x9FD19C20: anim_clip_data
    0xA98BE69B: model_std_vert
    0xB79CF1D7: anim_clip_lookup
    0xBEAB52E7: zone_script_plugs
    0xC5354B60: model_mirror_ids
    0xC61B1FF5: model_skin_batch
    0xC6A5905E: zone_model_names
    0xCEB30E68: conduit_built
    0xD86A7934: zone_script_vars
    0xDC625B3D: zone_actor_names
    0xDCA379A2: model_skin_data
    0xE501186F: config_built
    0xEE31971C: model_joint_lookup
    0xEF8637D5: zone_script_strings
    0xEFD92E68: model_physics_data
