"""XDF definition reader: XDFAxis, XDFParameter, XDFDefinition.

Transcribed by hand from the CPython 3.12 disassembly of the original classes
(recovered/6l80e-python-disasm/00905..01157). Each method names its source
disassembly file. Status: transcribed, NOT yet differentially verified
(see README.md: the original must not be executed without approval).

Usage:
    xdf = XDFDefinition.from_file("e38_6l80.xdf")
    param = xdf.find("Base Shift Pressure")
    data = param.read(bin_bytes)
"""

import xml.etree.ElementTree as ET


class XDFAxis:
    """Single axis (x, y or z) from an XDF table, or a scalar."""

    __slots__ = ('axis_id', 'address', 'size_bits', 'stride_bits', 'row_count',
                 'col_count', 'signed', 'little_endian', 'math_eq', 'label_units')

    def __init__(self):
        # __init__.dis 911
        self.axis_id = ''
        self.address = 0
        self.size_bits = 16
        self.stride_bits = 0
        self.row_count = 1
        self.col_count = 1
        self.signed = False
        self.little_endian = False
        self.math_eq = 'X'
        self.label_units = ''

    def _read_one(self, bin_data, offset_bytes):
        # _read_one.dis 923
        n_bytes = self.size_bits // 8
        if offset_bytes + n_bytes > len(bin_data):
            return 0.0
        raw_bytes = bin_data[offset_bytes:offset_bytes + n_bytes]
        byte_order = 'little' if self.little_endian else 'big'
        raw = int.from_bytes(raw_bytes, byte_order, signed=self.signed)
        return self._apply_math(raw)

    def _apply_math(self, raw_value):
        # _apply_math.dis 933
        # math_eq is an expression in X. Only characters in 0-9 . + - * / ( ) space e E
        # are allowed through to eval; anything else falls back to the raw value.
        eq = self.math_eq.strip()
        if not eq or eq.upper() == 'X':
            return float(raw_value)
        safe = eq.upper().replace('X', f'({float(raw_value)})')
        for c in safe:
            if c not in '0123456789.+-*/() eE':
                return float(raw_value)
        try:
            return float(eval(safe, {'__builtins__': {}}, {}))
        except Exception:
            return float(raw_value)

    def read_table(self, bin_data):
        # read_table.dis 948
        stride = self.stride_bits or self.size_bits * self.col_count
        out = []
        for r in range(max(1, self.row_count)):
            row = []
            row_byte_start = self.address + (r * stride) // 8
            for c in range(max(1, self.col_count)):
                offset = row_byte_start + c * (self.size_bits // 8)
                row.append(self._read_one(bin_data, offset))
            out.append(row)
        return out


class XDFParameter:
    """A scalar or table from an XDF definition."""

    def __init__(self):
        # __init__.dis 964
        self.kind = 'scalar'
        self.uid = ''
        self.title = ''
        self.category = ''
        self.units = ''
        self.description = ''
        self.x_axis = None
        self.y_axis = None
        self.z_axis = None

    def read(self, bin_data):
        # read.dis 975
        if self.kind == 'scalar':
            if self.z_axis:
                return self.z_axis._read_one(bin_data, self.z_axis.address)
            return 0.0

        def _flatten_or_single(table):
            if table and len(table) == 1:
                return table[0]
            return [v for row in table for v in row]

        result = {}
        if self.x_axis:
            result['x_breakpoints'] = _flatten_or_single(self.x_axis.read_table(bin_data))
        if self.y_axis:
            result['y_breakpoints'] = _flatten_or_single(self.y_axis.read_table(bin_data))
        result['z'] = self.z_axis.read_table(bin_data) if self.z_axis else []
        return result


class XDFDefinition:
    """Parsed XDF document: a collection of XDFParameter objects."""

    def __init__(self):
        # __init__.dis 1001
        self.parameters = []
        self.base_offset = 0
        self.title = ''

    def find(self, title_substr):
        # find.dis 1006
        lo = title_substr.lower()
        for p in self.parameters:
            if lo in p.title.lower():
                return p
        return None

    def find_all(self, title_substr):
        # find_all.dis 1013
        lo = title_substr.lower()
        return [p for p in self.parameters if lo in p.title.lower()]

    def categories(self):
        # categories.dis 1017
        return sorted({p.category for p in self.parameters if p.category})

    @classmethod
    def from_file(cls, path):
        # from_file.dis 1020
        try:
            tree = ET.parse(path)
        except ET.ParseError as e:
            raise ValueError(f'Invalid XDF XML: {e}')
        return cls._from_element(tree.getroot())

    @classmethod
    def from_string(cls, xml_str):
        # from_string.dis 1029
        return cls._from_element(ET.fromstring(xml_str))

    @classmethod
    def _from_element(cls, root):
        # _from_element.dis 1034
        xdf = cls()
        hdr = root.find('XDFHEADER')
        if hdr is not None:
            t = hdr.find('deftitle')
            if t is not None and t.text:
                xdf.title = t.text.strip()
            base = hdr.find('BASEOFFSET')
            if base is not None:
                xdf.base_offset = cls._parse_int(base.get('offset', '0'))
        for el in root.findall('XDFCONSTANT'):
            p = cls._parse_scalar(el)
            if p:
                xdf.parameters.append(p)
        for el in root.findall('XDFTABLE'):
            p = cls._parse_table(el)
            if p:
                xdf.parameters.append(p)
        return xdf

    @staticmethod
    def _parse_int(s):
        # _parse_int.dis 1056
        if not s:
            return 0
        s = s.strip()
        try:
            if s.lower().startswith('0x'):
                return int(s, 16)
            return int(s)
        except ValueError:
            return 0

    @staticmethod
    def _parse_axis(el, axis_id):
        # _parse_axis.dis 1068
        if el is None:
            return None
        ax = XDFAxis()
        ax.axis_id = axis_id

        emb = el.find('EMBEDDEDDATA')
        if emb is not None:
            ax.address = XDFDefinition._parse_int(emb.get('mmedaddress', '0'))
            ax.size_bits = int(emb.get('mmedelementsizebits', '16'))
            ax.stride_bits = int(emb.get('mmedmajorstridebits', '0'))
            ax.row_count = int(emb.get('mmedrowcount', '1'))
            ax.col_count = int(emb.get('mmedcolcount', '1'))
            flags = int(emb.get('mmedtypeflags', '0'), 0)
            ax.signed = bool(flags & 1)
            ax.little_endian = bool(flags & 2)

        math_el = el.find('MATH')
        if math_el is not None:
            ax.math_eq = math_el.get('equation', 'X') or 'X'

        units_el = el.find('units')
        if units_el is not None and units_el.text:
            ax.label_units = units_el.text.strip()

        idx_el = el.find('indexcount')
        if idx_el is not None and idx_el.text:
            try:
                cnt = int(idx_el.text)
                if axis_id == 'x' and ax.col_count == 1:
                    ax.col_count = cnt
                elif axis_id == 'y' and ax.row_count == 1:
                    ax.row_count = cnt
            except ValueError:
                return ax
        return ax

    @classmethod
    def _parse_scalar(cls, el):
        # _parse_scalar.dis 1102
        p = XDFParameter()
        p.kind = 'scalar'
        p.uid = el.get('uniqueid', '')
        t = el.find('title')
        if t is not None and t.text:
            p.title = t.text.strip()
        cat = el.find('CATEGORYMEM')
        if cat is not None:
            p.category = cat.get('category', '') or cat.get('index', '')
        desc = el.find('description')
        if desc is not None and desc.text:
            p.description = desc.text.strip()
        units = el.find('units')
        if units is not None and units.text:
            p.units = units.text.strip()
        p.z_axis = cls._parse_axis(el, 'z')
        if p.z_axis:
            p.z_axis.row_count = 1
            p.z_axis.col_count = 1
        return p if p.z_axis else None

    @classmethod
    def _parse_table(cls, el):
        # _parse_table.dis 1125
        p = XDFParameter()
        p.uid = el.get('uniqueid', '')
        t = el.find('title')
        if t is not None and t.text:
            p.title = t.text.strip()
        cat = el.find('CATEGORYMEM')
        if cat is not None:
            p.category = cat.get('category', '') or cat.get('index', '')

        for axis_el in el.findall('XDFAXIS'):
            axis_id = axis_el.get('id', '').lower()
            ax = cls._parse_axis(axis_el, axis_id)
            if ax is None:
                continue
            if axis_id == 'x':
                p.x_axis = ax
                continue
            if axis_id == 'y':
                p.y_axis = ax
                continue
            if axis_id != 'z':
                continue
            p.z_axis = ax
            # Units are read from XDFAXIS only for the z axis (x and y skip this step).
            units_el = axis_el.find('units')
            if units_el is None or not units_el.text:
                continue
            p.units = units_el.text.strip()

        if not p.z_axis:
            return None
        if p.x_axis and p.y_axis:
            p.kind = 'table_2d'
        elif p.x_axis or p.y_axis:
            p.kind = 'table_1d'
        else:
            p.kind = 'scalar'
        return p
