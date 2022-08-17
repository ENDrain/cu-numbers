# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
# To learn about Cyrillic numeral system (CU), see INTRODUCTION.md
"Module for number conversion between Arabic and Cyrillic numeral systems."

import re
from omninumeric import *

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
    dict = CyrillicDictionary

    def __init__(self, value, flags=0):
        super().__init__(value, flags)

    def build(self):
        "Build the CU number from digit groups."

        for k in self.groups:
            self.alphabetic = k + self.alphabetic
        return self

    def wrapDot(self, cond_a, cond_b):
        "Prepend and/or append dots if appropriate flags are set."

        self.alphabetic = (
            (self.dict.get("DOT") if cond_a else "")
            + self.alphabetic
            + (self.dict.get("DOT") if cond_b else "")
        )

        return self

    def delimDots(self, cond):
        "Insert dots between digit groups if appropriate flag is set."

        if cond:
            for i, k in enumerate(self.groups[1:]):
                self.groups[i + 1] = k + self.dict.get("DOT")

        return self

    def appendTitlo(self, cond):
        "Append titlo unless appropriate flag is set."

        if not cond:
            result = re.subn(
                "([\S]+)(?<![{0}\{1}])([\S])$".format(
                    self.dict.get("THOUSAND"), self.dict.get("DOT")
                ),
                "\g<1>{0}\g<2>".format(self.dict.get("TITLO")),
                self.alphabetic,
            )
            self.alphabetic = (
                result[0] if result[1] > 0 else self.alphabetic + self.dict.get("TITLO")
            )

        return self

    def swapDigits(self):
        "Swap digits in 11-19."

        for i, k in enumerate(self.groups):

            self.groups[i] = re.sub(
                "({0})([{1}])".format(self.dict.get(10), self.dict.digits()),
                "\g<2>\g<1>",
                self.groups[i],
            )

        return self

    def purgeEmptyGroups(self):
        "Remove empty groups from digit group collection."

        for i, k in enumerate(self.groups):

            if not k:
                self.groups.pop(i)

        return self

    @classmethod
    def appendThousandMarksDelim(cls, input, index):
        "Append thousand marks in delimeter style."

        if input:
            return cls.dict.get("THOUSAND") * index + input
        else:
            return ""

    @classmethod
    def appendThousandMarksPlain(cls, input, index):
        "Append thousand marks in plain style."

        result = ""

        for i in input:
            result = result + cls.appendThousandMarksDelim(i, index)

        return result

    def appendThousandMarks(self, cond):
        "Append thousand marks according to chosen style (plain or delimeter)."

        method = (
            self.appendThousandMarksDelim if cond else self.appendThousandMarksPlain
        )

        for i, k in enumerate(self.groups):

            self.groups[i] = method(self.groups[i], i)

        return self

    @classmethod
    def getDigit(cls, input):
        "Get CU digit for given Arabic digit."

        return cls.dict.get(input) if input else ""

    def translateGroups(self):
        "Translate the Arabic number per group."

        for i, k in enumerate(self.groups):

            result = ""
            index = 0

            while k > 0:
                result = self.getDigit(k % 10 * pow(10, index)) + result
                index = index + 1
                k = k // 10

            self.groups[i] = result

        return self

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

    def breakIntoGroups(self):
        "Break the Arabic number into groups of 3 digits."

        while self.arabic > 0:
            self.groups.append(self.arabic % 1000)
            self.arabic = self.arabic // 1000

        return self

    def convert(self):
        "Convert the Arabic number to Cyrillic."

        return (
            self.breakIntoGroups()
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


class CyrillicNumber(AlphabeticNumberConverter):

    dict = CyrillicDictionary

    regex = "{0}*[{1}]?(?:(?:{0}*[{3}])?{4}|(?:{0}*[{2}])?(?:{0}*[{3}])?)".format(
        dict.get("THOUSAND"),
        dict.hundreds(),
        dict.tens(2),
        dict.digits(),
        dict.get(10),
    )

    def validate(self, regex):
        "Validate that input is a Cyrillic number."

        if re.fullmatch(regex, self.alphabetic):
            return self
        else:
            raise ValueError(
                "String does not match any pattern for Cyrillic numeral system number"
            )

    def __init__(self, alphabetic):
        super().__init__(alphabetic)
        self.validate("({0})+".format(self.regex))

    def prepare(self):
        "Prepare the Cyrillic number for conversion."

        if super().prepare():
            self.alphabetic = re.sub(
                "[{0}\.]".format(self.dict.get("TITLO")), "", self.alphabetic
            )  # Strip ҃"҃ " and dots
            return self

    @classmethod
    def calculateMultiplier(cls, index, input):
        "Calculate multiplier for adjusting digit group value to its registry."

        multiplier = (
            re.match("({0}*)".format(cls.dict.get("THOUSAND")), input)
            .groups()[0]
            .count(cls.dict.get("THOUSAND"))
        )  # Count trailing thousand marks in the group
        multiplier = pow(1000, multiplier if multiplier else index - 1)
        # Use thousand marks if present, otherwise use group index
        return multiplier

    def translateGroups(self):
        "Translate the alphabetic number per group."

        for i, k in enumerate(self.groups):

            multiplier = self.calculateMultiplier(i, k)
            k = re.sub(self.dict.get("THOUSAND"), "", k)  # Strip thousand marks
            self.arabic += self.translate(k) * multiplier

        return self

    def breakIntoGroups(self, regex):
        "Break the Cyrillic number in groups of 1-3 digits."

        self.groups = re.split(regex, self.alphabetic)  # Break into groups
        for i, k in enumerate(self.groups):
            self.groups.pop(i) if not k else True  # Purge empty groups
        self.groups.reverse()  # Reverse groups (to ascending order)

        return self

    def convert(self):
        "Convert the Cyrillic number to Arabic."

        return self.breakIntoGroups("({0})".format(self.regex)).translateGroups().get()


def to_alphabetic(input, flags=0):
    """
    Convert an Arabic number into Cyrillic numeral system. Uses plain style by default.

    Requires a non-zero integer.
    """

    if isinstance(input, int, "Non-zero integer required, got {0}"):
        return ArabicNumber(input, flags).convert()


to_cu = to_alphabetic


def to_arabic(input, flags=0):
    """
    Convert a Cyrillic number into Arabic numeral system.

    Requires a non-empty string.
    """

    if isinstance(input, str, "Non-empty string required, got {0}"):
        return CyrillicNumber(input).convert()


to_arab = to_arabic
