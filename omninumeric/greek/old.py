# -*- coding: UTF-8 -*-
# For licensing information see LICENSE file included with the project.
"""
This module provides tools for reading and writing numbers in Old Greek numeral system.

WIP
"""

__all__ = ["ArabicNumber", "OldGreekNumber"]


from omninumeric import greek


class Dictionary(greek.Dictionary):
    "Old Greek numerals dictionary"

    α = 1
    β = 2
    γ = 3
    δ = 4
    є = 5
    ϛ = 6
    ζ = 7
    η = 8
    θ = 9
    ι = 10
    κ = 20
    λ = 30
    μ = 40
    ν = 50
    ξ = 60
    ο = 70
    π = 80
    ϟ = 90  # ϙ
    ρ = 100
    σ = 200
    τ = 300
    υ = 400
    φ = 500
    χ = 600
    ψ = 700
    ω = 800
    ϡ = 900
    THOUSAND = "͵"  # "Thousand" mark
    KERAIA = "ʹ"  # "Keraia" decorator
    OVERLINE = "̅"  # Overline decorator
    DOT = "."  # Dot decorator


class IntConverter(greek.IntConverter):
    "Number converter into Old Greek numeral system."

    def convert(self):
        """
        Convert into Old Greek numeral system. Uses plain style by default.

        Requires a non-zero integer.
        """
        return (
            self.breakIntoGroups()
            .translateGroups()
            .appendThousandMarks(self.hasFlag(self.flag.DELIM))
            .purgeEmptyGroups()
            .build()
            .get()
        )


class StrConverter(greek.StrConverter):
    "Number converter from Old Greek numeral system."

    dict = Dictionary

    def convert(self):
        """
        Convert from Old Greek numeral system.

        Requires a non-empty string.
        """

        return self.breakIntoGroups().purgeEmptyGroups().translateGroups().build().get()
