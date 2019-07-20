# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
import zlib


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Igtoc(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\xAF\x12\xAF\x77")
        self.len_decompressed = self._io.read_u4le()
        self._raw__raw_dec_toc = self._io.read_bytes_full()
        zobj = zlib.decompressobj()
        self._raw_dec_toc = zobj.decompress(self._raw__raw_dec_toc)
        self._raw_dec_toc += zobj.flush()
        io = KaitaiStream(BytesIO(self._raw_dec_toc))
        self.dec_toc = self._root.Toc(io, self, self._root)

    class AssetId(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.built_hash = self._io.read_u8le()


    class HeaderSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.const_hash = self._io.read_u4le()
            self.offset = self._io.read_u4le()
            self.len = self._io.read_u4le()


    class OffsetEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.archive_index = self._io.read_u4le()
            self.archive_offset = self._io.read_u4le()


    class Toc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dat1 = self._io.ensure_fixed_contents(b"\x31\x54\x41\x44")
            self.toc_const = self._io.read_u4le()
            self.len_file = self._io.read_u4le()
            self.num_sections = self._io.read_u4le()
            self.archive_files_hdr = self._root.HeaderSection(self._io, self, self._root)
            self.asset_ids_hdr = self._root.HeaderSection(self._io, self, self._root)
            self.sizes_hdr = self._root.HeaderSection(self._io, self, self._root)
            self.key_assets_hdr = self._root.HeaderSection(self._io, self, self._root)
            self.offsets_hdr = self._root.HeaderSection(self._io, self, self._root)
            self.spans_hdr = self._root.HeaderSection(self._io, self, self._root)
            self.file_type_str = (self._io.read_bytes_term(0, False, True, True)).decode(u"ASCII")

        @property
        def sizes(self):
            if hasattr(self, '_m_sizes'):
                return self._m_sizes if hasattr(self, '_m_sizes') else None

            _pos = self._io.pos()
            self._io.seek(self.sizes_hdr.offset)
            self._raw__m_sizes = [None] * (self.sizes_hdr.len // 12)
            self._m_sizes = [None] * (self.sizes_hdr.len // 12)
            for i in range(self.sizes_hdr.len // 12):
                self._raw__m_sizes[i] = self._io.read_bytes(12)
                io = KaitaiStream(BytesIO(self._raw__m_sizes[i]))
                self._m_sizes[i] = self._root.SizeEntry(io, self, self._root)

            self._io.seek(_pos)
            return self._m_sizes if hasattr(self, '_m_sizes') else None

        @property
        def archive_files(self):
            if hasattr(self, '_m_archive_files'):
                return self._m_archive_files if hasattr(self, '_m_archive_files') else None

            _pos = self._io.pos()
            self._io.seek(self.archive_files_hdr.offset)
            self._raw__m_archive_files = [None] * (self.archive_files_hdr.len // 24)
            self._m_archive_files = [None] * (self.archive_files_hdr.len // 24)
            for i in range(self.archive_files_hdr.len // 24):
                self._raw__m_archive_files[i] = self._io.read_bytes(24)
                io = KaitaiStream(BytesIO(self._raw__m_archive_files[i]))
                self._m_archive_files[i] = self._root.ArchiveFile(io, self, self._root)

            self._io.seek(_pos)
            return self._m_archive_files if hasattr(self, '_m_archive_files') else None

        @property
        def key_assets(self):
            if hasattr(self, '_m_key_assets'):
                return self._m_key_assets if hasattr(self, '_m_key_assets') else None

            _pos = self._io.pos()
            self._io.seek(self.key_assets_hdr.offset)
            self._raw__m_key_assets = [None] * (self.key_assets_hdr.len // 4)
            self._m_key_assets = [None] * (self.key_assets_hdr.len // 4)
            for i in range(self.key_assets_hdr.len // 4):
                self._raw__m_key_assets[i] = self._io.read_bytes(4)
                io = KaitaiStream(BytesIO(self._raw__m_key_assets[i]))
                self._m_key_assets[i] = self._root.KeyAsset(io, self, self._root)

            self._io.seek(_pos)
            return self._m_key_assets if hasattr(self, '_m_key_assets') else None

        @property
        def span_entries(self):
            if hasattr(self, '_m_span_entries'):
                return self._m_span_entries if hasattr(self, '_m_span_entries') else None

            _pos = self._io.pos()
            self._io.seek(self.spans_hdr.offset)
            self._raw__m_span_entries = [None] * (self.spans_hdr.len // 8)
            self._m_span_entries = [None] * (self.spans_hdr.len // 8)
            for i in range(self.spans_hdr.len // 8):
                self._raw__m_span_entries[i] = self._io.read_bytes(8)
                io = KaitaiStream(BytesIO(self._raw__m_span_entries[i]))
                self._m_span_entries[i] = self._root.SpanEntry(io, self, self._root)

            self._io.seek(_pos)
            return self._m_span_entries if hasattr(self, '_m_span_entries') else None

        @property
        def offsets(self):
            if hasattr(self, '_m_offsets'):
                return self._m_offsets if hasattr(self, '_m_offsets') else None

            _pos = self._io.pos()
            self._io.seek(self.offsets_hdr.offset)
            self._raw__m_offsets = [None] * (self.offsets_hdr.len // 8)
            self._m_offsets = [None] * (self.offsets_hdr.len // 8)
            for i in range(self.offsets_hdr.len // 8):
                self._raw__m_offsets[i] = self._io.read_bytes(8)
                io = KaitaiStream(BytesIO(self._raw__m_offsets[i]))
                self._m_offsets[i] = self._root.OffsetEntry(io, self, self._root)

            self._io.seek(_pos)
            return self._m_offsets if hasattr(self, '_m_offsets') else None

        @property
        def asset_ids(self):
            if hasattr(self, '_m_asset_ids'):
                return self._m_asset_ids if hasattr(self, '_m_asset_ids') else None

            _pos = self._io.pos()
            self._io.seek(self.asset_ids_hdr.offset)
            self._raw__m_asset_ids = [None] * (self.asset_ids_hdr.len // 8)
            self._m_asset_ids = [None] * (self.asset_ids_hdr.len // 8)
            for i in range(self.asset_ids_hdr.len // 8):
                self._raw__m_asset_ids[i] = self._io.read_bytes(8)
                io = KaitaiStream(BytesIO(self._raw__m_asset_ids[i]))
                self._m_asset_ids[i] = self._root.AssetId(io, self, self._root)

            self._io.seek(_pos)
            return self._m_asset_ids if hasattr(self, '_m_asset_ids') else None


    class ArchiveFile(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_00 = self._io.read_u2le()
            self.install_bucket = self._io.read_u1()
            self.unknown_03 = self._io.read_u1()
            self.chunkmap = self._io.read_u4le()
            self.filename = (self._io.read_bytes_term(0, False, True, True)).decode(u"ASCII")
            self.unknown_10 = self._io.read_bytes_full()


    class KeyAsset(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.asset_id_lo = self._io.read_u4le()


    class SpanEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.asset_index = self._io.read_u4le()
            self.count = self._io.read_u4le()


    class SizeEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_ctr_inc = self._io.read_u4le()
            self.file_size = self._io.read_u4le()
            self.file_ctr = self._io.read_u4le()



