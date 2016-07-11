#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# a `with statements` wrap for textwrap
# ----------

import textwrap
from contextlib import contextmanager

class ContextOfTextWrapper:
    def __init__(self, printer):
        self._printer = printer        
    def __enter__(self):
        pass
    def __exit__(self, *args):
        pass

class TextPrinter:
    '''a [with statement]s wrap for textwrap'''
    def __init__(self):
        self._text_wrapper = textwrap.TextWrapper(replace_whitespace=False)

    def print(self, text):
        print(self._text_wrapper.fill(text))

    def set(self, **kwargs):
        class SetContextOfTextWrapper(ContextOfTextWrapper):
            def __init__(self, printer):
                super().__init__(printer)
                self._old_values = {}
            def __enter__(self):
                for key in kwargs:
                    self._old_values[key] = getattr(self._printer._text_wrapper, key)
                    setattr(self._printer._text_wrapper, key, kwargs[key])
            def __exit__(self, *args):
                for key in self._old_values:
                    setattr(self._printer._text_wrapper, key, self._old_values[key])
        return SetContextOfTextWrapper(self)

    def add(self, **kwargs):
        class AddContextOfTextWrapper(ContextOfTextWrapper):
            def __init__(self, printer):
                super().__init__(printer)
                self._old_values = {}
            def __enter__(self):
                for key in kwargs:
                    old = getattr(self._printer._text_wrapper, key)
                    self._old_values[key] = old
                    setattr(self._printer._text_wrapper, key, old + kwargs[key])
            def __exit__(self, *args):
                for key in self._old_values:
                    setattr(self._printer._text_wrapper, key, self._old_values[key])
        return AddContextOfTextWrapper(self)

    def indent(self, prefix):
        return self.set(initial_indent=prefix, subsequent_indent=prefix)

    def indent_inc(self, prefix):
        return self.add(initial_indent=prefix, subsequent_indent=prefix)