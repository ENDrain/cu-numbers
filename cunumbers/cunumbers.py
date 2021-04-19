# For licensing information see LICENSE file included in the project's root directory.
# To learn about Cyrillic numeral system (further CU), see INTRODUCTION.md
"""
Module for number conversion between Arabic and Cyrillic numeral systems.
"""

import re

_CU_DELIM = 0x1  # Write in delim style
CU_PLAIN = 0x10  # Read/write in plain style
CU_NOTITLO = 0x100  # DO NOT append titlo
CU_ENDDOT = 0x1000  # Append dot
_CU_PREDOT = 0x10000  # Prepend dot
CU_DELIMDOT = 0x100001  # Delimeter dots (delim mode only)
CU_GREEKDOT = 0x1000000  # Greek-style dot
CU_TWODOTS = CU_ENDDOT + _CU_PREDOT  # Sandwich dots
CU_ALLDOTS = CU_ENDDOT + _CU_PREDOT + CU_DELIMDOT  # Sandwich and delimeter dots

_cu_digits = "авгдєѕзиѳ"
_cu_tens = "іклмнѯѻпч"
_cu_hundreds = "рстуфхѱѿц"
_cu_thousand = "҂"
_cu_titlo = "҃"
_cu_dot = _cu_rudot = "."
_cu_greekdot = "·"

_cu_null = "\uE000"  # A placeholder character to represent zero in CU numbers
_cu_dict = "{0}{1}{0}{2}{0}{3}".format(_cu_null, _cu_digits, _cu_tens, _cu_hundreds)

_cu_swap_regex = ["(%s)([%s])" % (_cu_tens[0], _cu_digits), "\g<2>\g<1>"]
_cu_base_regex = "[{0}]?(?:[{2}]?{3}|[{1}]?[{2}]?)".format(
    _cu_hundreds, _cu_tens[1:], _cu_digits, _cu_tens[0]
)
_cu_delim_regex = "(%s*%s)" % (_cu_thousand, _cu_base_regex)
_cu_plain_regex = "(%s+[%s]{1}|(?:%s)$)" % (
    _cu_thousand,
    _cu_dict.replace(_cu_null, ""),
    _cu_base_regex,
)


def _chflag(flags, flag):
    """Check a flag."""
    return False if flags & flag == 0 else True


def _to_cu_digit(digit=0, registry=0, multiplier=0):
    """Process an arabic digit."""

    if digit:
        return _cu_thousand * multiplier + _cu_dict[10 * registry + digit]
    else:  # Skip if @digit = 0
        return ""


def _to_cu_hundred(hundred=0, group=0, registry=0, result=""):
    """Process an arabic hundred group."""  # DELIM MODE ONLY

    if hundred:
        sub_result = _to_cu_digit(hundred % 10, registry) + result
        if hundred // 10:
            return _to_cu_hundred(hundred // 10, group, registry + 1, sub_result)
        else:
            # Swap digits in 11-19
            sub_result = re.sub(_cu_swap_regex[0], _cu_swap_regex[1], sub_result)
            return _cu_thousand * group + sub_result
    else:  # Skip if @hundred = 0
        return ""


def _to_cu_number_delim(input, group=0, result="", *, flags):
    """Process an arabic number per hundred group."""
    # @index is current hundred group

    # print("DELIM MODE")
    sub_result = (
        _to_cu_hundred(input % 1000, group) + result
    )  # Process leading hundred group
    if input // 1000:
        if _chflag(flags, CU_DELIMDOT):
            sub_result = _cu_dot + sub_result
        # Iterate over each hundred group, increasing @group index
        return _to_cu_number_delim(input // 1000, group + 1, sub_result, flags=flags)
    else:
        return sub_result


def _to_cu_number_plain(input, registry=0, result="", *, flags):
    """Process an arabic number per digit."""
    # @index is current registry

    sub_result = (
        _to_cu_digit(input % 10, registry % 3, registry // 3) + result
    )  # Process leading digit
    if input // 10:
        # Iterate over each digit, increasing @registry index
        return _to_cu_number_plain(input // 10, registry + 1, sub_result, flags=flags)
    else:
        # Swap digits in 11-19 if "і" is not "҂"-marked
        sub_result = re.sub(
            "(?<!%s)%s" % (_cu_thousand, _cu_swap_regex[0]),
            _cu_swap_regex[1],
            sub_result,
        )
        return sub_result


def _to_cu_number(input, flags=0):
    """Process an arabic number."""

    if _chflag(flags, CU_ALLDOTS):
        global _cu_dot
        if _chflag(flags, CU_GREEKDOT):
            _cu_dot = _cu_greekdot
        else:
            _cu_dot = _cu_rudot

    # Numbers up to 1000 are same in all styles, never DELIM those
    if input < 1001 or _chflag(flags, CU_PLAIN):
        sub_result = _to_cu_number_plain(input, flags=flags)
    else:
        sub_result = _to_cu_number_delim(input, flags=flags)

    if not _chflag(flags, CU_NOTITLO):
        # Calculate "titlo" position
        l = len(sub_result)
        # If 2nd-from-last symbol is a digit, place titlo next to it
        if l > 1 and sub_result[l - 2] != _cu_thousand and sub_result[l - 2] != _cu_dot:
            sub_result = sub_result[: l - 1] + _cu_titlo + sub_result[l - 1 :]
        else:
            sub_result += _cu_titlo  # Else, append to the end

    if _chflag(flags, CU_ENDDOT):
        sub_result += _cu_dot

    if _chflag(flags, _CU_PREDOT):
        sub_result = _cu_dot + sub_result

    return sub_result


def _digits_to_arab(input, group=0):
    """Process CU numerals."""
    # DELIM MODE: @group is current hundred group

    # Swap digits in numbers 11-19
    input = re.sub(_cu_swap_regex[0], _cu_swap_regex[1], input)

    subtotal = multiplier = 0
    for k in input:
        if k == _cu_thousand:
            multiplier += 1
            continue
        index = _cu_dict.index(k)  # Find current digit in dictionary
        number = index % 10  # Digit
        registry = index // 10  # Digit registry
        subtotal += number * pow(10, registry)  # Resulting number

    # Multiply result by 1000 - times "҂" marks or current group
    return subtotal * pow(1000, max(multiplier, group))


def _to_arab_number(input, flags=0):
    """Process a CU number."""

    sub_result = input
    hundreds = []

    if _chflag(flags, CU_PLAIN):
        hundreds = re.split("%s" % _cu_plain_regex, sub_result)
    else:
        hundreds = re.split("%s" % _cu_delim_regex, sub_result)

    while hundreds.count(""):  # Purge empty strs from collection
        hundreds.remove("")
    hundreds.reverse()

    result = 0
    if _chflag(flags, CU_PLAIN):
        for k in hundreds:
            result += _digits_to_arab(k)
    else:
        for i, k in enumerate(hundreds):
            result += _digits_to_arab(k, i)

    return result


def _prepare(input, flags=0):
    """Prepare a CU number for conversion."""

    input = re.sub("[%s\.]" % _cu_titlo, "", input)  # Strip ҃"҃ " and dots
    input = str.lower(str.strip(input))  # Trim and lowercase

    if re.fullmatch("%s+" % _cu_plain_regex, input):
        return _to_arab_number(input, flags=CU_PLAIN)
    elif re.fullmatch("%s+" % _cu_delim_regex, input):
        return _to_arab_number(input)
    else:
        raise ValueError(
            "String does not match any pattern for Cyrillic numeral system number"
        )


def to_cu(input, flags=0):
    """
    Convert a number into Cyrillic numeral system.

    Requires a non-zero integer.
    """

    t = type(input)
    if t != int:
        raise TypeError("Non-zero integer required, got %s" % t)
    elif input <= 0:
        raise ValueError("Non-zero integer required")
    return _to_cu_number(input, flags)


def to_arab(input, flags=0):
    """
    Convert a number into Arabic numeral system .

    Requires a non-empty string.
    """

    t = type(input)
    if t != str:
        raise TypeError("String required, got %s" % t)
    elif not input:
        raise ValueError("Non-empty string required")
    return _prepare(input)
