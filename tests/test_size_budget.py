"""Keep the always-loaded instructions from growing release by release.

SKILL.md is read on every run, so its size is a recurring cost. The cap is the
v1.0.7 size: adding a rule means removing an equal amount first. Detail-only
rules live in references/detail-evidence.md, which has its own cap. Raising a cap
is a deliberate decision recorded in CHANGELOG, not a side effect of editing.
"""
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
BUDGETS = {
    'SKILL.md': 23842,                      # v1.0.7 size
    'references/workflow.md': 31845,        # v1.0.7 size
    'references/detail-evidence.md': 8192,
}


class SizeBudgetTests(unittest.TestCase):
    def test_instruction_files_stay_within_budget(self):
        for name, cap in BUDGETS.items():
            size = len((PACKAGE / name).read_bytes())
            with self.subTest(file=name):
                self.assertLessEqual(size, cap, '%s is %d bytes, over its %d-byte budget; remove something '
                                                'before adding' % (name, size, cap))


if __name__ == '__main__':
    unittest.main()
