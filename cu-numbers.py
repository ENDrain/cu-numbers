# ABOUT CHURCH SLAVONIC NUMBERS
#
# Church Slavonic (CS) script has individual digits to represent numbers from 1 to 9,
# each round ten and each round hundred, for a total of 27 digits. There's no zero digit.
#
# A number x < 1000 in CS script is represented by a succession of 1 to 3 CS digits
# that may contain a hundreds digit, a tens digit and a proper digit in that order.
# Digits representing numbers 11-19 are swapped places, wheter or not a hundreds digit is present.
# 
# For the purpose of this program, this is to be referenced as "a hundred group".
#
# Examples:
# а҃ = 1
# і҃ = 10
# р҃ = 100
# ра҃і = 111 - note the digit swapping
# рк҃а = 121
#
# A number x >= 1000 in CS script is prepended with a "thousand" sign.
# For each "thousand" sign before a number, the number has to be mutiplied by a thousand.
#
# Altogether, a complete number in CS script consists of a succession of hundred groups
# with "thousand" signs inbetween.
#
# Examples:
# а҃ = 1
# ҂а҃ = 1000
# ҂҂а҃ = 1000000
# ҂҂а҂аа҃ = 1001001
#
# There's also a "titlo" superscript sign that's obligatory to Church Slavonic numbers.
# "Titlo" is placed in the number's rightmost hundred group;
# above the 2nd-from-last digit if it exists, otherwise above the only digit.
# See examples above.


import re

cu_digits = "авгдєѕзиѳ"
cu_tens = "іклмнѯѻпч"
cu_hundreds = "рстуфхѱѡц"
cu_thousand = "҂"
cu_titlo = "҃"

cu_null = "\uE000" # A placeholder character to represent zero in CU numbers
cu_dict = cu_null + cu_digits + cu_null + cu_tens + cu_null + cu_hundreds


# Process an arabic hundred group
def _write_cu_hundred(hundred):
    return cu_dict[20 + hundred // 100] + cu_dict[10 + hundred % 100 // 10] + cu_dict[hundred % 10]


# Process an arabic number in hundred groups
def _write_cu_number(index, number, result):
    # @index arg counts the amount of hundred groups in a number
    # to add the appropriate amount of the "҂" between each hundred group.

    # Process leading hundred. Prepend with "҂" times @index if @index > 0
    sub_result = cu_thousand * index + _write_cu_hundred(number % 1000) + result
    
    if number // 1000:
        # If the number is still >1000: @index++, drop last 3 digits and repeat
        return _write_cu_number(index + 1, number // 1000, sub_result) 

    else:
        # Purge zero-groups and individual zeroes
        sub_result = re.sub("(%s*%s{3})|(%s){1}" % (cu_thousand, cu_null, cu_null), "", sub_result)

        # Calculate "titlo" position. Get leftmost hundred group
        end = re.search("([%s]?[%s]?[%s]?$)" % (cu_hundreds, cu_tens, cu_digits), sub_result).group(0)
        # If leftmost hundred group is 1 digit, append "titlo" at the end. Else, append at the 2nd-from-last position.
        sub_result = sub_result + cu_titlo if len(end) == 1 else sub_result[:-1] + cu_titlo + sub_result[-1:] 

        sub_result = re.sub("(і)(%s)?([%s])" % (cu_titlo, cu_digits), "\g<3>\g<2>\g<1>", sub_result) # Swap digits in 11-19

        return sub_result   # And we're done


def _read_cu_hundred(index, input):
    # @index arg holds current position of a hundred group in the number

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


# Process a Church Slavonic number
def _read_cu_number(input):
    sub_result = str.strip(input)

    # Strip ҃"҃ " and "҂"
    sub_result = re.sub("[%s]" % cu_titlo, "", sub_result)
    # Swap digits in numbers 11-19
    sub_result = re.sub("([%s])([%s])" % (cu_digits, cu_dict[11]), "\g<2>\g<1>", sub_result)

    result = 0
    # Split number by hundred
    # It's important to split a number bottom-up, so that lower hundreds have lower indices
    hundreds = re.split("([%s]?[%s]?[%s]?[%s]*)" % (cu_digits, cu_tens, cu_hundreds, cu_thousand), sub_result[::-1])

    while hundreds.count(""): # Purge empty strs from the hundreds collection (it's a re.split() feature)
        hundreds.remove("")

    for i, k in enumerate(hundreds):
        result += _read_cu_hundred(i, k[::-1])

    return(result)