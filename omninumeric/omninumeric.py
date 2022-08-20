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
                return None


class NumberConverter:
    _dict = NotImplemented

    def __init__(self, flags=0):

        self._source = 0
        self._target = ""
        self._flags = flags
        self._groups = []

    def _hasFlag(self, flag):
        "Check if a flag is set."

        return self._flags & flag
        # return False if self._flags & flag == 0 else True

    @classmethod
    def _getNumeral(cls, numeral, fallback):
        "Get a numeral or its value from dictionary."

        return cls._dict.get(numeral) or fallback

    def _purgeEmptyGroups(self):
        "Remove empty groups from digit group collection."

        for i, k in enumerate(self._groups):

            if not k:
                self._groups.pop(i)  # Purge empty groups

        return self

    def convert(self):
        raise NotImplementedError


class IntNumberConverter(NumberConverter):
    def __init__(self, value, flags=0):

        super().__init__(flags)
        self._source = value
        self._target = ""

    def _get(self):
        "Return the alphabetic number representation."

        return self._target

    def _validate(self):
        "Validate that input is a natural Arabic number."

        isinstance(self._source, int, "Integer required, got {0}")

        if self._source <= 0:
            raise ValueError("Natural number required")

        return self

    @classmethod
    def _getNumeral(cls, numeral):
        "Get alphabetical digit for given Arabic digit."

        return super()._getNumeral(numeral, "")


class StrNumberConverter(NumberConverter):
    def __init__(self, alphabetic, flags=0):

        super().__init__(flags)
        self._source = alphabetic
        self._target = 0

    def _get(self):
        "Return the Arabic number representation."

        return self._target

    def _validate(self):
        "Validate that input is a alphabetic number in appropriate writing system."

        isinstance(self._source, str, "String required, got {0}")

        if not self._source:
            raise ValueError("Non-empty string required")

        return self

    def _prepare(self):
        "Prepare the alphabetic number for conversion."

        self._source = str.lower(str.strip(self._source))
        return self

    @classmethod
    def _getNumeral(cls, numeral):
        "Get alphabetical digit for given Arabic digit."

        return super()._getNumeral(numeral, 0)
