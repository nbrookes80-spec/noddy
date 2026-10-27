"""BinReader: read XDF-described parameters out of a calibration .bin image.

Transcribed by hand from the CPython 3.12 disassembly of the original class
(recovered/6l80e-python-disasm/01160..01204). Status: transcribed, NOT yet
differentially verified.

xdf is an XDFDefinition (see xdf.py): it must provide find(title_substr)
returning an XDFParameter or None, and categories() and parameters.
"""


class BinReader:
    def __init__(self, bin_data, xdf=None):
        # __init__.dis 1169
        self.data = bin_data
        self.xdf = xdf
        self.size = len(bin_data)

    @classmethod
    def from_file(cls, path, xdf=None):
        # from_file.dis 1174
        with open(path, 'rb') as f:
            data = f.read()
        return cls(data, xdf)

    def attach_xdf(self, xdf):
        # attach_xdf.dis 1180
        self.xdf = xdf

    def read(self, title_substr):
        # read.dis 1183
        # Returns a float (scalar), a dict of breakpoints and 'z' values (table), or None.
        if self.xdf is None:
            return None
        p = self.xdf.find(title_substr)
        if p:
            return p.read(self.data)
        return None

    def read_table(self, title_substr):
        # read_table.dis 1189
        r = self.read(title_substr)
        if isinstance(r, dict):
            return r.get('z')
        return None

    def info(self):
        # info.dis 1195
        s = f'BIN size: {self.size} bytes ({self.size // 1024} KB)'
        if self.xdf is not None:
            s += f'\nXDF: {self.xdf.title}'
            s += f'\nParameters: {len(self.xdf.parameters)}'
            cats = self.xdf.categories()
            if cats:
                extra = f' (+{len(cats) - 6} more)' if len(cats) > 6 else ''
                s += '\nCategories: ' + ', '.join(cats[:6]) + extra
        return s
