# Omninumeric

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/omninumeric) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/omninumeric) [![Codecov](https://img.shields.io/codecov/c/github/endrain/omninumeric)](https://app.codecov.io/gh/endrain/omninumeric)

[![PyPI - License](https://img.shields.io/pypi/l/omninumeric)](./LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🌏 English [Русский](./README.ru.md)

Omninumeric provides support for number reading and writing in alphabetic numeral systems.

## Supported numeral systems

- [x] Cyrillic
- [ ] Roman - WIP
- [ ] Byzantian Greek - WIP
- [ ] Modern Greek - planned
- [ ] Hebrew - planned

## Background

See [Introduction](./INTRODUCTION.md) to learn about Cyrillic numeral system.

## Installation

	pip install omninumeric

## Usage

	import omninumeric.cyrillic as CU

	#   Convert a number into Cyrillic
	#   Requires non-zero int, returns str

	a = CU.ArabicNumber(1).convert()
	
	#   Convert a Cyrillic number to Arabic
	#   Requires non-empty str, returns int

	b = CU.CyrillicNumber("а҃").convert()

"Delimiter" and "plain" style numbers are supported both for reading and writing, "plain" style is used by default for writing.

When writing into Cyrillic, several falgs can be used:

	#   CU_DELIM flag sets conversion to "delimeter" style

	c = cu.to_alphabetic(111111, CU_DELIM)
	
	#   CU_NOTITLO flag omits "titlo" decorator

	d = cu.to_alphabetic(11000, CU_DELIM | CU_NOTITLO)

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
