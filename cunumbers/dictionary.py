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


class HebrewTypeDictionary(Dictionary):
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
