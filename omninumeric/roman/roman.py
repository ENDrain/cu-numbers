# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included with the project.

import re, omninumeric


class Dictionary(omninumeric.Dictionary):

    I = 1
    V = 5
    X = 10
    L = 50
    C = 100
    D = 500
    M = 1000


class StrConverter(omninumeric.StrConverter):

    dict_ = Dictionary

    regex_a = "{0}{{0,3}}"
    regex_b = "{0}?{1}"
    regex_c = "{1}{0}{{0,3}}"
    regex_d = "{0}{2}"
    group_regex = "({0}|{1}|{2}|{3})".format(regex_a, regex_b, regex_c, regex_d)
    number_regex = "^({0})?{1}?{2}?{3}?$".format(
        regex_a.format(Dictionary.get(1000)),
        group_regex.format(
            Dictionary.get(100), Dictionary.get(500), Dictionary.get(1000)
        ),
        group_regex.format(Dictionary.get(10), Dictionary.get(50), Dictionary.get(100)),
        group_regex.format(Dictionary.get(1), Dictionary.get(5), Dictionary.get(10)),
    )

    def prepare(self):
        super().prepare()
        self.source = str.upper(self.source)
        return self

    def translateGroups(self):

        for i, k in enumerate(self.groups):
            total = 0
            last = 1000

            for l in k:
                l = self.dict_.get(l)
                total = total + l if l > last else total - l
                last = l

            self.groups[i] = abs(total)

        return self

    def breakIntoGroups(self):

        # print(self.source)
        self.groups = list(re.fullmatch(self.number_regex, self.source).groups())
        return self

    def convert(self):

        return (
            self.prepare()
            .validate()
            .breakIntoGroups()
            .purgeEmptyGroups()
            .translateGroups()
            .build()
            .get()
        )


def read(number, flags=0):

    return StrConverter(number, flags).convert()
