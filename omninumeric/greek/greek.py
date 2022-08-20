# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.

import re

from omninumeric import (
    Dictionary,
    ArabicNumberConverter,
    AlphabeticNumberConverter,
)


PLAIN = 0  # Write in plain style
DELIM = 0b1  # Read/write in delim style


class DictionaryGreek(Dictionary):
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


class ArabicNumberConverterGreek(ArabicNumberConverter):
    def _build(self):
        "Build the CU number from digit groups."

        for k in self._groups:
            self._alphabetic = "{0}{1}".format(k, self._alphabetic)
        return self

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

    @classmethod
    def _getDigit(cls, input):

        return cls._dict.get(input) if input else ""

    def _translateGroups(self):
        "Translate the Arabic number per group."

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
        "Break the Arabic number into groups of 3 digits."

        while self._arabic > 0:
            self._groups.append(self._arabic % 1000)
            self._arabic = self._arabic // 1000

        return self


class AlphabeticNumberConverterGreek(AlphabeticNumberConverter):
    @classmethod
    def _calculateMultiplier(cls, index, input):
        "Calculate multiplier for adjusting digit group value to its registry."

        multiplier = (
            re.match("({0}*)".format(cls._dict.get("THOUSAND")), input)
            .groups()[0]
            .count(cls._dict.get("THOUSAND"))
        )  # Count trailing thousand marks in the group
        multiplier = pow(1000, multiplier if multiplier else index - 1)
        # Use thousand marks if present, otherwise use group index
        return multiplier

    @classmethod
    def _translate(cls, alphabetic):

        total = 0  # Current group total value
        for k in alphabetic:
            total += cls._dict.get(k)

        return total

    def _translateGroups(self):
        "Translate the alphabetic number per group."

        for i, k in enumerate(self._groups):

            multiplier = self._calculateMultiplier(i, k)
            k = re.sub(self._dict.get("THOUSAND"), "", k)  # Strip thousand marks
            self._arabic += self._translate(k) * multiplier

        return self

    def _breakIntoGroups(self, regex=""):
        "Break the Cyrillic number in groups of 1-3 digits."

        self._groups = re.split(regex, self._alphabetic)  # Break into groups
        self._groups.reverse()  # Reverse groups (to ascending order)

        return self
