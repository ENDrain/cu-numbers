# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included with the project.
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

    _dict = NotImplemented

    def __init__(self, source, target, flags=0):
        self._source = source
        self._target = target
        self._flags = flags
        self._groups = []

    def _hasFlag(self, flag):
        "Check if a flag is set."

        return self._flags & flag
        # return False if self._flags & flag == 0 else True

    def _get(self):
        "Return the converted number."

        return self._target

    def _build(self):
        "Build the converted number from groups of numerals."

        for k in self._groups:
            self._target = k + self._target
        return self

    @classmethod
    def _getNumeral(cls, numeral, fallback):
        """
        Look a numeral up in dictionary.

        @numeral - numeral to look up
        @fallback - value to return if @numeral is not found
        """

        return cls._dict.get(numeral) or fallback

    def _purgeEmptyGroups(self):
        "Remove empty groups from numeral groups collection."

        print(self._groups)
        while self._groups.count(""):
            self._groups.remove("")  # Purge empty groups
        print(self._groups)
        return self

    def convert(self):
        raise NotImplementedError


class IntNumberConverter(NumberConverter):
    """
    ABC for number conversion into alphabetic numeral systems.

    Derive from this class to define converters into alphabetic numeral systems.
    """

    def __init__(self, value, flags=0):
        super().__init__(value, "", flags)

    def _validate(self):
        "Validate that source number is a natural number."

        isinstanceEx(self._source, int, "Integer required, got {0}")

        if self._source <= 0:
            raise ValueError("Natural number required")

        return self

    @classmethod
    def _getNumeral(cls, numeral):
        "Get alphabetic digit for given value."

        return super()._getNumeral(numeral, "")


class StrNumberConverter(NumberConverter):
    """
    ABC for number conversion from alphabetic numeral systems.

    Derive from this class to define converters from ABS.
    """

    def __init__(self, alphabetic, flags=0):
        super().__init__(alphabetic, 0, flags)

    def _validate(self):
        "Validate that source number is a non-empty string."

        isinstanceEx(self._source, str, "String required, got {0}")

        if not self._source:
            raise ValueError("Non-empty string required")

        return self

    def _prepare(self):
        "Prepare source number for further operations."

        self._source = str.lower(str.strip(self._source))
        return self

    @classmethod
    def _getNumeral(cls, numeral):
        "Get value for given alphabetic digit."

        return super()._getNumeral(numeral, 0)
