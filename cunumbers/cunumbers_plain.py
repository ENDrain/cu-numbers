def _arab_to_cu_digit_plain(digit = 0, registry = 0, multiplier = 0):
    """
    Convert Arabic digit into Church Slavonic script.
    PLAIN MODE
    """

    if digit:
        return cu_thousand * multiplier + cu_dict[10 * registry + digit]


def _arab_to_cu_plain(input = 0, registry = 0, result = ""):
    """
    Convert Arabic number into Church Slavonic script.
    PLAIN MODE
    """

    result += _cu_to_arab_digit(input % 10, registry % 3, registry // 3)

    if input // 10:
        return _cu_to_arab(input // 10, registry + 1, result)

    else:
        l = len(result)
        if result[l - 2] != cu_thousand:
            result = result[:l - 2] + cu_titlo + result[l - 2:]
        else:
            result += cu_titlo
        
        return result


def _cu_to_arab_digit_plain(input = ""):   
    """
    Convert Church Slavonic script digit into Arabic.
    PLAIN MODE
    """

    multiplier = 0
    while input[0] == cu_thousand:
        multiplier += 1
        input = input[1:]

    index = cu_dict.index(input)
    digit = index % 10
    registry = index // 10
    return digit * pow(10, registry) * pow(1000, multiplier)


def _cu_to_arab_plain(input = "")
    """
    Convert Church Slavonic script number into Arabic.
    PLAIN MODE
    """

    Strip ҃"҃ "
    sub_result = re.sub("%s" % cu_titlo, "", input)

    hundreds = re.split("(%s*[%s]\{1\})" % (cu_thousand, cu_digits + cu_tens + cu_hundreds), sub_result).reverse()

    while hundreds.count(""): # Purge empty strs from the hundreds collection
        hundreds.remove("")

    result = 0
    for i, k in enumerate(hundreds):
        result += _cu_to_arab_digit_plain(k)

    return result
