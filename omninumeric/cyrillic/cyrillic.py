# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
# To learn about Cyrillic numeral system (CU), see INTRODUCTION.md
"This module provides tools for reading and writing numbers in Cyrillic numeral system."

import re
from omninumeric import greek


PLAIN = greek.PLAIN  # Write in plain style flag
DELIM = greek.DELIM  # Read/write in delim style flag
NOTITLO = 0b10  # DO NOT append titlo flag
ENDDOT = 0b100  # Append dot flag
PREDOT = 0b1000  # Prepend dot flag
DOT = 0b10000  # Delimeter dots flag
DELIMDOT = DOT | DELIM  # Delimeter dots flag (forces delim style)
WRAPDOT = ENDDOT | PREDOT  # Wrap in dots flag
ALLDOT = ENDDOT | PREDOT | DELIMDOT  # Wrapper and delimeter dots flag


class Dictionary(greek.Dictionary):
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


class Const:
    THOUSAND = "҂"  # "Thousand" mark
    TITLO = "҃"  # "Titlo" decorator
    DELIMETER = "."  # Dot decorator


class IntConverter(greek.IntConverter):
    "Number converter into Cyrillic numeral system."

    dict_ = Dictionary
    const = Const

    def ambiguityCheck(self, cond, flag):
        "Force delimeter for ambiguous numbers (i.e. ҂а҃і and ҂а.і҃)."
        if self.hasFlag(cond):
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
                "({0})([{1}])".format(self.dict_.get(10), self.dict_.digits()),
                "\g<2>\g<1>",
                self.groups[i],
            )

        return self

    def appendTitlo(self, cond):
        'Apply "titlo" decorator unless appropriate flag is set.'

        if not self.hasFlag(cond):
            result = re.subn(
                "([\S]+)(?<![{0}\{1}])([\S])$".format(
                    self.const.THOUSAND, self.const.DELIMETER
                ),
                "\g<1>{0}\g<2>".format(self.const.TITLO),
                self.target,
            )
            self.target = (
                result[0]
                if result[1] > 0
                else "{0}{1}".format(self.target, self.const.TITLO)
            )

        return self

    def delimDots(self, cond):
        "Insert dots between numeral groups if appropriate flag is set."

        if self.hasFlag(cond):
            for i, k in enumerate(self.groups[1:]):
                self.groups[i + 1] = "{0}{1}".format(k, self.const.DELIMETER)

        return self

    def wrapDot(self, cond_a, cond_b):
        "Prepend and/or append a dot if appropriate flags are set."

        self.target = "{0}{1}{2}".format(
            self.const.DELIMETER if self.hasFlag(cond_a) else "",
            self.target,
            self.const.DELIMETER if self.hasFlag(cond_b) else "",
        )

        return self

    def appendThousandMarks(self, cond):
        return super().appendThousandMarks(self.hasFlag(cond), self.const.THOUSAND)

    def convert(self):
        "Convert into Cyrillic numeral system. Uses plain style by default."

        return (
            self.validate()
            .breakIntoGroups()
            .ambiguityCheck(DELIM, DOT)
            .translateGroups()
            .appendThousandMarks(DELIM)
            .purgeEmptyGroups()
            .swapDigits()
            .delimDots(DOT)
            .build()
            .appendTitlo(NOTITLO)
            .wrapDot(PREDOT, ENDDOT)
            .get()
        )


class StrConverter(greek.StrConverter):
    "Number converter from Cyrillic numeral system."

    dict_ = Dictionary
    const = Const

    regex = "({0}*[{1}]?(?:(?:{0}*[{3}])?{4}|(?:{0}*[{2}])?(?:{0}*[{3}])?))".format(
        const.THOUSAND,
        dict_.hundreds(),
        dict_.tens(2),
        dict_.digits(),
        dict_.get(10),
    )  # Regular expression for typical Cyrillic numeral system number

    def prepare(self):
        "Prepare source number for conversion."

        super().prepare()
        self.source = re.sub(
            "[{0}\{1}]".format(self.const.TITLO, self.const.DELIMETER),
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

    @classmethod
    def calculateMultiplier(cls, index, group):
        return super().calculateMultiplier(index, group, cls.const.THOUSAND)

    def breakIntoGroups(self):
        return super().breakIntoGroups(self.regex)

    def translateGroups(self):
        return super().translateGroups(self.const.THOUSAND)

    def convert(self):
        "Convert from Cyrillic numeral system."

        return (
            self.prepare()
            .validate()
            .breakIntoGroups()
            .purgeEmptyGroups()
            .translateGroups()
            .build()
            .get()
        )


def write(number, flags=0):
    """
    Convert into Cyrillic numeral system. Uses plain style by default.

    Requires a non-zero integer.
    """

    return IntConverter(number, flags).convert()


def read(number, flags=0):
    """
    Convert from Cyrillic numeral system.

    Requires a non-empty string.
    """

    return StrConverter(number, flags).convert()
