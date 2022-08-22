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


class Const:
    regex_a = "{0}{{0,3}}"
    regex_b = "{0}?{1}"
    regex_c = "{1}{0}{{0,3}}"
    regex_d = "{0}{2}"
    group_regex = "({0}|{1}|{2}|{3})".format(regex_a, regex_b, regex_c, regex_d)
    number_regex = "({0})?{1}?{2}?{3}?".format(
        regex_a.format(Dictionary.get(1000)),
        group_regex.format(
            Dictionary.get(100), Dictionary.get(500), Dictionary.get(1000)
        ),
        group_regex.format(Dictionary.get(10), Dictionary.get(50), Dictionary.get(100)),
        group_regex.format(Dictionary.get(1), Dictionary.get(5), Dictionary.get(10)),
    )


class StrConverter(omninumeric.StrConverter):

    dict = Dictionary
    const = Const

    def translateGroups(self):

        for i, k in enumerate(self.groups):

            total = last = 0

            for l in k:

                l = cls.dict_.get(k)
                total = total + l if l <= last else total - l
                last = l

            self.groups[i] = total

    def breakIntoGroups(self):

        self.groups = re.split(
            self.const.group_regex.format(
                "(?:{0}|{1}|{2}|{3})".format(
                    self.dict_.get(1),
                    self.dict_.get(10),
                    self.dict_.get(100),
                    self.dict_.get(1000),
                ),
                "[{0}{1}{2}]".format(
                    self.dict_.get(5), self.dict_.get(50), self.dict_.get(500)
                ),
                "[{0}{1}{2}]".format(
                    self.dict_.get(10), self.dict_.get(100), self.dict_.get(1000)
                ),
            ),
            self.source,
        )

        for i, k in enumerate(self.groups):
            self.groups.pop(i) if not k else True  # Purge empty groups

        print(self.groups)

        return self

    def convert(self):

        return self.prepare().validate().breakIntoGroups().translateGroups().get()
