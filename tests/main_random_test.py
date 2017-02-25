# -*- coding:utf-8 -*-
import tempfile
import os
import unittest
import re
import subprocess
import numpy as np
from click.testing import CliRunner
from pyNTCIREVAL.main import cli
from tests.helper import ntcireval_formatting

from logging import getLogger, StreamHandler, DEBUG, INFO
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

class MainRandomTestCase(unittest.TestCase):
    NUM_DOCS = 1000
    NUM_RES = 100
    MAX_GRADE = 3
    NON_LABEL_PROB = 0.05
    LOOP = 10

    def setUp(self):
        self.maxDiff = None
        self.tmpfiles = []

    def tearDown(self):
        for filehandle, filepath in self.tmpfiles:
            if os.path.exists(filepath):
                os.close(filehandle)
                os.remove(filepath)

    def test_compute(self):
        resfile = self._generate_random_res_file()
        relfile = self._generate_random_rel_file()
        labfile = self._label(relfile, resfile)
        res = self._run_ntcireval(relfile, labfile)
        runner = CliRunner()
        result = runner.invoke(cli, ['compute',
            '-r', relfile,
            '-g', '1:2:3',
            labfile])
        self.assertEqual(
            re.split(r'\r?\n', result.output.strip().replace(" ", "")),
            re.split(r'\r?\n', ntcireval_formatting(res)),
        )
        logger.info("\n" + "\n".join(res.split("\n")))
        logger.info("\n" + "\n".join(result.output.split("\n")))

    def _run_ntcireval(self, relfile, labfile):
        args = [os.path.join(os.path.dirname(__file__),
            '..', 'NTCIREVAL', 'ntcir_eval'),
            'compute',
            '-r', relfile,
            '-g', '1:2:3',
            labfile]
        p = subprocess.Popen(args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = p.communicate()
        return stdout_data.decode()

    def _label(self, relfile, resfile):
        tf = self._generate_tmpfile()
        runner = CliRunner()
        result = runner.invoke(cli, ['label',
            '-r', relfile,
            resfile])
        with open(tf, "w") as f:
            f.write(result.output)
        return tf

    def _generate_tmpfile(self):
        tfh, tf = tempfile.mkstemp()
        self.tmpfiles.append((tfh, tf))
        return tf

    def _generate_random_res_file(self):
        tf = self._generate_tmpfile()
        with open(tf, "w") as f:
            for i in range(self.NUM_RES):
                p = np.random.rand()
                if p < self.NON_LABEL_PROB:
                    idx = self.NUM_DOCS + np.random.randint(self.NUM_DOCS)
                else:
                    idx = np.random.randint(self.NUM_DOCS)
                f.write("D%010d\n" % idx)
        return tf

    def _generate_random_rel_file(self):
        tf = self._generate_tmpfile()
        with open(tf, "w") as f:
            for i in range(self.NUM_DOCS):
                g = np.random.randint(self.MAX_GRADE+1)
                f.write("D%010d L%s\n" % (i, g))
        return tf

for i in range(MainRandomTestCase.LOOP):
    setattr(MainRandomTestCase, 'test_compute_%06d' % i, MainRandomTestCase.test_compute)
