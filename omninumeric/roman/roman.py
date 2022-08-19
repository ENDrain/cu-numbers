# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included with the project.

from omninumeric import Dictionary


class RomanDictionary(Dictionary):

    I = 1
    V = 5
    X = 10
    L = 50
    C = 100
    D = 500
    M = 1000

    regex_a = "{0}{{0,3}}"
    regex_b = "{0}?{1}"
    regex_c = "{1}{0}{{0,3}}"
    regex_d = "{0}{2}"
    group_regex = "({0}|{1}|{2}|{3})".format(regex_a, regex_b, regex_c, regex_d)
    number_regex = "({0})?{1}?{2}?{3}?"

    @classmethod
    def regex(cls):
        return cls.number_regex.value.format(
            cls.regex_a.value.format(cls.get(1000)),
            cls.group_regex.value.format(cls.get(100), cls.get(500), cls.get(1000)),
            cls.group_regex.value.format(cls.get(10), cls.get(50), cls.get(100)),
            cls.group_regex.value.format(cls.get(1), cls.get(5), cls.get(10)),
        )


print(RomanDictionary.regex())
