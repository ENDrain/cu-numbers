# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included with the project.

import re
from omninumeric import Dictionary, AlphabeticNumberConverter


class RomanDictionary(Dictionary):

    I = 1
    V = 5
    X = 10
    L = 50
    C = 100
    D = 500
    M = 1000


class RomanConverter(AlphabeticNumberConverter):

    _dict = RomanDictionary

    regex_a = "{0}{{0,3}}"
    regex_b = "{0}?{1}"
    regex_c = "{1}{0}{{0,3}}"
    regex_d = "{0}{2}"
    group_regex = "({0}|{1}|{2}|{3})".format(regex_a, regex_b, regex_c, regex_d)
    number_regex = "({0})?{1}?{2}?{3}?".format(
        regex_a.format(_dict.get(1000)),
        group_regex.format(_dict.get(100), _dict.get(500), _dict.get(1000)),
        group_regex.format(_dict.get(10), _dict.get(50), _dict.get(100)),
        group_regex.format(_dict.get(1), _dict.get(5), _dict.get(10)),
    )

    print(number_regex)

    def _translate(cls, alphabetic):

        total = last = 0

        for k in alphabetic:

            k = cls._dict.get(k)
            total = total + k if k <= last else total - k
            last = k

        return abs(total)

    def _translateGroups(self):

        for i, k in enumerate(self._groups):
            self._arabic += self._translate(k)

    def _breakIntoGroups(self):

        self._groups = re.split(
            self.group_regex.format(
                "(?:{0}|{1}|{2}|{3})".format(
                    self._dict.get(1),
                    self._dict.get(10),
                    self._dict.get(100),
                    self._dict.get(1000),
                ),
                "[{0}{1}{2}]".format(
                    self._dict.get(5), self._dict.get(50), self._dict.get(500)
                ),
                "[{0}{1}{2}]".format(
                    self._dict.get(10), self._dict.get(100), self._dict.get(1000)
                ),
            ),
            self._alphabetic,
        )

        for i, k in enumerate(self._groups):
            self._groups.pop(i) if not k else True  # Purge empty groups

        print(self._groups)

        return self

    def convert(self):

        return self._prepare()._validate()._breakIntoGroups()._translateGroups()._get()
