"""
A dumber implementation of csv that allows for easier *editing* of records
in tab-separated-values without messing up version control unnecessarily.

It's also pickier than the csv reader
"""
import io

class TSVEntry:
    __slots__ = ("_d", "_k", "_keylist")
    def __init__(self, keylist, value_dict):
        self._k = set(keylist)
        self._keylist = keylist
        self._d = dict(value_dict)
    def update_other(self, other):
        if self._keylist == other._keylist: return self
        keylist = other._keylist
        out = TSVEntry(keylist, other._d.copy())
        for k in keylist:
            if k in self._d:
                out[k] = self[k]
    def __getattr__(self, nm): return getattr(self._d, nm)
    def _clean_value(self, value):
        if value is None: return None
        return value.strip()
    def __getitem__(self, nm):
        """
        This function cleans up the data before it returns it.
        We keep the un-cleaned-up version around so that it
        gets outputted the same way it was inputted.
        """
        return self._clean_value(self._d[nm])
    def get(self, nm, default=None): return self._clean_value(self._d.get(nm, default))
    def __dict__(self): return self._d
    def __setitem__(self, nm, value):
        if nm not in self._k: raise KeyError(nm)
        self._d[nm] = value
    def print_entry(self, fp=None):
        if fp is None: fp = io.StringIO()
        it = reversed(self._keylist)
        ls = []
        try:
            cur = next(it)
            while cur not in self._d: cur = next(it)
            ls.append(self._d[cur])
            while True: ls.append(self._d.get(next(it), ""))
        except StopIteration:
            pass
        for idx, e in enumerate(reversed(ls)):
            if idx: fp.write("\t")
            fp.write(e)
        fp.write("\n")
        try:
            return fp.getvalue()
        except AttributeError:
            return
    def __repr__(self): return repr(self._d)
    def __str__(self): return self.print_entry()

class TSVFileData:
    __slots__ = ("_headings", "_headings_clean")
    def __init__(self, headings):
        self._headings = headings
        self._headings_clean = headings
    def print_headings(self, fp=None):
        out = "\t".join(self._headings) + "\n"
        if fp is not None: fp.write(out)
        return out
    def dict_from_line(self, values):
        if len(values) > len(self._headings):
            raise TSVError("Too many values, expected {} found {}: {}".format(
                len(self._headings),
                len(self._values),
                repr(values)
            ))
        return TSVEntry(self._headings_clean,
                        dict(zip(self._headings_clean, values)))

class TSVFileLineReader:
    __slots__ = ("_lines",)
    def __init__(self, lines): self._lines = iter(lines)
    def __next__(self):
        line = next(self._lines)
        while line and line[-1] in "\n\r": line = line[:-1]
        return line.split("\t")
    def __iter__(self): return self

class TSVFileReader:
    __slots__ = ("_line_reader", "_file_data")
    def __init__(self, lines):
        self._line_reader = TSVFileLineReader(lines)
        self._file_data = TSVFileData(next(self._line_reader))
    def __next__(self): return self._file_data.dict_from_line(next(self._line_reader))
    def __iter__(self): return self
    def print_headings(self, fp=None): return self._file_data.print_headings(fp=fp)
