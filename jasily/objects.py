#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import uuid
from .exceptions import InvalidOperationException

class __NotFound:
    '''a object for not found value.'''
    pass

NOT_FOUND = __NotFound()

class ValueContainer:
    def __init__(self, *args):
        self.__has_value = False
        self.__value = None
        if len(args) == 1:
            self.set_value(args[0])
        elif len(args) > 0:
            raise TypeError('only accept zero or one args.')

    @property
    def has_value(self):
        '''whether if container has value.'''
        return self.__has_value

    @property
    def value(self):
        '''get current value or None.'''
        return self.__value

    def set_value(self, value):
        '''set container value.'''
        self.__has_value = True
        self.__value = value

    def unset_value(self):
        '''remove container value.'''
        self.__has_value = False
        self.__value = None


class UInt:
    def __init__(self, value: int):
        v = int(value)
        if v < 0:
            raise ValueError
        self._value = v

    def __int__(self):
        return self._value

    def __str__(self):
        return str(self._value)

    def __hash__(self):
        return hash(self._value)

    def __eq__(self, value):
        return self._value == value

    @property
    def value(self):
        return self._value


class Set(set):
    def add(self, v):
        if v in self:
            return False
        set.add(self, v)
        return True


class Char:
    def __init__(self, ch: (str, int)):
        self._value_int: int = None
        self._value_str: str = None
        if isinstance(ch, Char):
            self._value_int = ch._value_int
            self._value_str = ch._value_int
        elif isinstance(ch, str):
            if len(ch) != 1:
                raise ValueError
            self._value_str = ch
            self._value_int = ord(ch)
        elif isinstance(ch, int):
            self._value_int = ch
            self._value_str = chr(ch)
        else:
            raise ValueError

    def __int__(self):
        return self._value_int

    def __str__(self):
        return self._value_str

    def __hash__(self):
        return hash(self._value_int)

    def __eq__(self, value):
        if isinstance(value, Char):
            return self._value_int == value._value_int
        elif isinstance(value, str):
            return str(self) == value
        elif isinstance(value, int):
            return int(self) == value
        else:
            return NotImplemented
