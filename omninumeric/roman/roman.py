# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.

import re, omninumeric


class Dictionary(omninumeric.Dictionary):

    I = 1
    V = 5
    X = 10
    L = 50
    C = 100
    D = 500
    M = 1000


class Const:
    THOUSAND = "̅"


def buildRegex():
    regex_a = "(?:{A}{{vinculum}}){{quantifier}}"  # I-III, X-XXX, C-CCC, M-MMM
    regex_b = "(?:{A}{{vinculum}})?{B}{{vinculum}}"  # IV-V, XL-L, CD-D
    regex_c = (
        "{B}{{vinculum}}(?:{A}{{vinculum}}){{quantifier}}"  # V-VIII, L-LXXX, D-DCCC
    )
    regex_d = "{A}{{vinculum}}{C}{{vinculum}}"  # IX, XC, CM
    group_regex = "({0}|{1}|{2}|{3})".format(regex_a, regex_b, regex_c, regex_d)

    number_regex = "({0})?{1}?{2}?{3}?".format(
        regex_a.format(A="{thousand}"),
        group_regex.format(A="{hundred}", B="{fivehundred}", C="{thousand}"),
        group_regex.format(A="{ten}", B="{fifty}", C="{hundred}"),
        group_regex.format(A="{one}", B="{five}", C="{ten}"),
    ).format(
        one=Dictionary.get(1),
        five=Dictionary.get(5),
        ten=Dictionary.get(10),
        fifty=Dictionary.get(50),
        hundred=Dictionary.get(100),
        fivehundred=Dictionary.get(500),
        thousand=Dictionary.get(1000),
        quantifier="{{0,3}}",
        vinculum="{vinculum}",
    )

    return "^{0}{1}$".format(
        number_regex.format(vinculum=Const.THOUSAND), number_regex.format(vinculum="")
    )


REGEX = buildRegex()


class IntConverter(omninumeric.IntConverter):
    def __init__(self, source, flags):
        super().__init__(source, flags, Dictionary, Const())

    def translateGroups(self):

        for i, k in enumerate(self.groups):
            if k == 0:
                result = ""
            elif k < 4:
                result = self.dict_.get(1 * pow(10, i)) * k
            elif k < 9:
                result = self.dict_.get(5 * pow(10, i))
                diff = k - 5
                if diff < 0:
                    result = "{0}{1}".format(
                        self.dict_.get(1 * pow(10, i)) * abs(diff), result
                    )
                elif diff > 0:
                    result = "{0}{1}".format(
                        result, self.dict_.get(1 * pow(10, i)) * diff
                    )
            else:
                result = "{0}{1}".format(
                    self.dict_.get(1 * pow(10, i)), self.dict_.get(1 * pow(10, i + 1))
                )

            self.groups[i] = result

        return self

    def breakIntoGroups(self):

        while self.source > 0:
            self.groups.append(self.source % 10)
            self.source = self.source // 10

        return self

    def convert(self):
        return self.breakIntoGroups().purgeEmptyGroups().translateGroups().build().get()


class StrConverter(omninumeric.StrConverter):
    def __init__(self, source, flags):
        super().__init__(source, flags, Dictionary, Const())

    def prepare(self):
        super().prepare()
        self.source = str.upper(self.source)
        return self

    def translateGroups(self):

        for i, k in enumerate(self.groups):
            total = 0
            last = 1000
            multiplier = pow(1000, 1 if k.find(self.const.THOUSAND) > -1 else 0)
            k = re.sub(self.const.THOUSAND, "", k)

            for l in k:
                l = self.dict_.get(l)
                total = total + l if l > last else total - l
                last = l

            self.groups[i] = abs(total) * multiplier

        return self

    def breakIntoGroups(self):

        # print(self.source)
        self.groups = list(re.fullmatch(REGEX, self.source).groups())
        return self

    def convert(self):

        return (
            self.prepare()
            .breakIntoGroups()
            .purgeEmptyGroups()
            .translateGroups()
            .build()
            .get()
        )


def write(number, flags=0):

    return IntConverter(number, flags).convert()


def read(number, flags=0):

    return StrConverter(number, flags).convert()
