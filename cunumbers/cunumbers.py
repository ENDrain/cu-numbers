# For licensing information see LICENSE file included in the project's root directory.
"""
Module for number conversion between Church Slavonic and Arabic.
"""

import re

cu_digits = "авгдєѕзиѳ"
cu_tens = "іклмнѯѻпч"
cu_hundreds = "рстуфхѱѿц"
cu_thousand = "҂"
cu_titlo = "҃"

cu_null = "\uE000" # A placeholder character to represent zero in CU numbers
cu_dict = "{0}{1}{0}{2}{0}{3}". format(cu_null, cu_digits, cu_tens, cu_hundreds)

cu_group_regex = "({0}*[{1}]?(?:[{4}]?{3}|[{2}]?[{4}]?))". format(cu_thousand, cu_hundreds, cu_tens[1:],  cu_tens[0], cu_digits)
print(cu_group_regex)


def _to_cu_hundred(hundred = 0, group = 0):
    """Process an arabic hundred group."""

    if hundred:
        return cu_thousand * group + cu_dict[20 + hundred // 100] + cu_dict[10 + hundred % 100 // 10] + cu_dict[hundred % 10]
    else:
        return ""


def _to_cu_number(number = 0, group = 0, result = ""):
    """Process an arabic number per hundred group."""
    # @group is the current hundred group index

    # Process leading hundred
    sub_result = _to_cu_hundred(number % 1000, group) + result
    
    if number // 1000:
        # If the number is still >1000: @group++, drop last 3 digits and repeat
        return _to_cu_number(number // 1000, group + 1, sub_result) 

    else:
        # Purge zeroes
        sub_result = re.sub(cu_null, "", sub_result)

        sub_result = re.sub("(?<!%s)(%s)([%s])" % (cu_thousand, cu_tens[0], cu_digits), "\g<2>\g<1>", sub_result) # Swap digits in 11-19

        # Calculate "titlo" position

        l = len(sub_result)
        if l > 1 and sub_result[l - 2] != cu_thousand:
            sub_result = sub_result[:l - 1] + cu_titlo + sub_result[l - 1:]
        else:
            sub_result += cu_titlo 

        return sub_result   # And we're done


def _to_arab_hundred(input = "" , index = 0):
    """Process a CU hundred group."""
    # @index arg holds current position of a hundred group in the number

    # Swap digits in numbers 11-19
    input = re.sub("([%s])([%s])" % (cu_digits, cu_tens[0]), "\g<2>\g<1>", input)

    subtotal = multiplier = 0
    for k in input:
        if k == cu_thousand:
            # Set multiplier to the amount of leading "҂"
            multiplier += 1
            continue

        _index = cu_dict.index(k)
        number = _index % 10 # Digit
        registry = _index // 10 # Digit registry
        number = number * pow(10, registry) # Resulting number

        subtotal += number # Add number up to the hundred subtotal
    
    # Raise hundred subtotal to the current registry, whether it's defined by the hunred @index or "҂" marks
    subtotal *= pow(1000, max(multiplier, index))
    return subtotal


def _to_arab_number(input = ""):
    """Process a CU number per hundred group."""

    sub_result = input

    # Strip ҃"҃ "
    sub_result = re.sub("[%s]" % cu_titlo, "", input)

    # Split number by hundred and reverse (so that lower groups have lower indices)
    hundreds = re.split("%s" % (cu_group_regex), sub_result)
    while hundreds.count(""): # Purge empty strs from the hundreds collection
        hundreds.remove("")
    print(hundreds)
    hundreds.reverse()
    print(hundreds)

    result = 0
    for i, k in enumerate(hundreds):
        result += _to_arab_hundred(k, i)

    return(result)


def prepare(input):
    """Prepare a CU number for conversion."""

    input = str.lower(str.strip(input))         # Trim and lowercase
    if re.fullmatch("([%s]*[%s]{1,4})+" % (cu_thousand, cu_digits + cu_tens + cu_hundreds + cu_titlo), input) == None:
        raise ValueError("String does not match the pattern for Church Slavonic script number")
    else:
        return input



def to_cu(input):
    """
    Convert an Arabic number into Church Slavonic script.
    
    Requires a non-zero integer.
    """

    t = type(input)
    if t != int:
        raise TypeError("Non-zero integer required, got %s" % t)
    elif input <= 0:
        raise ValueError("Non-zero integer required")
    else:
        return _to_cu_number(input)    


def to_arab(input):
    """
    Convert a Church Slavonic script number into Arabic.

    Requires a string.
    """

    t = type(input)
    if t != str:
        raise TypeError("String required, got %s" % t)
    else:
        return _to_arab_number(prepare(input))


arab_to_cu = to_cu
cu_to_arab = to_arab