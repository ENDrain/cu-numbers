# cu-numbers

A program for numbers conversion between Church Slavonic script (*further CU*) and Arabic numerals.

## Background

See [Introduction](./INTRODUCTION.md) to learn about CU numbers.

## Requirements

    Python >= 3.5

## Installation

    pip install cu-numbers

## Usage

    import cunumbers

    #   Convert an Arabic number to CU
    #   Requires non-zero int, returns str

    a = cunumbers.to_cu(1)
    
    #   Convert a CU number to an Arabic
    #   Requires str, returns int

    b = cunumbers.to_arab("а҃")

"Delimiter" and "plain" styles are supported. Arabic to CU conversion mode can be specified by supplying a flag. "Delimeter" style is by default.

    #   Use CU_PLAIN or CU_DELIM to specify Arabic to CU coversion mode

    c = cunumbers.to_cu(111111, CU_PLAIN)
    
    #   Use CU_NOTITLO flag to omit "titlo"

    d = cunumbers.to_cu(11000, CU_PLAIN + CU_NOTITLO)


## Contributing

Create an issue describing a bug or suggestion, then create a pull request mentioning the issue.

## Feedback

Drop me a line: amshoor@gmail.com

## Changelog

See [Changelog](./CHANGELOG.md).

## License

See [LICENSE](./LICENSE).