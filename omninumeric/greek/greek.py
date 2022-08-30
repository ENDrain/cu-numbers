# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included in the project's root directory.
"This module provides basic tools for reading and writing numbers in Greek-type alphabetic numeral systems."

import re, omninumeric


PLAIN = 0  # Write in plain style flag
DELIM = 0b1  # Read/write in delim style flag


class Dictionary(omninumeric.Dictionary):
    """
    ABC for Greek-type alphabetic numeral systems ditcionaries.

    Derive from this class to define numeral dictionaries for Greek type alphabetic numeral systems.
    """

    @classmethod
    def getmany(cls, start=1, end=10, step=1):
        """
        Look a range of numerals up in dictionary.

        @start - starting numeral value (i.e. 5 for range of 5, 6, 7...)
        @end - ending numeral value (i.e. 5 for range of ...3, 4, 5)
        step - numeral value increment (i.e. 1 for range of 1, 2, 3...; 10 for range of 10, 20, 30...)
        """

        r = ""
        for i in range(start * step, (end + 1) * step, step):
            r += cls(i).name
        return r

    @classmethod
    def digits(cls, start=1, end=9):
        """
        Get a range of numerals in digits registry.

        @start - starting numeral value (i.e. 5 for range of 5, 6, 7...)
        @end - ending numeral value (i.e. 5 for range of ...3, 4, 5)
        """
        return cls.getmany(start, end, 1)

    @classmethod
    def tens(cls, start=1, end=9):
        """
        Get a range of numerals in tens registry.

        @start - starting numeral value (i.e. 5 for range of 50, 60, 70...)
        @end - ending numeral value (i.e. 5 for range of ...30, 40, 50)
        """
        return cls.getmany(start, end, 10)

    @classmethod
    def hundreds(cls, start=1, end=9):
        """
        Get a range of numerals in hundreds registry.

        @start - starting numeral value (i.e. 5 for range of 500, 600, 700...)
        @end - ending numeral value (i.e. 5 for range of ...300, 400, 500)
        """
        return cls.getmany(start, end, 100)


class IntConverter(omninumeric.IntConverter):
    """
    ABC for number conversion into Greek-type alphabetic numeral systems.

    Derive from this class to define converters into Greek-type alphabetic numeral systems.
    """

    def appendThousandMarks(self, cond, thousand):
        "Append thousand marks according to chosen style (plain or delimeter)."

        for i, k in enumerate(self.groups):
            if k:
                if self.hasFlag(cond):
                    result = "{0}{1}".format(thousand * i, k)

                else:
                    result = ""

                    for l in k:
                        result = "{0}{1}{2}".format(result, thousand * i, l)

                self.groups[i] = result

        return self

    def translateGroups(self):
        "Translate groups of numerals one by one."

        for i, k in enumerate(self.groups):
            result = ""
            registry = 0

            while k > 0:
                result = "{0}{1}".format(
                    self.getNumeral(k % 10 * pow(10, registry)), result
                )
                registry = registry + 1
                k = k // 10

            self.groups[i] = result

        return self

    def breakIntoGroups(self):
        "Break source number into groups of 3 numerals."

        while self.source > 0:
            self.groups.append(self.source % 1000)
            self.source = self.source // 1000

        return self


class StrConverter(omninumeric.StrConverter):
    """
    ABC for number conversion from Greek-type alphabetic numeral systems.

    Derive from this class to define converters from Greek-type alphabetic numeral systems.
    """

    def prepare(self):

        super().prepare()
        self.source = str.lower(self.source)
        return self

    @classmethod
    def calculateMultiplier(cls, index, group, thousand):
        'Calculate multiplier for a numerals group, according to group index or "thousand" marks present in the group.'

        multiplier = (
            re.match("({0}*)".format(thousand), group).groups()[0].count(thousand)
        )  # Count trailing thousand marks in the group
        multiplier = pow(1000, multiplier if multiplier else index)
        # Use thousand marks if present, otherwise use group index
        return multiplier

    def translateGroups(self, thousand):
        "Translate groups of numerals one by one."

        for i, k in enumerate(self.groups):
            total = 0  # Current group total value
            multiplier = self.calculateMultiplier(i, k)
            k = re.sub(thousand, "", k)  # Strip thousand marks

            for l in k:
                total += self.getNumeral(l)

            self.groups[i] = total * multiplier

        return self

    def breakIntoGroups(self, regex=""):
        "Break source number in groups of 1-3 numerals."

        self.groups = re.split(regex, self.source)  # Break into groups
        self.groups.reverse()  # Reverse groups (to ascending order)

        return self
