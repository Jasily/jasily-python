#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# the missing
# ----------

from .typed.ensures import *

class uint(int):
    '''
    the unsigned integer.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__() # object.__init__() takes no arguments
        if self < 0:
            raise ValueError(f'uint cannot less then zero.')


class IComparer:
    def hash(self, obj):
        raise NotImplementedError

    def eq(self, obj1, obj2):
        raise NotImplementedError

    def wrap(self, obj):
        class Wrap:
            def __init__(self, comparer, obj):
                self._comparer = comparer
                self._obj = obj

            def unwrap(self):
                return self._obj

            def __repr__(self):
                return self._obj.__repr__()

            def __str__(self):
                return self._obj.__str__()

            def __hash__(self):
                return self._comparer.hash(self._obj)

            def __eq__(self, obj):
                if isinstance(obj, Wrap):
                    obj = obj.unwrap()
                return self._comparer.eq(self._obj, obj)
        return Wrap(self, obj)


class ObjectComparer(IComparer):
    def hash(self, obj):
        return hash(obj)

    def eq(self, obj1, obj2):
        return obj1 == obj2


class Dict(dict):
    def __init__(self, comparer: IComparer=None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._comparer = comparer or ObjectComparer()

    def __contains__(self, k):
        k = self._comparer.wrap(k)
        return super().__contains__(k)

    def __delitem__(self, k):
        k = self._comparer.wrap(k)
        return super().__delitem__(k)

    def __getitem__(self, k):
        k = self._comparer.wrap(k)
        return super().__getitem__(k)

    def __iter__(self):
        for k in super().__iter__():
            yield k.unwrap()

    def __setitem__(self, k, v):
        k = self._comparer.wrap(k)
        return super().__setitem__(k, v)

    def fromkeys(self, *args):
        if 0 < len(args):
            def iterkeys(i):
                for k in i:
                    yield self._comparer.wrap(k)
            args = list(args)
            args[0] = iterkeys(args[0])
        return super().fromkeys(*args)

    def get(self, k, v):
        k = self._comparer.wrap(k)
        return super().get(k, v)

    def keys(self):
        return [k.unwrap() for k in super().keys()]

    def pop(self, *args):
        if 0 < len(args):
            args = list(args)
            args[0] = self._comparer.wrap(args[0])
        return super().pop(*args)

    def popitem(self):
        k, v = super().popitem()
        return k.unwrap(), v

    def setdefault(self, k, d):
        k = self._comparer.wrap(k)
        return super().setdefault(k, d)

    def update(self, *args, **kwargs):
        raise NotImplementedError


class Set(set):
    def add(self, v):
        size = len(self)
        set.add(self, v)
        return len(self) > size


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
