# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
"This module provides basic tools for reading and writing numbers in alphabetic numeral systems."

import re
from enum import Enum, unique


def isinstanceEx(value, cond, msg=""):
    """
    Test if value is of a speciic type, raise error with specified message if not.

    @value - value to test
    @cond - type to test against
    @msg - error message to print. Supports format() to print @value type
    """

    t = type(value)
    if not t == cond:
        raise TypeError(msg.format(t))


@unique
class Dictionary(Enum):
    """
    ABC for alphabetic numeral systems dictionaries.

    Derive from this class to define numeral dictionaries for alphabetic numeral systems.
    """

    @classmethod
    def get(cls, numeral):
        """
        Look a numeral up in dictionary.

        @numeral - str or int to look up. Returns int if str is found and vice versa, returns None if nothing found
        """

        try:
            return cls[numeral].value
        except:
            try:
                return cls(numeral).name
            except:
                return None


class NumberConverter:
    """
    ABC for number conversion.

    Derive from this class to define converters into and from alphabetic numeral systems.
    """

    dict_ = NotImplemented
    const = NotImplemented

    def __init__(self, source, target, flags=0):
        self.source = source
        self.target = target
        self.flags = flags
        self.groups = []

    def hasFlag(self, flag):
        "Check if a flag is set."

        return self.flags & flag

    def get(self):
        "Return the converted number."

        return self.target

    def build(self):
        "Build the converted number from groups of numerals."

        for k in self.groups:
            self.target = k + self.target
        return self

    @classmethod
    def getNumeral(cls, numeral, fallback):
        """
        Look a numeral up in dictionary.

        @numeral - numeral to look up
        @fallback - value to return if @numeral is not found
        """

        return cls.dict_.get(numeral) or fallback

    def purgeEmptyGroups(self):
        "Remove empty groups from numeral groups collection."

        while self.groups.count(""):
            self.groups.remove("")  # Purge empty groups
        return self

    def convert(self):
        raise NotImplementedError


class IntConverter(NumberConverter):
    """
    ABC for number conversion into alphabetic numeral systems.

    Derive from this class to define converters into alphabetic numeral systems.
    """

    def __init__(self, value, flags=0):
        super().__init__(value, "", flags)

    def validate(self):
        "Validate that source number is a natural number."

        isinstanceEx(self.source, int, "Integer required, got {0}.")

        if self.source <= 0:
            raise ValueError("Natural number required.")

        return self

    @classmethod
    def getNumeral(cls, numeral):
        "Get alphabetic digit for given value."

        return super().getNumeral(numeral, "")


class StrConverter(NumberConverter):
    """
    ABC for number conversion from alphabetic numeral systems.

    Derive from this class to define converters from alphabetic numeral systems.
    """

    def __init__(self, alphabetic, flags=0):
        super().__init__(alphabetic, 0, flags)

    def validate(self):
        "Validate that source number is a non-empty string."

        isinstanceEx(self.source, str, "String required, got {0}.")

        if not self.source:
            raise ValueError("Non-empty string required.")

        return self

    def prepare(self):
        "Prepare source number for further operations."

        self.source = str.strip(self.source)
        return self

    @classmethod
    def getNumeral(cls, numeral):
        "Get value for given alphabetic digit."

        return super().getNumeral(numeral, 0)
