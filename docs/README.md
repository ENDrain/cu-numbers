# cu-numbers

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cu-numbers) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/cu-numbers) [![Codecov](https://img.shields.io/codecov/c/github/endrain/cu-numbers)](https://app.codecov.io/gh/endrain/cu-numbers)

[![PyPI - License](https://img.shields.io/pypi/l/cu-numbers)](./LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🌏 English [Русский](./README.ru.md)

A program for numbers conversion between Arabic and Cyrillic (*further CU*) numeral systems.

## Background

See [Introduction](./INTRODUCTION.md) to learn about CU numeral system.

## Installation

	pip install cu-numbers

## Usage

	import cunumbers.cunumbers as cu

	#   Convert an Arabic number to CU
	#   Requires non-zero int, returns str

	a = cu.to_cu(1)
	
	#   Convert a CU number to Arabic
	#   Requires non-empty str, returns int

	b = cu.to_arab("а҃")

"Delimiter" and "plain" style numbers are supported in both directions. "Delimeter" style is default for CU-wise conversion.

Several falgs can be used with `to_cu()` method:

	#   CU_PLAIN flag sets conversion to "plain" style

	c = cu.to_cu(111111, CU_PLAIN)
	
	#   CU_NOTITLO flag omits "titlo" output

	d = cu.to_cu(11000, CU_PLAIN | CU_NOTITLO)

	#   Following flags control dot styling:
	#
	#   CU_ENDDOT - append dot at the end
	#   CU_WRAPDOT - append dot at both ends
	#   CU_DELIMDOT - add dot separator between digit groups. Sets conversion to "delim" style
	#   CU_ALLDOT - combine CU_WRAPDOT and CU_DELIMDOT


## Contributing

Create an issue describing a bug or suggestion, then create a pull request mentioning the issue.

## Feedback

Drop me a line: amshoor@gmail.com

## Changelog

See [Changelog](./CHANGELOG.md).
