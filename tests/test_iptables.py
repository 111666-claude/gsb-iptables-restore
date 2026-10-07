import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iptables import core

TEXT = "*filter\n:INPUT ACCEPT [0:0]\n-A INPUT -j ACCEPT\nCOMMIT\n"


class IptablesTest(unittest.TestCase):
    def test_rule_count(self):
        self.assertEqual(len(core.parse(TEXT, core.Counter()).rules), 1)

    def test_chain_declared(self):
        ruleset = core.parse(TEXT, core.Counter())
        self.assertEqual(ruleset.chains[0]["name"], "INPUT")

    def test_rules_in_chain(self):
        ruleset = core.parse(TEXT, core.Counter())
        self.assertEqual(len(core.rules_in(ruleset, "INPUT", core.Counter())), 1)

    def test_comment_skipped(self):
        self.assertEqual(len(core.parse("# c\n", core.Counter()).rules), 0)

    def test_empty_text(self):
        self.assertEqual(len(core.parse("", core.Counter()).rules), 0)

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse(TEXT, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
