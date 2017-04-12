#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
# wrap any obj as a command class.
# ----------

from ..objects import UInt


class CommandObject:
    def __init__(self, data):
        self._data = data


class ValueCommandObject(CommandObject):
    def get(self):
        return self._data


class SubscriptableCommandObject(CommandObject):
    def get(self, index: UInt):
        index = int(index)
        if index < len(self._data):
            return self._data[index]
        raise ValueError


class DictCommandObject(CommandObject):
    def get(self, key: str):
        return self._data.get(key, None)


class IterableCommandObject(CommandObject):
    def get(self, index: int):
        for item in self._data:
            if index == 0:
                return item
            index -= 1
        raise ValueError


def wrap(obj):
    if isinstance(obj, (list, tuple)):
        return SubscriptableCommandObject(obj)
    elif isinstance(obj, dict):
        return DictCommandObject(obj)
    elif isinstance(obj, (int, float, str)):
        return ValueCommandObject(obj)
    raise NotImplementedError(type(obj))