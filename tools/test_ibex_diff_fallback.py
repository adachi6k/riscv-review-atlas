import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import ibex_diff_fallback as fallback

class DiffDecodingTests(unittest.TestCase):
    def test_non_utf8_bytes_remain_recoverable(self):
        original=b'diff --git a/x b/x\n+Copyright \xa9\n'
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch.object(fallback,'BASE',root):
                fallback.write_diff(1,original,'test')
            self.assertEqual((root/'diff-raw/1.bin').read_bytes(),original)
            self.assertEqual((root/'diffs/1.diff').read_text().encode('latin-1'),original)
            provenance=json.loads((root/'diff-provenance/1.json').read_text())
            self.assertEqual(provenance['raw_sha256'],hashlib.sha256(original).hexdigest())
            self.assertEqual(provenance['decoding'],'latin-1-byte-mapping')

if __name__=='__main__':unittest.main()
