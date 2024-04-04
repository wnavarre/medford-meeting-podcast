import unittest
import clean_tsv
from io import StringIO

class TestCleanTSV(unittest.TestCase):
    def test_read(self):
        data_file = StringIO("L\tR\nA\tB\nC\tD\n")
        res = list(clean_tsv.TSVFileReader(data_file))
        self.assertEqual(len(res), 2)
        self.assertEqual(dict(res[0]), dict(L="A", R="B"))
        self.assertEqual(dict(res[1]), dict(L="C", R="D"))
        record = res[1]
        fout = StringIO()
        record["R"] = "~~~~~~~"
        record.print_entry(fout)
        self.assertIn("~~", fout.getvalue())
if __name__ == '__main__':
    unittest.main()
