import collections, sys, unittest
from spark_parser.spark import GenericParser

class Rules(GenericParser):
    """Testing duplicate rules"""
    def p_rules(self, args):
        """
        x ::= TOKEN
        x ::= TOKEN

        stmts ::= stmt+
        ratings ::= STARS*
        """
        pass

    def duplicate_rule(self, rule):
        if not hasattr(self, 'dups'):
            self.dups = []
        self.dups.append(rule)
    pass

class RulesPeriod(GenericParser):
    """Testing ? extended rule"""
    def p_rules(self, args):
        """
        opt_period ::= PERIOD?
        """
        pass
    pass

class InvalidRule(GenericParser):
    """Testing ? extended rule"""
    def p_rules(self, args):
        """
        foo ::= foo
        """
        pass
    pass

class TestMisc(unittest.TestCase):

    def test_basic(self):
        # Check duplicate rule detection
        parser = Rules('x', debug={'dups': True})
        self.assertTrue(hasattr(parser, 'dups'))
        self.assertEqual(parser.dups, [('x', ('TOKEN',))])

        # Check "+", and "*", expansion
        rules = sorted(parser.rule2name.items())
        self.assertEqual(rules,
                         [(('START', ('|-', 'x')), 'ambda>'),
                          (('ratings', ()), 'rules'),
                          (('ratings', ('ratings', 'STARS')), 'rules'),
                          (('stmts', ('stmt',)), 'rules'),
                          (('stmts', ('stmts', 'stmt')), 'rules'),
                          (('x', ('TOKEN',)), 'rules')])

        # Check Invalid rule
        try:
            InvalidRule('foo', debug={'dups': True})
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)


    def test_period(self):
        parser = RulesPeriod('opt_period', debug={'dups': True})

        # Check "?" expansion
        rules = sorted(parser.rule2name.items())
        self.assertEqual(rules,
                         [(('START', ('|-', 'opt_period')), 'ambda>'),
                          (('opt_period', ()), 'rules'),
                          (('opt_period', ('PERIOD',)), 'rules'),])


if __name__ == '__main__':
    unittest.main()