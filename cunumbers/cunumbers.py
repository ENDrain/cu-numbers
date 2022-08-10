# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
# To learn about Cyrillic numeral system (CU), see INTRODUCTION.md
"Module for number conversion between Arabic and Cyrillic numeral systems."

import re

CU_PLAIN = 0x1  # Write in plain style
CU_DELIM = 0x10  # Read/write in delim style
CU_NOTITLO = 0x100  # DO NOT append titlo
CU_ENDDOT = 0x1000  # Append dot
CU_PREDOT = 0x10000  # Prepend dot
CU_DOT = 0x100000  # Delimeter dots (private, for internal flag checks)
CU_DELIMDOT = CU_DOT | CU_DELIM  # Delimeter dots (forces delim style)
CU_WRAPDOT = CU_ENDDOT | CU_PREDOT  # Wrap in dots
CU_ALLDOT = CU_ENDDOT | CU_PREDOT | CU_DELIMDOT  # Wrapper and delimeter dots

cu_digits = "авгдєѕзиѳ"  # CU digit numerals
cu_tens = "іклмнѯѻпч"  # CU tens numerals
cu_hundreds = "рстуфхѱѿц"  # CU hundreds numerals
cu_thousand = "҂"  # "Thousand" mark
cu_titlo = "҃"  # "Titlo" decorator
cu_dot = "."  # Dot decorator

cu_null = "\uE000"  # Placeholder character to represent zero in CU numbers
cu_dict = "{0}{1}{0}{2}{0}{3}".format(  # CU numerals dictionary
    cu_null, cu_digits, cu_tens, cu_hundreds
)

cu_regex = "{0}*[{1}]?(?:(?:{0}*[{3}])?{4}|(?:{0}*[{2}])?(?:{0}*[{3}])?)".format(
    cu_thousand, cu_hundreds, cu_tens[1:], cu_digits, cu_tens[0]
)


class CUNumber:
    def __init__(self, input, flags=0):
        self.cu = ""
        self.arabic = input
        self.flags = flags
        self.groups = []
        self.prepare()

    def get(self):
        "Return the CU number string representation."

        return self.cu

    def prepare(self):
        "Prepare the Arabic number for conversion."

        if self.arabic <= 0:
            raise ValueError("Non-zero integer required")

    def hasFlag(self, flag):
        "Check if a flag is set."

        return False if self.flags & flag == 0 else True

    def build(self):
        "Build the CU number from digit groups."

        for k in self.groups:
            self.cu = k + self.cu
        return self

    def wrapDot(self, cond_a, cond_b):
        "Prepend and/or append dots if appropriate flags are set."

        self.cu = (cu_dot if cond_a else "") + self.cu + (cu_dot if cond_b else "")

        return self

    def delimDots(self, cond):
        "Insert dots between digit groups if appropriate flag is set."

        if cond:
            for i, k in enumerate(self.groups[1:]):
                self.groups[i + 1] = k + cu_dot

        return self

    def appendTitlo(self, cond):
        "Append titlo unless appropriate flag is set."

        if not cond:
            result = re.subn(
                "([\S]+)(?<![{0}\{1}])([\S])$".format(cu_thousand, cu_dot),
                "\g<1>{0}\g<2>".format(cu_titlo),
                self.cu,
            )
            self.cu = result[0] if result[1] > 0 else self.cu + cu_titlo

        return self

    def appendThousandMarksDelim(input, index):
        "Append thousand marks in delimeter style."

        if input:
            return cu_thousand * index + input
        else:
            return ""

    def appendThousandMarksPlain(input, index):
        "Append thousand marks in plain style."

        result = ""

        for i in input:
            result = result + CUNumber.appendThousandMarksDelim(i, index)

        return result

    def appendThousandMarks(self, cond):
        "Append thousand marks according to chosen style (plain or delimeter)."

        method = (
            CUNumber.appendThousandMarksDelim
            if cond
            else CUNumber.appendThousandMarksPlain
        )

        for i, k in enumerate(self.groups):

            self.groups[i] = method(self.groups[i], i)

        return self

    def swapDigits(self):
        "Swap digits in 11-19."

        for i, k in enumerate(self.groups):

            self.groups[i] = re.sub(
                "({0})([{1}])".format(cu_tens[0], cu_digits),
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

    def getDigit(input, index):
        "Get CU digit for given Arabic digit."

        if input:
            return cu_dict[input + 10 * index]
        else:
            return ""

    def translateGroups(self):
        "Translate the Arabic number per group."

        for i, k in enumerate(self.groups):

            result = ""
            index = 0

            while k > 0:
                result = CUNumber.getDigit(k % 10, index) + result
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


class ArabicNumber:
    def __init__(self, input):
        self.cu = input
        self.arabic = 0
        self.groups = []
        self.prepare()

    def get(self):
        "Return the Arabic number integer representation."

        return self.arabic

    def prepare(self):
        "Prepare the Cyrillic number for conversion."

        if self.cu:
            self.cu = re.sub(
                "[{0}\.]".format(cu_titlo), "", self.cu
            )  # Strip ҃"҃ " and dots
            self.cu = str.strip(self.cu)
            self.cu = str.lower(self.cu)
        else:
            raise ValueError("Non-empty string required")

    def getDigit(input):
        "Get Arabic digit for the given CU digit."

        index = cu_dict.index(input)  # Find current digit in dictionary
        number = index % 10  # Get the digit
        registry = index // 10  # Get digit registry

        return number * pow(10, registry)

    def calculateMultiplier(index, input):
        "Calculate multiplier for adjusting digit group value to its registry."

        multiplier = (
            re.match("({0}*)".format(cu_thousand), input).groups()[0].count(cu_thousand)
        )  # Count trailing thousand marks in the group
        multiplier = pow(1000, multiplier if multiplier else index - 1)
        # Use thousand marks if present, otherwise use group index
        return multiplier

    def translateGroups(self):
        "Translate the Cyrillic number per group."

        for i, k in enumerate(self.groups):

            subtotal = 0  # Current group total value

            multiplier = ArabicNumber.calculateMultiplier(i, k)
            k = re.sub(cu_thousand, "", k)  # Strip thousand marks
            for l in k:
                subtotal += ArabicNumber.getDigit(l)

            self.arabic += subtotal * multiplier

        return self

    def breakIntoGroups(self, regex):
        "Break the Cyrillic number in groups of 1-3 digits."

        self.groups = re.split(regex, self.cu)  # Break into groups
        for i, k in enumerate(self.groups):
            self.groups.pop(i) if not k else True  # Purge empty groups
        self.groups.reverse()  # Reverse groups (to ascending order)

        return self

    def validate(self, regex):
        "Validate that input is a Cyrillic number."

        if re.fullmatch(regex, self.cu):
            return self
        else:
            raise ValueError(
                "String does not match any pattern for Cyrillic numeral system number"
            )

    def convert(self):
        "Convert the Cyrillic number to Arabic."

        return (
            self.validate("({0})+".format(cu_regex))
            .breakIntoGroups("({0})".format(cu_regex))
            .translateGroups()
            .get()
        )


def isinstance(input, condition, msg):
    t = type(input)
    if t == condition:
        return True
    else:
        raise TypeError(msg.format(t))


def to_cu(input, flags=0):
    """
    Convert a number into Cyrillic numeral system. Uses plain style by default.

    Requires a non-zero integer.
    """

    if isinstance(input, int, "Non-zero integer required, got {0}"):
        return CUNumber(input, flags).convert()


def to_arab(input, flags=0):
    """
    Convert a number into Arabic numeral system.

    Requires a non-empty string.
    """

    if isinstance(input, str, "Non-empty string required, got {0}"):
        return ArabicNumber(input).convert()
