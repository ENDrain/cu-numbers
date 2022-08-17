# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included with the project.
"This module provides basic tools for reading and writing numbers in Greek-type alphabetic numeral systems."

import re

from omninumeric import (
    Dictionary,
    IntNumberConverter,
    StrNumberConverter,
)


PLAIN = 0  # Write in plain style flag
DELIM = 0b1  # Read/write in delim style flag


class DictionaryGreek(Dictionary):
    """
    ABC for Greek-type alphabetic numeral systems ditcionaries.

    Derive from this class to define numeral dictionaries for Greek type alphabetic numeral systems.
    """

    @classmethod
    def _getmany(cls, start=1, end=10, step=1):
        """
        Look a range of numerals up in dictionary.

        @start - starting numeral value (i.e. 5 for range of 5, 6, 7...)
        @end - ending numeral value (i.e. 5 for range of ...3, 4, 5)
        step - numeral value increment (i.e. 1 for range of 1, 2, 3...; 10 for range of 10, 20, 30...)
        """

        r = ""
        for i in range(start * step, (end + 1) * step, step):
            r += cls(i).name
        return r

    @classmethod
    def digits(cls, start=1, end=9):
        """
        Get a range of numerals in digits registry.

        @start - starting numeral value (i.e. 5 for range of 5, 6, 7...)
        @end - ending numeral value (i.e. 5 for range of ...3, 4, 5)
        """
        return cls._getmany(start, end, 1)

    @classmethod
    def tens(cls, start=1, end=9):
        """
        Get a range of numerals in tens registry.

        @start - starting numeral value (i.e. 5 for range of 50, 60, 70...)
        @end - ending numeral value (i.e. 5 for range of ...30, 40, 50)
        """
        return cls._getmany(start, end, 10)

    @classmethod
    def hundreds(cls, start=1, end=9):
        """
        Get a range of numerals in hundreds registry.

        @start - starting numeral value (i.e. 5 for range of 500, 600, 700...)
        @end - ending numeral value (i.e. 5 for range of ...300, 400, 500)
        """
        return cls._getmany(start, end, 100)


class IntNumberConverterGreek(IntNumberConverter):
    """
    ABC for number conversion into Greek-type alphabetic numeral systems.

    Derive from this class to define converters into Greek-type alphabetic numeral systems.
    """

    def _appendThousandMarks(self, cond):
        "Append thousand marks according to chosen style (plain or delimeter)."

        for i, k in enumerate(self._groups):

            if k:
                if cond:
                    result = "{0}{1}".format(self._dict.get("THOUSAND") * i, k)

                else:
                    result = ""

                    for l in k:
                        result = "{0}{1}{2}".format(
                            result, self._dict.get("THOUSAND") * i, l
                        )

                self._groups[i] = result

        return self

    def _translateGroups(self):
        "Translate groups of numerals one by one."

        for i, k in enumerate(self._groups):

            result = ""
            index = 0

            while k > 0:
                result = self._getNumeral(k % 10 * pow(10, index)) + result
                index = index + 1
                k = k // 10

            self._groups[i] = result

        return self

    def _breakIntoGroups(self):
        "Break source number into groups of 3 numerals."

        while self._source > 0:
            self._groups.append(self._source % 1000)
            self._source = self._source // 1000

        return self


class StrNumberConverterGreek(StrNumberConverter):
    """
    ABC for number conversion from Greek-type alphabetic numeral systems.

    Derive from this class to define converters from Greek-type alphabetic numeral systems.
    """

    @classmethod
    def _calculateMultiplier(cls, index, group):
        'Calculate multiplier for a numerals group, according to group index or "thousand" marks present in the group.'

        multiplier = (
            re.match("({0}*)".format(cls._dict.get("THOUSAND")), group)
            .groups()[0]
            .count(cls._dict.get("THOUSAND"))
        )  # Count trailing thousand marks in the group
        multiplier = pow(1000, multiplier if multiplier else index)
        # Use thousand marks if present, otherwise use group index
        return multiplier

    def _translateGroups(self):
        "Translate groups of numerals one by one."

        for i, k in enumerate(self._groups):
            total = 0  # Current group total value
            multiplier = self._calculateMultiplier(i, k)
            k = re.sub(self._dict.get("THOUSAND"), "", k)  # Strip thousand marks

            for l in k:
                total += self._getNumeral(l)

            self._groups[i] = total * multiplier

        return self

    def _breakIntoGroups(self, regex=""):
        "Break source number in groups of 1-3 numerals."

        self._groups = re.split(regex, self._source)  # Break into groups
        self._groups.reverse()  # Reverse groups (to ascending order)

        return self
