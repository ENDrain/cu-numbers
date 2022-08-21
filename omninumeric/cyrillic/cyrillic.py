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


class CyrillicDictionary(DictionaryGreek):
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

    dict = CyrillicDictionary

    def ambiguityCheck(self, cond, flag):
        if cond:
            try:
                if (self.groups[0] // 10 % 10 == 1) and (
                    self.groups[1] // 10 % 10 == 0
                ):
                    self.flags = self.flags | flag
            finally:
                return self
        else:
            return self

    def swapDigits(self):
        "Swap digits for values 11-19 (unless separated)."

        for i, k in enumerate(self.groups):

            self.groups[i] = re.sub(
                "({0})([{1}])".format(self.dict.get(10), self.dict.digits()),
                "\g<2>\g<1>",
                self.groups[i],
            )

        return self

    def appendTitlo(self, cond):
        'Apply "titlo" decorator unless appropriate flag is set.'

        if not cond:
            result = re.subn(
                "([\S]+)(?<![{0}\{1}])([\S])$".format(
                    self.dict.get("THOUSAND"), self.dict.get("DOT")
                ),
                "\g<1>{0}\g<2>".format(self.dict.get("TITLO")),
                self.target,
            )
            self.target = (
                result[0]
                if result[1] > 0
                else "{0}{1}".format(self.target, self.dict.get("TITLO"))
            )

        return self

    def delimDots(self, cond):
        "Insert dots between numeral groups if appropriate flag is set."

        if cond:
            for i, k in enumerate(self.groups[1:]):
                self.groups[i + 1] = "{0}{1}".format(k, self.dict.get("DOT"))

        return self

    def wrapDot(self, cond_a, cond_b):
        "Prepend and/or append a dot if appropriate flags are set."

        self.target = "{0}{1}{2}".format(
            self.dict.get("DOT") if cond_a else "",
            self.target,
            self.dict.get("DOT") if cond_b else "",
        )

        return self

    def convert(self):
        """
        Convert into Cyrillic numeral system. Uses plain style by default.

        Requires a non-zero integer.
        """

        return (
            self.validate()
            .breakIntoGroups()
            .ambiguityCheck(self.hasFlag(CU_DELIM), CU_DOT)
            .translateGroups()
            .appendThousandMarks(self.hasFlag(CU_DELIM))
            .purgeEmptyGroups()
            .swapDigits()
            .delimDots(self.hasFlag(CU_DOT))
            .build()
            .appendTitlo(self.hasFlag(CU_NOTITLO))
            .wrapDot(self.hasFlag(CU_PREDOT), self.hasFlag(CU_ENDDOT))
            .get()
        )


class CyrillicNumber(StrNumberConverterGreek):
    "Number converter from Cyrillic numeral system."

    dict = CyrillicDictionary

    regex = "({0}*[{1}]?(?:(?:{0}*[{3}])?{4}|(?:{0}*[{2}])?(?:{0}*[{3}])?))".format(
        dict.get("THOUSAND"),
        dict.hundreds(),
        dict.tens(2),
        dict.digits(),
        dict.get(10),
    )  # Regular expression for typical Cyrillic numeral system number

    def prepare(self):
        "Prepare source number for conversion."

        super().prepare()
        self.source = re.sub(
            "[{0}\{1}]".format(self.dict.get("TITLO"), self.dict.get("DOT")),
            "",
            self.source,
        )  # Strip ҃decorators

        return self

    def validate(self):
        "Validate that source number is a non-empty string and matches the pattern for Cyrillic numeral system numbers."

        super().validate()
        if not re.fullmatch("{0}+".format(self.regex), self.source):
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
            self.prepare()
            .validate()
            .breakIntoGroups(self.regex)
            .purgeEmptyGroups()
            .translateGroups()
            .build()
            .get()
        )


class Cyrillic:
    def read(number, flags=0):
        """
        Convert from Cyrillic numeral system.

        Requires a non-empty string.
        """

        return CyrillicNumber(number, flags).convert()

    def write(number, flags=0):
        """
        Convert into Cyrillic numeral system. Uses plain style by default.

        Requires a non-zero integer.
        """

        return ArabicNumber(number, flags).convert()


def to_cu(integer, flags=0):
    "Deprecated. Use ArabicNumber().convert() instead."

    return Cyrillic.write(integer, flags)


def to_arab(alphabetic, flags=0):
    "Deprecated. Use CyrillicNumber().convert() instead."

    return Cyrillic.read(alphabetic, flags)
