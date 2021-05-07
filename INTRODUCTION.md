# CYRILLIC NUMERAL SYSTEM

## 1. Numerals
Cyrillic numeral system has individual letters assigned to represent numbers from 1 to 9 in registries from digits to hundreds, for a total of 27 numerals. There's no zero numeral.

Cyrillic|Arabic|Cyrillic|Arabic|Cyrillic|Arabic
---|---|---|---|---|---
а҃|1|і҃|10|р҃|100
в҃|2|к҃|20|с҃|200
г҃|3|л҃|30|т҃|300
д҃|4|м҃|40|у҃|400
є҃|5|н҃|50|ф҃|500
ѕ҃|6|ѯ҃|60|х҃|600
з҃|7|ѻ҃|70|ѱ҃|700
и҃|8|п҃|80|ѿ҃|800
ѳ҃|9|ч҃|90|ц҃|900

## 2. Basic numbers
A number `x < 1000` is represented by appropriate Cyrillic registry numerals in descending registry order, except for numbers 11-19, where numerals are swapped.

**Examples:**
Cyrillic|Arabic|Cyrillic|Arabic|Cyrillic|Arabic
---|---|---|---|---|---
а҃|1|і҃|10|р҃|100
|||||р҃а|101
|||||р҃і|110
|||а҃і|11|ра҃і|111
|||к҃а|21|рк҃а|121

## 3. Thousands and above
In a number `x > 999`, the `҂` "thousand" sign is used before numerals that represent higher order of magnitude. For each thousand sign before a numeral its value is multiplied by 1000.

**Examples:**
Cyrillic|Arabic
---|---
҂а҃|1 000
҂і҃|10 000
҂р҃|100 000
҂҂а҃|1 000 000

## 4. Number building: various styles
There are various styles of building Cyrillic numbers with values `x > 999`.

## 4.1. "Plain" style
In "plain" style, "thousand" signs are prepended to each numeral in higher registries, so that only the numeral following is multiplied.

In this style, numerals representing numbers 11-19 are only swapped unless "thousand"-marked.

***Examples:**
Cyrillic|Arabic
---|---
҂р҂і҂ара҃і|111 111

## 4.2 "Delimeter" style
In "delimeter" style, "thousand" signs are prepended to each group of numerals that form a basic number, so that the whole basic number following is multiplied.

Unlike in "plain", in this style numerals representing numbers 11-19 are swapped on each occurrence.

**Examples:**
Cyrillic|Arabic
---|---
҂раіра҃і|111 111

## 4.3 "Circled" style
In "circled" style, a special set of encircling markers is used to denote each higher order of magnitude from ten thousands up to billions.

**Examples:**
Cyrillic|Arabic
---|---
а&#1160;а&#8413;҂ара҃і|111 111

## 5. Decoration

## 5.1 "Titlo"
The `҃`&nbsp; "titlo" superscript sign is obligatory to Cyrillic numbers. "Titlo" is placed above the 2nd-from-last digit if it exists and is not thousand-marked, otherwise above the last digit.

Historically, "titlo" could've been placed above the 2nd digit, or above the whole number. It is possible to reproduce this with Unicode symbols "Titlo start", "titlo section", "titlo end".

## 5.2 Dots
	
Cyrillic numbers may be decorated with dots. A dot may be appended at the end or at both sides of a number. Dots also may be used as additional delimeters. It is necessary to do so in some cases to avoid ambiguity:

||Cyrillic|Arabic
|---|---|---
|"Plain" style:|҂і҂а҃|11000
|"Delim" style:|҂а҃і|11000
||҂а.і҃|1010
