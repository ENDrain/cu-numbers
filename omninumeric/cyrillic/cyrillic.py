# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
# To learn about Cyrillic numeral system (CU), see INTRODUCTION.md
"Module for number conversion between Arabic and Cyrillic numeral systems."

import re
from omninumeric.greek import *


CU_PLAIN = PLAIN
CU_DELIM = DELIM
CU_NOTITLO = 0b10  # DO NOT append titlo
CU_ENDDOT = 0b100  # Append dot
CU_PREDOT = 0b1000  # Prepend dot
CU_DOT = 0b10000  # Delimeter dots (private, for internal flag checks)
CU_DELIMDOT = CU_DOT | CU_DELIM  # Delimeter dots (forces delim style)
CU_WRAPDOT = CU_ENDDOT | CU_PREDOT  # Wrap in dots
CU_ALLDOT = CU_ENDDOT | CU_PREDOT | CU_DELIMDOT  # Wrapper and delimeter dots


class _CyrillicDictionary(DictionaryGreek):

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


class ArabicNumber(ArabicNumberConverterGreek):
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
        "Swap digits in 11-19."

        for i, k in enumerate(self._groups):

            self._groups[i] = re.sub(
                "({0})([{1}])".format(self._dict.get(10), self._dict.digits()),
                "\g<2>\g<1>",
                self._groups[i],
            )

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

    def _delimDots(self, cond):
        "Insert dots between digit groups if appropriate flag is set."

        if cond:
            for i, k in enumerate(self._groups[1:]):
                self._groups[i + 1] = "{0}{1}".format(k, self._dict.get("DOT"))

        return self

    def _wrapDot(self, cond_a, cond_b):
        "Prepend and/or append dots if appropriate flags are set."

        self._alphabetic = "{0}{1}{2}".format(
            self._dict.get("DOT") if cond_a else "",
            self._alphabetic,
            self._dict.get("DOT") if cond_b else "",
        )

        return self

    def convert(self):
        """
        Convert an Arabic number into Cyrillic numeral system. Uses plain style by default.

        Requires a non-zero integer.
        """

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


class CyrillicNumber(AlphabeticNumberConverterGreek):

    _dict = _CyrillicDictionary

    _regex = "({0}*[{1}]?(?:(?:{0}*[{3}])?{4}|(?:{0}*[{2}])?(?:{0}*[{3}])?))".format(
        _dict.get("THOUSAND"),
        _dict.hundreds(),
        _dict.tens(2),
        _dict.digits(),
        _dict.get(10),
    )

    def _prepare(self):
        "Prepare the Cyrillic number for conversion."

        if super()._prepare():
            self._alphabetic = re.sub(
                "[{0}\.]".format(self._dict.get("TITLO")), "", self._alphabetic
            )  # Strip ҃"҃ " and dots
            return self

    def _validate(self):
        "Validate that input is a Cyrillic number."

        super()._validate("{0}+".format(self._regex))

    def _breakIntoGroups(self):
        return super()._breakIntoGroups(self._regex)

    def convert(self):
        """
        Convert a Cyrillic number into Arabic numeral system.

        Requires a non-empty string.
        """

        return self._breakIntoGroups()._translateGroups()._get()


def to_cu(integer, flags=0):
    "Deprecated; use ArabicNumber().convert() instead."

    return ArabicNumber(integer, flags).convert()


def to_arab(alphabetic, flags=0):
    "Deprecated; use CyrillicNumber().convert() instead."

    return CyrillicNumber(alphabetic).convert()
