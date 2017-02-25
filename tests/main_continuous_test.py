# -*- coding:utf-8 -*-
import sys, os
import unittest
from click.testing import CliRunner
from pyNTCIREVAL.main import cli
from tests.helper import ntcireval_formatting

def p(path):
    return os.path.join(os.path.dirname(__file__), 'dat', path)

def r(name):
    return open(p("res_%s.txt" % name)).read()

class MainTestCase(unittest.TestCase):
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
