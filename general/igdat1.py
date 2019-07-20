# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Igdat1(KaitaiStruct):

    class Types(Enum):
        dict = 51707972
        zone_scene_objects = 111921842
        model_look = 116096764
        model_index = 140084797
        zone_actor_groups = 217418350
        actor_prius_built = 324547272
        model_joint = 366976315
        model_tex_vert = 385071640
        level_link_names = 574014586
        model_built = 675087235
        level_zone_names = 732116738
        conduit_asset_refs = 792745678
        zone_asset_references = 819649033
        model_material = 844151680
        level_some_data = 865900302
        actor_object_built = 910847100
        level_regions_built = 963613720
        level_region_names = 1093720323
        config_type = 1242726946
        model_parent_ids = 1255696229
        level_zones_built = 1308768096
        config_asset_refs = 1488475530
        zone_script_actions = 1582607567
        zone_decal_geometry = 1702171323
        zone_model_insts = 1770516850
        zone_actors = 1885875384
        model_locator_lookup = 1931263022
        model_subset = 2027539422
        level_built = 2091329149
        light_grid_probes = 2530704317
        light_grid_data = 2575940425
        model_locator = 2673954731
        anim_clip_data = 2681314336
        model_std_vert = 2844518043
        anim_clip_lookup = 3080516055
        zone_script_plugs = 3198898919
        model_mirror_ids = 3308604256
        model_skin_batch = 3323666421
        zone_model_names = 3332739166
        conduit_built = 3467841128
        zone_script_vars = 3630856500
        zone_actor_names = 3697433405
        model_skin_data = 3701701026
        config_built = 3842054255
        model_joint_lookup = 3996227356
        zone_script_strings = 4018550741
        model_physics_data = 4023987816
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x31\x54\x41\x44")
        self.type_hash = self._io.read_u4le()
        self.len_file = self._io.read_u4le()
        self.num_sections = self._io.read_u2le()
        self.unk_0e = self._io.read_u2le()
        self.sections = [None] * (self.num_sections)
        for i in range(self.num_sections):
            self.sections[i] = self._root.Section(self._io, self, self._root)

        self.file_type_str = (KaitaiStream.bytes_terminate(self._io.read_bytes_full(), 0, False)).decode(u"ASCII")

    class ZoneVar(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ofs_name = self._io.read_u4le()
            self.name_hash = self._io.read_u4le()
            self.ofs_data = self._io.read_u4le()
            self.len_data = self._io.read_u4le()

        @property
        def name(self):
            if hasattr(self, '_m_name'):
                return self._m_name if hasattr(self, '_m_name') else None

            io = self._root._io
            _pos = io.pos()
            io.seek(self.ofs_name)
            self._m_name = (KaitaiStream.bytes_terminate(io.read_bytes_full(), 0, False)).decode(u"ASCII")
            io.seek(_pos)
            return self._m_name if hasattr(self, '_m_name') else None

        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data if hasattr(self, '_m_data') else None

            io = self._root._io
            _pos = io.pos()
            io.seek(self.ofs_data)
            self._raw__m_data = io.read_bytes(self.len_data)
            io = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = self._root.SubSection(16, io, self, self._root)
            io.seek(_pos)
            return self._m_data if hasattr(self, '_m_data') else None


    class ModelIndices(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.indices = []
            i = 0
            while not self._io.is_eof():
                self.indices.append(self._root.ModelIndex(self._io, self, self._root))
                i += 1



    class Vec4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()
            self.w = self._io.read_f4le()


    class ByteF32(KaitaiStruct):
        def __init__(self, attr, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.attr = attr
            self._read()

        def _read(self):
            self.value = [None] * (((self.attr & 4080) >> 4))
            for i in range(((self.attr & 4080) >> 4)):
                self.value[i] = self._io.read_u1()



    class Vert(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk_00 = self._io.read_s2le()
            self.unk_02 = self._io.read_s2le()
            self.unk_04 = self._io.read_s2le()
            self.unk_06 = self._io.read_u2le()
            self.unk_08 = self._io.read_u4le()
            self.unk_0c = self._io.read_u4le()


    class Align(KaitaiStruct):
        def __init__(self, num, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.num = num
            self._read()

        def _read(self):
            self.align__ = self._io.read_bytes(((self.num - self._root._io.pos()) % self.num))


    class ActorHash(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hash = self._io.read_u8le()


    class StrRefSection(KaitaiStruct):
        """A section containing file-relative string offsets."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.refs = []
            i = 0
            while not self._io.is_eof():
                self.refs.append(self._root.StrRef(self._io, self, self._root))
                i += 1



    class ItemHdr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.key_hash = self._io.read_u4le()
            self.key_attr = self._io.read_u2le()
            self.key_type = self._io.read_u2le()


    class ModelIndex(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.index_a = self._io.read_u2le()
            self.index_b = self._io.read_u2le()
            self.index_c = self._io.read_u2le()


    class Section(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type_hash = self._io.read_u4le()
            self.ofs_section = self._io.read_u4le()
            self.len_section = self._io.read_u4le()

        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data if hasattr(self, '_m_data') else None

            _pos = self._io.pos()
            self._io.seek(self.ofs_section)
            _on = self.type_hash
            if _on == 732116738:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 574014586:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 3697433405:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 1242726946:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.SubSection(16, io, self, self._root)
            elif _on == 1093720323:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 2020098101:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 865900302:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.SubSection(16, io, self, self._root)
            elif _on == 3506546380:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 787027571:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.SubSection(16, io, self, self._root)
            elif _on == 1488475530:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 2091329149:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.SubSection(16, io, self, self._root)
            elif _on == 140084797:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.ModelIndices(io, self, self._root)
            elif _on == 3332739166:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 3842054255:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.SubSection(16, io, self, self._root)
            elif _on == 3560352135:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.SubSection(16, io, self, self._root)
            elif _on == 1357759805:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.ZoneVarSection(io, self, self._root)
            elif _on == 2844518043:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.ModelStdVerts(io, self, self._root)
            elif _on == 4018550741:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            elif _on == 2519319175:
                self._raw__m_data = self._io.read_bytes(self.len_section)
                io = KaitaiStream(BytesIO(self._raw__m_data))
                self._m_data = self._root.StrRefSection(io, self, self._root)
            else:
                self._m_data = self._io.read_bytes(self.len_section)
            self._io.seek(_pos)
            return self._m_data if hasattr(self, '_m_data') else None


    class ZoneSceneObjects(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.scene_objects = []
            i = 0
            while not self._io.is_eof():
                self.scene_objects.append(self._root.SceneObject(self._io, self, self._root))
                i += 1



    class ItemName(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ofs_name = self._io.read_u4le()

        @property
        def name(self):
            if hasattr(self, '_m_name'):
                return self._m_name if hasattr(self, '_m_name') else None

            io = self._root._io
            _pos = io.pos()
            io.seek(self.ofs_name)
            self._m_name = (KaitaiStream.bytes_terminate(io.read_bytes_full(), 0, False)).decode(u"ASCII")
            io.seek(_pos)
            return self._m_name if hasattr(self, '_m_name') else None


    class ZoneVarSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.zone_vars = []
            i = 0
            while not self._io.is_eof():
                self.zone_vars.append(self._root.ZoneVar(self._io, self, self._root))
                i += 1



    class StrLit(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.align__ = self._root.Align(4, self._io, self, self._root)
            self.len_str = self._io.read_u4le()
            self.str_hash = self._io.read_u4le()
            self.unk_hash_a = self._io.read_u4le()
            self.unk_hash_b = self._io.read_u4le()
            self.str = (KaitaiStream.bytes_terminate(self._io.read_bytes(((self.len_str & ~3) + 4)), 0, False)).decode(u"ASCII")


    class ItemDict(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.item_hdrs = [None] * (self._parent.num_items)
            for i in range(self._parent.num_items):
                self.item_hdrs[i] = self._root.ItemHdr(self._io, self, self._root)

            self.item_names = [None] * (self._parent.num_items)
            for i in range(self._parent.num_items):
                self.item_names[i] = self._root.ItemName(self._io, self, self._root)

            self.item_values = [None] * (self._parent.num_items)
            for i in range(self._parent.num_items):
                _on = self.item_hdrs[i].key_type
                if _on == 2048:
                    self.item_values[i] = self._io.read_f4le()
                elif _on == 2560:
                    self.item_values[i] = self._root.StrLit(self._io, self, self._root)
                elif _on == 0:
                    self.item_values[i] = self._root.ByteF32(self.item_hdrs[i].key_attr, self._io, self, self._root)
                elif _on == 4864:
                    self.item_values[i] = self._root.SubSection(self.item_hdrs[i].key_attr, self._io, self, self._root)
                elif _on == 512:
                    self.item_values[i] = self._io.read_s4le()
                elif _on == 1024:
                    self.item_values[i] = self._io.read_s1()
                elif _on == 4352:
                    self.item_values[i] = self._root.ActorHash(self._io, self, self._root)
                elif _on == 256:
                    self.item_values[i] = self._io.read_u2le()
                elif _on == 3328:
                    self.item_values[i] = self._root.SubSection(self.item_hdrs[i].key_attr, self._io, self, self._root)
                elif _on == 3840:
                    self.item_values[i] = self._io.read_bits_int(1) != 0
                else:
                    self.item_values[i] = self._io.read_u1()

            if self._parent.num_items > 0:
                _on = self.item_hdrs[-1].key_type
                if _on == 3840:
                    self.align__ = self._root.Align(2, self._io, self, self._root)
                else:
                    self.align__ = self._root.Align(4, self._io, self, self._root)



    class SubSectionItem(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk_00 = self._io.read_u4le()
            self.type_hash = self._io.read_u4le()
            self.num_items = self._io.read_u4le()
            self.body_size = self._io.read_u4le()
            _on = self.type_hash
            if _on == 51707972:
                self._raw_items = self._io.read_bytes(self.body_size)
                io = KaitaiStream(BytesIO(self._raw_items))
                self.items = self._root.ItemDict(io, self, self._root)
            elif _on == 119544169:
                self._raw_items = self._io.read_bytes(self.body_size)
                io = KaitaiStream(BytesIO(self._raw_items))
                self.items = self._root.ItemDict(io, self, self._root)
            else:
                self.items = self._io.read_bytes(self.body_size)


    class SceneObject(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk_00 = self._io.read_bytes(48)
            self.position = self._root.Vec4(self._io, self, self._root)


    class ModelStdVerts(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.verts = []
            i = 0
            while not self._io.is_eof():
                self.verts.append(self._root.Vert(self._io, self, self._root))
                i += 1



    class SubSection(KaitaiStruct):
        """A section containing a dictionary of items, including more potential sub-dictionaries."""
        def __init__(self, attr, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.attr = attr
            self._read()

        def _read(self):
            self.items = [None] * (((self.attr & 4080) >> 4))
            for i in range(((self.attr & 4080) >> 4)):
                self.items[i] = self._root.SubSectionItem(self._io, self, self._root)



    class StrRef(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ofs_ref = self._io.read_u4le()

        @property
        def ref(self):
            if hasattr(self, '_m_ref'):
                return self._m_ref if hasattr(self, '_m_ref') else None

            io = self._root._io
            _pos = io.pos()
            io.seek(self.ofs_ref)
            self._m_ref = (KaitaiStream.bytes_terminate(io.read_bytes_full(), 0, False)).decode(u"ASCII")
            io.seek(_pos)
            return self._m_ref if hasattr(self, '_m_ref') else None



