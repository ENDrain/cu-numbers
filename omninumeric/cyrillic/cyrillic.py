# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
# To learn about Cyrillic numeral system (CU), see INTRODUCTION.md
"Module for number conversion between Arabic and Cyrillic numeral systems."

import re
from omninumeric import (
    GreekTypeDictionary,
    ArabicNumberConverter,
    AlphabeticNumberConverter,
)

CU_PLAIN = 0x1  # Write in plain style
CU_DELIM = 0x10  # Read/write in delim style
CU_NOTITLO = 0x100  # DO NOT append titlo
CU_ENDDOT = 0x1000  # Append dot
CU_PREDOT = 0x10000  # Prepend dot
CU_DOT = 0x100000  # Delimeter dots (private, for internal flag checks)
CU_DELIMDOT = CU_DOT | CU_DELIM  # Delimeter dots (forces delim style)
CU_WRAPDOT = CU_ENDDOT | CU_PREDOT  # Wrap in dots
CU_ALLDOT = CU_ENDDOT | CU_PREDOT | CU_DELIMDOT  # Wrapper and delimeter dots


class CyrillicDictionary(GreekTypeDictionary):

    а = 1
    в = 2
    г = 3
    д = 4
    є = 5
    ѕ = 6
    з = 7
    и = 8
    ѳ = 9
    і = 10
    к = 20
    л = 30
    м = 40
    н = 50
    ѯ = 60
    ѻ = 70
    п = 80
    ч = 90
    р = 100
    с = 200
    т = 300
    у = 400
    ф = 500
    х = 600
    ѱ = 700
    ѿ = 800
    ц = 900
    THOUSAND = "҂"  # "Thousand" mark
    TITLO = "҃"  # "Titlo" decorator
    DOT = "."  # Dot decorator


class ArabicNumber(ArabicNumberConverter):
    _dict = CyrillicDictionary

    def __init__(self, value, flags=0):
        super().__init__(value, flags)

    def _build(self):
        "Build the CU number from digit groups."

        for k in self._groups:
            self._alphabetic = "{0}{1}".format(k, self._alphabetic)

        return self

    def _wrapDot(self, cond_a, cond_b):
        "Prepend and/or append dots if appropriate flags are set."

        self._alphabetic = "{0}{1}{2}".format(
            self._dict.get("DOT") if cond_a else "",
            self._alphabetic,
            self._dict.get("DOT") if cond_b else "",
        )

        return self

    def _delimDots(self, cond):
        "Insert dots between digit groups if appropriate flag is set."

        if cond:
            for i, k in enumerate(self._groups[1:]):
                self._groups[i + 1] = "{0}{1}".format(k, self._dict.get("DOT"))

        return self

    def _appendTitlo(self, cond):
        "Append titlo unless appropriate flag is set."

        if not cond:
            result = re.subn(
                "([\S]+)(?<![{0}\{1}])([\S])$".format(
                    self._dict.get("THOUSAND"), self._dict.get("DOT")
                ),
                "\g<1>{0}\g<2>".format(self._dict.get("TITLO")),
                self._alphabetic,
            )
            self._alphabetic = (
                result[0]
                if result[1] > 0
                else "{0}{1}".format(self._alphabetic, self._dict.get("TITLO"))
            )

        return self

    def _swapDigits(self):
        "Swap digits in 11-19."

        for i, k in enumerate(self._groups):

            self._groups[i] = re.sub(
                "({0})([{1}])".format(self._dict.get(10), self._dict.digits()),
                "\g<2>\g<1>",
                self._groups[i],
            )

        return self

    def _purgeEmptyGroups(self):
        "Remove empty groups from digit group collection."

        for i, k in enumerate(self._groups):

            if not k:
                self._groups.pop(i)

        return self

    @classmethod
    def _appendThousandMarksDelim(cls, input, index):
        "Append thousand marks in delimeter style."

        if input:
            return "{0}{1}".format(cls._dict.get("THOUSAND") * index, input)
        else:
            return ""

    @classmethod
    def _appendThousandMarksPlain(cls, input, index):
        "Append thousand marks in plain style."

        result = ""

        for i in input:
            result = "{0}{1}".format(result, cls._appendThousandMarksDelim(i, index))

        return result

    def _appendThousandMarks(self, cond):
        "Append thousand marks according to chosen style (plain or delimeter)."

        method = (
            self._appendThousandMarksDelim if cond else self._appendThousandMarksPlain
        )

        for i, k in enumerate(self._groups):

            self._groups[i] = method(self._groups[i], i)

        return self

    @classmethod
    def _getDigit(cls, input):
        "Get CU digit for given Arabic digit."

        return cls._dict.get(input) if input else ""

    def _translateGroups(self):
        "Translate the Arabic number per group."

        for i, k in enumerate(self._groups):

            result = ""
            index = 0

            while k > 0:
                result = self._getDigit(k % 10 * pow(10, index)) + result
                index = index + 1
                k = k // 10

            self._groups[i] = result

        return self

    def _ambiguityCheck(self, cond, flag):
        if cond:
            try:
                if (self._groups[0] // 10 % 10 == 1) and (
                    self._groups[1] // 10 % 10 == 0
                ):
                    self._flags = self._flags | flag
            finally:
                return self
        else:
            return self

    def _breakIntoGroups(self):
        "Break the Arabic number into groups of 3 digits."

        while self._arabic > 0:
            self._groups.append(self._arabic % 1000)
            self._arabic = self._arabic // 1000

        return self

    def convert(self):
        """
        Convert an Arabic number into Cyrillic numeral system. Uses plain style by default.

        Requires a non-zero integer.
        """

        if super()._convert():
            return (
                self._breakIntoGroups()
                ._ambiguityCheck(self._hasFlag(CU_DELIM), CU_DOT)
                ._translateGroups()
                ._appendThousandMarks(self._hasFlag(CU_DELIM))
                ._purgeEmptyGroups()
                ._swapDigits()
                ._delimDots(self._hasFlag(CU_DOT))
                ._build()
                ._appendTitlo(self._hasFlag(CU_NOTITLO))
                ._wrapDot(self._hasFlag(CU_PREDOT), self._hasFlag(CU_ENDDOT))
                ._get()
            )


class CyrillicNumber(AlphabeticNumberConverter):

    _dict = CyrillicDictionary

    _regex = "({0}*[{1}]?(?:(?:{0}*[{3}])?{4}|(?:{0}*[{2}])?(?:{0}*[{3}])?))".format(
        _dict.get("THOUSAND"),
        _dict.hundreds(),
        _dict.tens(2),
        _dict.digits(),
        _dict.get(10),
    )

    def _validate(self):
        "Validate that input is a Cyrillic number."

        if re.fullmatch("{0}+".format(self._regex), self._alphabetic):
            return self
        else:
            raise ValueError(
                "String does not match any pattern for Cyrillic numeral system number"
            )

    def __init__(self, alphabetic):
        super().__init__(alphabetic)
        self._validate()

    def _prepare(self):
        "Prepare the Cyrillic number for conversion."

        if super()._prepare():
            self._alphabetic = re.sub(
                "[{0}\.]".format(self._dict.get("TITLO")), "", self._alphabetic
            )  # Strip ҃"҃ " and dots
            return self

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

    def _translateGroups(self):
        "Translate the alphabetic number per group."

        for i, k in enumerate(self._groups):

            multiplier = self._calculateMultiplier(i, k)
            k = re.sub(self._dict.get("THOUSAND"), "", k)  # Strip thousand marks
            self._arabic += self._translate(k) * multiplier

        return self

    def _breakIntoGroups(self):
        "Break the Cyrillic number in groups of 1-3 digits."

        self._groups = re.split(self._regex, self._alphabetic)  # Break into groups
        for i, k in enumerate(self._groups):
            self._groups.pop(i) if not k else True  # Purge empty groups
        self._groups.reverse()  # Reverse groups (to ascending order)

        return self

    def convert(self):
        """
        Convert a Cyrillic number into Arabic numeral system.

        Requires a non-empty string.
        """

        if super()._convert():
            return self._breakIntoGroups()._translateGroups()._get()


def to_cu(integer, flags=0):
    "Deprecated; use ArabicNumber().convert() instead."

    return ArabicNumber(integer, flags).convert()


def to_arab(alphabetic, flags=0):
    "Deprecated; use CyrillicNumber().convert() instead."

    return CyrillicNumber(alphabetic).convert()
