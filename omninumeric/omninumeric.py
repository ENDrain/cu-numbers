# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.

from enum import Enum, unique


def isinstance(value, condition, msg):
    t = type(value)
    if t == condition:
        return True
    else:
        raise TypeError(msg.format(t))


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


class GreekTypeDictionary(Dictionary):
    @classmethod
    def _getmany(cls, start=1, end=10, step=1):
        r = ""
        for i in range(start * step, end * step, step):
            r += cls(i).name
        return r

    @classmethod
    def digits(cls, start=1, end=10):
        return cls._getmany(start, end, 1)

    @classmethod
    def tens(cls, start=1, end=10):
        return cls._getmany(start, end, 10)

    @classmethod
    def hundreds(cls, start=1, end=10):
        return cls._getmany(start, end, 100)


class NumberConverter:
    def _convert(self, value, condition, msg):
        if isinstance(value, condition, msg):
            return self


class ArabicNumberConverter(NumberConverter):
    def _prepare(self):
        "Prepare the Arabic number for conversion."

        if self._arabic <= 0:
            raise ValueError("Non-zero integer required")

    def __init__(self, value, flags=0):
        self._alphabetic = ""
        self._arabic = value
        self._flags = flags
        self._groups = []
        self._prepare()

    def _get(self):
        "Return the alphabetic number representation."

        return self._alphabetic

    def _hasFlag(self, flag):
        "Check if a flag is set."

        return self._flags & flag
        # return False if self._flags & flag == 0 else True

    def _convert(self):
        if super()._convert(self._arabic, int, "Non-zero integer required, got {0}"):
            return self


class AlphabeticNumberConverter(NumberConverter):

    _dict = Dictionary

    def _prepare(self):
        "Prepare the alphabetic number for conversion."

        if self._alphabetic:
            self._alphabetic = str.lower(str.strip(self._alphabetic))
            return self
        else:
            raise ValueError("Non-empty string required")

    def __init__(self, alphabetic):

        self._alphabetic = alphabetic
        self._arabic = 0
        self._groups = []
        self._prepare()

    def _get(self):
        "Return the Arabic number representation."

        return self._arabic

    @classmethod
    def _translate(cls, alphabetic):

        total = 0  # Current group total value
        for k in alphabetic:
            total += cls._dict.get(k)

        return total

    def _convert(self):
        if super()._convert(
            self._alphabetic, str, "Non-empty string required, got {0}"
        ):
            return self
