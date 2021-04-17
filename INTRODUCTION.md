# NUMBERS IN CHURCH SLAVONIC SCRIPT

## 1. Numerals

Church Slavonic script (*further CU*) has individual numerals to represent numbers from 1 to 9, each round ten and each round hundred, for a total of 27 numerals. There's no zero digit.

CU | Arabic | CU | Arabic | CU | Arabic
--- | --- | --- | --- | --- | ---
а҃ | 1 | і҃ | 10 | р҃ | 100
в҃ | 2 | к҃ | 20 | с҃ | 200
г҃ | 3 | л҃ | 30 | т҃ | 300
д҃ | 4 | м҃ | 40 | у҃ | 400
є҃ | 5 | н҃ | 50 | ф҃ | 500
ѕ҃ | 6 | ѯ҃ | 60 | х҃ | 600
з҃ | 7 | ѻ҃ | 70 | ѱ҃ | 700
и҃ | 8 | п҃ | 80 | ѿ҃ | 800
ѳ҃ | 9 | ч҃ | 90 | ц҃ | 900

## 2. Basic numbers

A number `x < 1000` in CU is represented by a succession of 1 to 3 CU digits that may contain a hundreds digit, a tens digit and a proper digit in that order. Digits representing numbers 11-19 are swapped places, wheter or not a hundreds digit is present.

For the purpose of this program, this is to be referenced as a "hundred group".

**Examples:**
CU | Arabic
---|---
а҃  | 1
і҃ | 10
р҃ | 100
ра҃і | 111 - note digit swapping
рк҃а | 121

## 3. Thousands
A number `x >= 1000` in CU is prepended with one or more `҂` "thousand" signs. For each "thousand" sign before a number, the number has to be mutiplied by one thousand.

## 4. Number building

Altogether, a complete number in CU consists of a succession of hundred groups with "thousand" signs inbetween.

**Examples:**
CU | Arabic
---|---
а҃ | 1
҂а҃ | 1000
҂҂а҃ | 1000000
҂҂а҂а҃а | 1001001

## 5. Decoration
Finally, there is a `҃` "titlo" superscript sign that's obligatory to CU numbers. "Titlo" is placed above the 2nd-from-last digit if it exists and is not thousand-marked, otherwise above the last digit.
    
**Examples:**

See examples above. **NB:** in some (many) fonts "titlo" appears to follow after a digit, not above it.