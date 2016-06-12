# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name = "pyNTCIREVAL",
    packages = ["pyNTCIREVAL"],
    version = "0.0.1",
    description = "python version of NTCIREVAL",
    author = "Makoto P. Kato",
    author_email = "kato@dl.kuis.kyoto-u.ac.jp",
    license     = "MIT License",
    url = "https://github.com/mpkato/pyNTCIREVAL",
    entry_points='''
        [console_scripts]
        pyNTCIREVAL=pyNTCIREVAL.main:cli
    ''',
    install_requires = [
        'numpy'
    ],
    tests_require=['nose']
)