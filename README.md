# cu-numbers

A program for numbers conversion between Arabic and Cyrillic (*further CU*) numeral systems.

## Background

See [Introduction](./INTRODUCTION.md) to learn about CU numeral system.

## Requirements

	Python >= 3.5

## Installation

	pip install cu-numbers

## Usage

	import cunumbers

	#   Convert an Arabic number to CU
	#   Requires non-zero int, returns str

	a = cunumbers.to_cu(1)
	
	#   Convert a CU number to Arabic
	#   Requires str, returns int

	b = cunumbers.to_arab("а҃")

"Delimiter" and "plain" style numbers are supported in both directions. "Delimeter" style is default for CU-wise conversions.

	#   Use CU_PLAIN flag to use "plain" style in CU-wise conversion

	c = cunumbers.to_cu(111111, CU_PLAIN)
	
	#   Use CU_NOTITLO flag to omit "titlo"

	d = cunumbers.to_cu(11000, CU_PLAIN + CU_NOTITLO)

	#   Use following flags in CU-wise conversion to add dot-styling:
	#   CU_ENDDOT - append dot at the end
	#   CU_TWODOTS - append dot at both ends
	#   CU_DELIMDOT - add dot between each group in "delimeter" style.
	#       Sets conversion to "delim" style.
	#   CU_ALL_DOTS = combine CU_TWODOTS and CU_DELIMDOT
	#   CU_GREEKDOT = use "greek" style (floating) dot


## Contributing

Create an issue describing a bug or suggestion, then create a pull request mentioning the issue.

## Feedback

Drop me a line: amshoor@gmail.com

## Changelog

See [Changelog](./CHANGELOG.md).

## License

See [LICENSE](./LICENSE).
