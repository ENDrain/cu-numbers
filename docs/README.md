# Omninumeric

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/omninumeric) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/omninumeric) [![Codecov](https://img.shields.io/codecov/c/github/endrain/omninumeric)](https://app.codecov.io/gh/endrain/omninumeric)

[![PyPI - License](https://img.shields.io/pypi/l/omninumeric)](./LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🌏 English [Русский](./README.ru.md)

Omninumeric provides support for number reading and writing in alphabetic numeral systems.

## Supported numeral systems

- [x] Cyrillic
- [x] Roman - numbers up to 3999
- [ ] Byzantian Greek - WIP
- [ ] Modern Greek - planned
- [ ] Hebrew - planned

## Background

See [Introduction](./INTRODUCTION.md) to learn about Cyrillic numeral system.

## Installation

	pip install omninumeric

## Usage

```py
#   Convert a number into Roman numeral system
#   Requires non-zero int, returns str
from omninumeric import roman

a = roman.write(1)

#   Convert a Cyrillic number to Arabic numeral system
#   Requires non-empty str, returns int
from omninumeric import cyrillic

b = cyrillic.read("а҃")
```

For Greek-type numeral systems, "Delimiter" and "plain" style numbers are supported both for reading and writing. "Plain" style is used by default for writing.

For Cyrillic numeral system, several falgs can be used for writing:

```py
#   DELIM flag sets conversion to "delimeter" style

c = cyrillic.write(111111, cyrillic.DELIM)

#   NOTITLO flag omits "titlo" decorator

d = cyrillic.write(11000, cyrillic.DELIM | cyrillic.NOTITLO)

#   Following flags control dot styling:
#
#   ENDDOT - append dot at the end
#   WRAPDOT - append dot at both ends
#   DELIMDOT - add dot separator between digit groups. Sets conversion to "delim" style
#   ALLDOT - combine WRAPDOT and DELIMDOT
```

## Contributing

Create an issue describing a bug or suggestion, then create a pull request mentioning the issue.

## Feedback

Drop me a line: amshoor@gmail.com

## Changelog

See [Changelog](./CHANGELOG.md).
