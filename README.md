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

    a = cunumbers.arab_to_cu(1)
    
    #   Convert a CU number to an Arabic
    #   Requires str, returns int

    b = cunumbers.cu_to_arab("а҃")

## Contributing

Create an issue describing a bug or suggestion, then create a pull request mentioning the issue.

## Feedback

Drop me a line: amshoor@gmail.com

## Changelog

See [Changelog](./CHANGELOG.md).

## License

See [LICENSE](./LICENSE).