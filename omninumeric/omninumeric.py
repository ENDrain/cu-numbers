# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.

from enum import Enum, unique


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
    def __getmany(cls, start=1, end=10, step=1):
        r = ""
        for i in range(start * step, end * step, step):
            r += cls(i).name
        return r

    @classmethod
    def digits(cls, start=1, end=10):
        return cls.__getmany(start, end, 1)

    @classmethod
    def tens(cls, start=1, end=10):
        return cls.__getmany(start, end, 10)

    @classmethod
    def hundreds(cls, start=1, end=10):
        return cls.__getmany(start, end, 100)


class ArabicNumberConverter:

    dict = Dictionary

    def prepare(self):
        "Prepare the Arabic number for conversion."

        if self.arabic <= 0:
            raise ValueError("Non-zero integer required")

    def __init__(self, value, flags=0):
        self.alphabetic = ""
        self.arabic = value
        self.flags = flags
        self.groups = []
        self.prepare()

    def get(self):
        "Return the alphabetic number representation."

        return self.alphabetic

    def hasFlag(self, flag):
        "Check if a flag is set."

        return self.flags & flag
        # return False if self.flags & flag == 0 else True


class AlphabeticNumberConverter:

    dict = Dictionary

    def prepare(self):
        "Prepare the alphabetic number for conversion."

        if self.alphabetic:
            self.alphabetic = str.lower(str.strip(self.alphabetic))
            # self.alphabetic = str.lower(self.alphabetic)
            return self
        else:
            raise ValueError("Non-empty string required")

    def __init__(self, alphabetic):

        self.alphabetic = alphabetic
        self.arabic = 0
        self.groups = []
        self.prepare()

    def get(self):
        "Return the Arabic number representation."

        return self.arabic

    @classmethod
    def translate(cls, alphabetic):

        total = 0  # Current group total value
        for k in alphabetic:
            total += cls.dict.get(k)

        return total


def isinstance(input, condition, msg):
    t = type(input)
    if t == condition:
        return True
    else:
        raise TypeError(msg.format(t))
