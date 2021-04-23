# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
# To learn about Cyrillic numeral system (further CU), see INTRODUCTION.md
"Module for number conversion between Arabic and Cyrillic numeral systems."

import re

CU_DELIM = 0x1  # Write in delim style
CU_PLAIN = 0x10  # Read/write in plain style
CU_NOTITLO = 0x100  # DO NOT append titlo
CU_ENDDOT = 0x1000  # Append dot
CU_PREDOT = 0x10000  # Prepend dot
CU_DELIMDOT = 0x100000 | CU_DELIM  # Delimeter dots (delim mode only)
CU_WRAPDOT = CU_ENDDOT | CU_PREDOT  # Wrap in dots
CU_ALLDOT = CU_ENDDOT | CU_PREDOT | CU_DELIMDOT  # Wrapper and delimeter dots

cu_digits = "авгдєѕзиѳ"  # CU digit numerals
cu_tens = "іклмнѯѻпч"  # CU tens numerals
cu_hundreds = "рстуфхѱѿц"  # CU hundreds numerals
cu_thousand = "҂"  # "Thousand" mark
cu_titlo = "҃"  # "Titlo" decorator
cu_dot = "."  # Dot decorator

cu_null = "\uE000"  # A placeholder character to represent zero in CU numbers
cu_dict = "{0}{1}{0}{2}{0}{3}".format(  # CU numerals dictionary
    cu_null, cu_digits, cu_tens, cu_hundreds
)

cu_group_regex = (  # Regex for a basic CU number x < 1000
    "[{0}]?(?:[{2}]?{3}|[{1}]?[{2}]?)".format(
        cu_hundreds, cu_tens[1:], cu_digits, cu_tens[0]
    )
)
cu_delim_regex = "({0}*{1})".format(  # Regex for a digit group in "delim" style
    cu_thousand, cu_group_regex
)
cu_plain_regex = (  # Regex for a single digit in "plain" style
    "({0}+[{1}]{2}|(?:{3})$)".format(
        cu_thousand,
        cu_dict.replace(cu_null, ""),
        "{1}",
        cu_group_regex,
    )
)


class CUNumber:
    def __init__(self, input, flags=0):
        self.cu = None
        self.arabic = input
        self.flags = flags

    def get(self):
        return self.cu

    def hasFlag(self, flag):
        """Check a flag."""

        return False if self.flags & flag == 0 else True

    def stripDelimDots(self):
        "Strip delimeter dots unless CU_DELIMDOT is set."

        if not self.hasFlag(CU_DELIMDOT):
            self.cu = re.sub(
                "(\{0}(?!{1}$)|(?<!{2}[{3}])\{0}(?={1}$))".format(
                    cu_dot, cu_tens[0], cu_thousand, cu_digits
                ),
                "",
                self.cu,
            )
        return self

    def stripAheadDot(self):
        "Strip ahead dot."

        self.cu = re.sub("^\.([\S]*)", "\g<1>", self.cu)
        return self

    def prependDot(self):
        "Prepend dot if CU_PREDOT is set."

        if self.hasFlag(CU_PREDOT):
            self.cu = re.sub("^[^\.][\S]*", ".\g<0>", self.cu)
            return self
        else:
            return self.stripAheadDot()

    def appendDot(self):
        "Append dot if CU_ENDDOT is set."

        if self.hasFlag(CU_ENDDOT):
            self.cu = re.sub("[\S]*[^\.]$", "\g<0>.", self.cu)
        return self

    def appendTitlo(self):
        """Append "titlo" unless CU_NOTITLO is set."""

        if not self.hasFlag(CU_NOTITLO):
            result = re.subn(
                "([\S]+)(?<![{0}\{1}])([\S])$".format(cu_thousand, cu_dot),
                "\g<1>{0}\g<2>".format(cu_titlo),
                self.cu,
            )
            self.cu = result[0] if result[1] > 0 else self.cu + cu_titlo
        return self

    def swapDigits(input):
        """Swap digits in 11-19 unless "і" is "thousand"-marked."""

        result = re.sub(
            "(?<!{0})({1})([{2}])".format(cu_thousand, cu_tens[0], cu_digits),
            "\g<2>\g<1>",
            input,
        )
        return result

    def processDigit(input, registry=0, multiplier=0):
        "Convert the Arabic digit to a CU numeral."

        return (
            cu_thousand * multiplier + cu_dict[10 * registry + input] if input else ""
        )

    def _processNumberPlain(input, registry=0, result=""):
        "Process the Arabic number per digit."
        # @registry is current registry

        if input:
            result = (
                CUNumber.processDigit(input % 10, registry % 3, registry // 3) + result
            )
            return CUNumber._processNumberPlain(input // 10, registry + 1, result)
        else:
            return CUNumber.swapDigits(result)

    def processGroup(input, group=0):
        "Process the group of 3 Arabic digits."

        input = input % 1000
        return (
            (cu_dot + cu_thousand * group + CUNumber._processNumberPlain(input))
            if input
            else ""
        )

    def _processNumberDelim(input, group=0, result=""):
        "Process the Arabic number per groups of 3 digits."
        # @index is current group of digits number (i.e. amount of multiplications of thousand)

        if input:
            result = CUNumber.processGroup(input, group) + result
            return CUNumber._processNumberDelim(input // 1000, group + 1, result)
        else:
            return result

    def processNumberPlain(self):

        self.cu = CUNumber._processNumberPlain(self.arabic)
        return self

    def processNumberDelim(self):

        self.cu = CUNumber._processNumberDelim(self.arabic)
        return self

    def convert(self):
        "Convert the Arabic number to CU."

        if self.arabic <= 0:
            return self
        elif self.arabic < 1001 or self.hasFlag(CU_PLAIN):
            self.processNumberPlain()
        else:
            self.processNumberDelim()
        return self.stripDelimDots().prependDot().appendDot().appendTitlo()


class ArabicNumber:
    def __init__(self, input):
        self.cu = input
        self.arabic = None
        self.prepare()

    def get(self):
        return self.arabic

    def prepare(self):
        "Prepare the CU number for conversion."

        self.cu = re.sub(
            "[{0}\.]".format(cu_titlo), "", self.cu
        )  # Strip ҃"҃ " and dots
        self.cu = str.strip(self.cu)
        self.cu = str.lower(self.cu)

    def processDigit(input, registry=0):
        "Convert the CU numeral to an arabic digit."
        print(input)
        index = cu_dict.index(input)  # Find current digit in dictionary
        number = index % 10  # Digit
        registry = index // 10  # Digit registry
        return number * pow(10, registry)  # Resulting number

    def processGroup(input, group=0):
        "Process the group of CU numerals."

        subtotal = multiplier = 0
        for k in input:
            if k == cu_thousand:
                multiplier += 1
                continue
            subtotal += ArabicNumber.processDigit(k)

        # Multiply result by 1000 - times "҂" marks or current group
        return subtotal * pow(1000, max(multiplier, group))

    def prepareGroups(input, regex):
        "Prepare CU digit groups for conversion."

        groups = re.split(regex, input)

        while groups.count(""):  # Purge empty strs from collection
            groups.remove("")
        groups.reverse()
        return groups

    def _processNumberPlain(input):
        "Process the CU number per digit."

        groups = ArabicNumber.prepareGroups(input, cu_plain_regex)

        result = 0
        for k in groups:
            result += ArabicNumber.processGroup(k)
        return result

    def _processNumberDelim(input):
        "Process the CU number per groups of 1-3 digits."

        groups = ArabicNumber.prepareGroups(input, cu_delim_regex)

        result = 0
        for i, k in enumerate(groups):
            result += ArabicNumber.processGroup(k, i)
        return result

    def processNumberPlain(self):
        self.arabic = ArabicNumber._processNumberPlain(self.cu)
        return self

    def processNumberDelim(self):
        self.arabic = ArabicNumber._processNumberDelim(self.cu)
        return self

    def convert(self):
        "Choose the CU number to Arabic."

        if not self.cu:
            return self
        if re.fullmatch("{0}+".format(cu_plain_regex), self.cu):
            return self.processNumberPlain()
        elif re.fullmatch("{0}+".format(cu_delim_regex), self.cu):
            return self.processNumberDelim()
        else:
            return self


def to_cu(input, flags=0):
    """
    Convert a number into Cyrillic numeral system.

    Requires a non-zero integer.
    """

    if isinstance(input, int):
        return CUNumber(input, flags).convert().get()
    return None


def to_arab(input, flags=0):
    """
    Convert a number into Arabic numeral system .

    Requires a non-empty string.
    """

    if isinstance(input, str):
        return ArabicNumber(input).convert().get()
    return None
