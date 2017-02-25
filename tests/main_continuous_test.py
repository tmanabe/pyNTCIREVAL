# -*- coding:utf-8 -*-
import sys, os
import unittest
from click.testing import CliRunner
from pyNTCIREVAL.main import cli
from pyNTCIREVAL.utils import continuous_grade
from tests.helper import ntcireval_formatting

def p(path):
    return os.path.join(os.path.dirname(__file__), 'dat', path)

def r(name):
    return open(p("res_%s.txt" % name)).read()

class MainContinuousTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_label(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['label',
            '-r', p('sample_continuous.rel'),
            p('sample_continuous.res')])
        self.assertEqual(result.output.strip(),
            '''
dummy11 L0
dummy01 L1.5
dummy12
dummy04 L0.5
'''.strip())

    def test_continuous_grade_forward(self):
        cg = continuous_grade(max=1.5)
        try:
            cg[-1.5]
            raise Exception
        except ValueError:
            pass
        self.assertEqual(1.5, cg[-1])
        self.assertEqual(0.5, cg[-0.5])
        self.assertEqual(1.0, cg[0.0])
        self.assertEqual(1.5, cg[0.5])
        try:
            cg[1.0]
            raise Exception
        except ValueError:
            pass

    def test_continuous_grade_backward(self):
        cg = continuous_grade(max=1.5)
        try:
            cg.index(0.0)
            raise Exception
        except ValueError:
            pass
        self.assertEqual(-0.5, cg.index(0.5))
        self.assertEqual(0.0, cg.index(1.0))
        self.assertEqual(0.5, cg.index(1.5))
        try:
            cg.index(2.0)
            raise Exception
        except ValueError:
            pass

    def test_compute(self):
        self.maxDiff = None
        runner = CliRunner()
        result = runner.invoke(cli, ['compute',
            '-r', p('sample_continuous.rel'),
            '-g', ':1.5',
            p('sample_continuous.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            ntcireval_formatting(r("test_continuous")))

    def test_compute_cutoff(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute',
            '-r', p('sample_continuous.rel'),
            '-g', ':1.5',
            '--cutoffs', '2',
            p('sample_continuous.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            ntcireval_formatting(r("test_continuous_cutoff")))
