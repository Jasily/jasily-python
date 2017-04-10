#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback
import unittest
import colorama as c

from jasily.exceptions import *

class TestArgumentTypeException(unittest.TestCase):
    def test_ctor(self):
        with self.assertRaises(ArgumentTypeException):
            ArgumentTypeException('str', 1)

    def test_tostr(self):
        print()
        print('show str(ArgumentTypeException):')
        print('  ' + str(ArgumentTypeException(str, 1)))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        c.init(True)
        unittest.main()
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
