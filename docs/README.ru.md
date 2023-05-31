# Omninumeric

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/omninumeric) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/omninumeric) [![Codecov](https://img.shields.io/codecov/c/github/endrain/omninumeric)](https://app.codecov.io/gh/endrain/omninumeric)

[![PyPI - License](https://img.shields.io/pypi/l/omninumeric)](./LICENSE.ru) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🌏 [English](./README.md) Русский

Программа для чтения и записи чисел в алфавитных системах записи.

## Поддерживаемые системы записи

- [x] Церковно-славянская
- [x] Римская - числа до 3999
- [ ] Византийская греческая - в работе
- [ ] Современная греческая - в проекте
- [ ] Еврейская - в проекте

## Историческая справка

[В этой статье](./INTRODUCTION.ru.md) вы можете ознакомиться с церковнославянской системой записи чисел.

## Установка

	pip install omninumeric

## Использование

```py
#   Преобразовать арабское число в римское
#   Принимает ненулевой int, возвращает str
from omninumeric import roman

a = roman.write(1)

#   Преобразовать церковнославянское число в арабское
#   Принимает непустой str, возвращает int
from omninumeric import cyrillic

b = cyrillic.read("а҃")
```

Для систем записи чисел греческого типа, в обоих направлениях поддерживаются варианты написания "сплошной" и "по группам". "Сплошное" написание используется по умолчанию для записи.

Для записи церковно-славянских чисел доступны следующие флаги:

```py
#   DELIM устанавливает вариант записи в ЦСЯ "по группам"

c = cyrillic.write(111111, cyrillic.DELIM)

#   NOTITLO опускает вывод знака "титло"

d = cyrillic.write(11000, cyrillic.DELIM | cyrillic.NOTITLO)

#   Следующие флаги управляют декорированием точками:
#
#   ENDDOT - выводит точку в конце
#   WRAPDOT - выводит точки с обеих сторон
#   DELIMDOT - выводит точки-разделители разрядов. Устанавливает вариант записи "по группам"
#   ALLDOT - комбинация флагов WRAPDOT и DELIMDOT
```

## Принять участие

Откройте новую проблему, опишите в ней исправляемый баг или предлагаемый функционал. Затем откройте запрос на слияние, в описании дайте ссылку на проблему.

## Отзывы

Пишите по адресу: amshoor@gmail.com

## История версий

Смотрите [здесь](./CHANGELOG.ru.md).
