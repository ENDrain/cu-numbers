# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.

import re
from enum import Enum, unique


def isinstance(value, condition, msg):

    t = type(value)
    if t == condition:
        return True
    else:
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

    def __init__(self, value=0, flags=0):

        self._flags = flags
        return NotImplemented

    def _hasFlag(self, flag):
        "Check if a flag is set."

        return self._flags & flag
        # return False if self._flags & flag == 0 else True

    def convert(self, value, condition, msg):

        if isinstance(value, condition, msg):
            return NotImplemented


class ArabicNumberConverter(NumberConverter):
    def _validate(self):
        "Validate that input is a natural Arabic number."

        if self._arabic <= 0:
            raise ValueError("Natural number integer required")
        return self

    def __init__(self, value, flags=0):

        super().__init__(value, flags)
        self._alphabetic = ""
        self._arabic = value
        self._groups = []
        self._validate()

    def _get(self):
        "Return the alphabetic number representation."

        return self._alphabetic

    def convert(self):
        if super().convert(self._arabic, int, "Non-zero integer required, got {0}"):
            return NotImplemented


class AlphabeticNumberConverter(NumberConverter):

    _regex = NotImplemented

    def _prepare(self):
        "Prepare the alphabetic number for conversion."

        if self._alphabetic:
            self._alphabetic = str.lower(str.strip(self._alphabetic))
            return self
        else:
            raise ValueError("Non-empty string required")

    def _validate(self, regex=""):
        "Validate that input is a alphabetic number in appropriate writing system."

        if re.fullmatch(regex, self._alphabetic):
            return NotImplemented
        else:
            raise ValueError(
                "String does not match any pattern for Cyrillic numeral system number"
            )

    def __init__(self, alphabetic, flags=0):

        super().__init__(alphabetic, flags)
        self._alphabetic = alphabetic
        self._arabic = 0
        self._groups = []
        self._prepare()
        return NotImplemented

    def _get(self):
        "Return the Arabic number representation."

        return self._arabic

    @classmethod
    def _translate(cls, alphabetic):

        total = 0  # Current group total value
        for k in alphabetic:
            total += cls._dict.get(k)

        return total

    def convert(self):

        if super().convert(self._alphabetic, str, "Non-empty string required, got {0}"):
            return NotImplemented
