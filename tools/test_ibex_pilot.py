"""Offline boundary tests; these do not validate hardware behavior."""
import copy
import unittest
from ibex_pilot import diff_file_count, same_repo_references, validate_result

class EvidenceBoundaryTests(unittest.TestCase):
    def test_nested_tracked_patch_is_not_an_extra_file(self):
        diff = 'diff --git a/a b/a\n+diff --git a/nested b/nested\ndiff --git a/b b/b\n'
        self.assertEqual(diff_file_count(diff), 2)

    def test_link_forms_and_external_repo_exclusion(self):
        text = '#12 lowRISC/ibex#13 https://github.com/lowRISC/ibex/pull/14 other/repo#15 #12 #99'
        self.assertEqual(same_repo_references(text, 99), [12, 13, 14])

    def test_reject_invalid_api_values(self):
        valid = {'answers': {'category': {'type': 'choice', 'choice': 'rtl'},
                             'review_value': {'type': 'noul', 'noul': 0.5},
                             'insufficient': {'type': 'noul', 'noul': 0.2}}}
        validate_result(valid)
        for bad in [True, '0.5', float('nan'), -0.01, 1.01]:
            result = copy.deepcopy(valid)
            result['answers']['review_value']['noul'] = bad
            with self.assertRaises(ValueError):
                validate_result(result)
        result = copy.deepcopy(valid)
        result['answers']['category']['choice'] = 'invented'
        with self.assertRaises(ValueError):
            validate_result(result)

if __name__ == '__main__':
    unittest.main()
