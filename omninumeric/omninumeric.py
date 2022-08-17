# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.

import re
from enum import Enum, unique


def isinstance(value, cond, msg):

    t = type(value)
    if not t == cond:
        raise TypeError(msg.format(t))


@unique
class Dictionary(Enum):
    @classmethod
    def get(cls, input):
        try:
            return cls[input].value
        except:
            try:
                return cls(input).name
            except:
                return ""


class NumberConverter:
    _dict = NotImplemented

    def __init__(self, flags=0):

        self._arabic = 0
        self._alphabetic = ""
        self._flags = flags
        self._groups = []

    def _hasFlag(self, flag):
        "Check if a flag is set."

        return self._flags & flag
        # return False if self._flags & flag == 0 else True

    def convert(self):
        raise NotImplementedError


class ArabicNumberConverter(NumberConverter):
    def __init__(self, value, flags=0):

        super().__init__(flags)
        self._arabic = value

    def _get(self):
        "Return the alphabetic number representation."

        return self._alphabetic

    def _validate(self):
        "Validate that input is a natural Arabic number."

        isinstance(self._arabic, int, "Integer required, got {0}")

        if self._arabic <= 0:
            raise ValueError("Natural number required")

        return self


class AlphabeticNumberConverter(NumberConverter):
    def __init__(self, alphabetic, flags=0):

        super().__init__(flags)
        self._alphabetic = alphabetic

    def _get(self):
        "Return the Arabic number representation."

        return self._arabic

    def _validate(self):
        "Validate that input is a alphabetic number in appropriate writing system."

        isinstance(self._alphabetic, str, "String required, got {0}")

        if not self._alphabetic:
            raise ValueError("Non-empty string required")

        return self

    def _prepare(self):
        "Prepare the alphabetic number for conversion."

        self._alphabetic = str.lower(str.strip(self._alphabetic))

    @classmethod
    def _translate(cls, alphabetic):

        total = 0  # Current group total value
        for k in alphabetic:
            total += cls._dict.get(k)

        return total
