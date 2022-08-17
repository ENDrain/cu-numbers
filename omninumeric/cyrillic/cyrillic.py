# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included with the project.
# To learn about Cyrillic numeral system (CU), see INTRODUCTION.md
"This module provides tools for reading and writing numbers in Cyrillic numeral system."

import re
from omninumeric.greek import *


CU_PLAIN = PLAIN  # Write in plain style flag
CU_DELIM = DELIM  # Read/write in delim style flag
CU_NOTITLO = 0b10  # DO NOT append titlo flag
CU_ENDDOT = 0b100  # Append dot flag
CU_PREDOT = 0b1000  # Prepend dot flag
CU_DOT = 0b10000  # Delimeter dots flag
CU_DELIMDOT = CU_DOT | CU_DELIM  # Delimeter dots flag (forces delim style)
CU_WRAPDOT = CU_ENDDOT | CU_PREDOT  # Wrap in dots flag
CU_ALLDOT = CU_ENDDOT | CU_PREDOT | CU_DELIMDOT  # Wrapper and delimeter dots flag


class _CyrillicDictionary(DictionaryGreek):
    "Cyrillic numerals ditcionary."

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


class ArabicNumber(IntNumberConverterGreek):
    "Number converter into Cyrillic numeral system."

    _dict = _CyrillicDictionary

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

    def _swapDigits(self):
        "Swap digits for values 11-19 (unless separated)."

        for i, k in enumerate(self._groups):

            self._groups[i] = re.sub(
                "({0})([{1}])".format(self._dict.get(10), self._dict.digits()),
                "\g<2>\g<1>",
                self._groups[i],
            )

        return self

    def _appendTitlo(self, cond):
        'Apply "titlo" decorator unless appropriate flag is set.'

        if not cond:
            result = re.subn(
                "([\S]+)(?<![{0}\{1}])([\S])$".format(
                    self._dict.get("THOUSAND"), self._dict.get("DOT")
                ),
                "\g<1>{0}\g<2>".format(self._dict.get("TITLO")),
                self._target,
            )
            self._target = (
                result[0]
                if result[1] > 0
                else "{0}{1}".format(self._target, self._dict.get("TITLO"))
            )

        return self

    def _delimDots(self, cond):
        "Insert dots between numeral groups if appropriate flag is set."

        if cond:
            for i, k in enumerate(self._groups[1:]):
                self._groups[i + 1] = "{0}{1}".format(k, self._dict.get("DOT"))

        return self

    def _wrapDot(self, cond_a, cond_b):
        "Prepend and/or append a dot if appropriate flags are set."

        self._target = "{0}{1}{2}".format(
            self._dict.get("DOT") if cond_a else "",
            self._target,
            self._dict.get("DOT") if cond_b else "",
        )

        return self

    def convert(self):
        """
        Convert into Cyrillic numeral system. Uses plain style by default.

        Requires a non-zero integer.
        """

        return (
            self._validate()
            ._breakIntoGroups()
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


class CyrillicNumber(StrNumberConverterGreek):
    "Number converter from Cyrillic numeral system."

    _dict = _CyrillicDictionary

    _regex = "({0}*[{1}]?(?:(?:{0}*[{3}])?{4}|(?:{0}*[{2}])?(?:{0}*[{3}])?))".format(
        _dict.get("THOUSAND"),
        _dict.hundreds(),
        _dict.tens(2),
        _dict.digits(),
        _dict.get(10),
    )  # Regular expression for typical Cyrillic numeral system number

    def _prepare(self):
        "Prepare source number for conversion."

        super()._prepare()
        self._source = re.sub(
            "[{0}\{1}]".format(self._dict.get("TITLO"), self._dict.get("DOT")),
            "",
            self._source,
        )  # Strip ҃decorators

        return self

    def _validate(self):
        "Validate that source number is a non-empty string and matches the pattern for Cyrillic numeral system numbers."

        super()._validate()
        if not re.fullmatch("{0}+".format(self._regex), self._source):
            raise ValueError(
                "String does not match any pattern for Cyrillic numeral system numbers"
            )

        return self

    def convert(self):
        """
        Convert from Cyrillic numeral system.

        Requires a non-empty string.
        """

        return (
            self._prepare()
            ._validate()
            ._breakIntoGroups(self._regex)
            ._purgeEmptyGroups()
            ._translateGroups()
            ._build()
            ._get()
        )


def to_cu(integer, flags=0):
    "Deprecated. Use ArabicNumber().convert() instead."

    return ArabicNumber(integer, flags).convert()


def to_arab(alphabetic, flags=0):
    "Deprecated. Use CyrillicNumber().convert() instead."

    return CyrillicNumber(alphabetic).convert()
