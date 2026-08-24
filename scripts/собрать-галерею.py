#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Переписывает палитру одностраничной галереи из tokens.css.

Галерея `дизайн-система.html` существует ради одного случая: показать систему
там, где сборки ещё нет — до прототипа, в переписке, ссылкой. Всё остальное
время правда живёт в `presets/core-vue/features/SystemView.vue`, потому что та
галерея рисует **настоящие компоненты кита** и соврать о системе не может.

Проблема копии в том, что она расходится с оригиналом молча. Поэтому палитра
в HTML не пишется руками: этот скрипт читает `light-dark()` из tokens.css и
перекладывает пары в три блока голого CSS — светлый, `prefers-color-scheme`
и `[data-theme=dark]`.

    python3 scripts/собрать-галерею.py           # переписать
    python3 scripts/собрать-галерею.py --проверить # только сверить, код 1 при расхождении

Ненулевой код возврата означает: галерея отстала от токенов.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS = ROOT / 'presets' / 'core-vue' / 'design' / 'tokens.css'
PAGE = ROOT / 'scripts' / 'дизайн-система.html'
BEGIN, END = '/*ПАЛИТРА-НАЧАЛО*/', '/*ПАЛИТРА-КОНЕЦ*/'

# Что галерея показывает. Имя слева — как в голом CSS, справа — токен палитры.
USED = [
    ('canvas', 'canvas'), ('rail', 'rail'), ('raised', 'raised'),
    ('surface', 'surface'), ('surface-2', 'surface-2'),
    ('line', 'line'), ('line-strong', 'line-strong'), ('line-control', 'line-control'),
    ('text', 'text'), ('text-soft', 'text-soft'), ('muted', 'muted'), ('strong', 'strong'),
    ('inverse', 'inverse'), ('on-inverse', 'on-inverse'), ('on-inverse-soft', 'on-inverse-soft'),
    ('accent', 'accent'), ('accent-hover', 'accent-hover'), ('on-solid', 'on-solid'),
    ('accent-quiet', 'accent-quiet'), ('accent-soft', 'accent-soft'), ('accent-line', 'accent-line'),
    ('danger', 'danger'), ('danger-soft', 'danger-soft'), ('on-danger-soft', 'on-danger-soft'),
    ('warning', 'warning'), ('warning-soft', 'warning-soft'), ('on-warning-soft', 'on-warning-soft'),
    ('focus', 'focus'),
    ('shade-xs', 'shade-xs'), ('shade-sm', 'shade-sm'), ('shade-sm2', 'shade-sm2'),
    ('shade-md', 'shade-md'), ('shade-md2', 'shade-md2'),
]


def pairs():
    """--p-имя: light-dark(светлое, тёмное) → {имя: (светлое, тёмное)}

    Запятая внутри `rgba(…)` — не разделитель аргументов. Первая версия
    делила по первой запятой регулярным выражением и получала
    `rgba(238` вместо `rgba(238, 244, 242, 0.72)`: галерея собиралась из
    обрубков и молча ломала половину палитры. Поэтому разбор идёт по
    глубине скобок, а не по знаку.
    """
    src = TOKENS.read_text(encoding='utf-8')
    out = {}
    for m in re.finditer(r'--p-([a-z0-9-]+)\s*:\s*light-dark\(', src):
        name, i, depth = m.group(1), m.end(), 1
        start, comma = i, None
        while i < len(src) and depth:
            ch = src[i]
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if not depth:
                    break
            elif ch == ',' and depth == 1 and comma is None:
                comma = i
            i += 1
        if comma is None:
            sys.exit('--p-%s: у light-dark() нет второго аргумента' % name)
        out[name] = (src[start:comma].strip(), src[comma + 1:i].strip())
    return out


def block(found, dark, indent):
    rows, line = [], indent
    for css, token in USED:
        if token not in found:
            sys.exit('в tokens.css нет --p-%s — галерея просит токен, которого нет' % token)
        piece = '--%s: %s;' % (css, found[token][1 if dark else 0])
        if len(line) + len(piece) > 108:
            rows.append(line.rstrip()); line = indent
        line += piece + ' '
    rows.append(line.rstrip())
    return '\n'.join(rows)


def build(found):
    return '\n'.join([
        BEGIN,
        '  /* Палитра переписана из tokens.css скриптом собрать-галерею.py.',
        '     Руками не править: правка потеряется при следующем прогоне, а до',
        '     тех пор галерея будет показывать не ту систему, что в коде. */',
        '  :root {',
        '    color-scheme: light dark;',
        block(found, False, '    '),
        '  }',
        '  @media (prefers-color-scheme: dark) {',
        '    :root:not([data-theme=light]) {',
        block(found, True, '      '),
        '    }',
        '  }',
        '  :root[data-theme=dark] {',
        block(found, True, '    '),
        '  }',
        '  ' + END,
    ])


def main():
    check = '--проверить' in sys.argv or '--check' in sys.argv
    page = PAGE.read_text(encoding='utf-8')
    i, j = page.find(BEGIN), page.find(END)
    if i < 0 or j < 0:
        sys.exit('в галерее нет маркеров палитры — вставьте %s … %s' % (BEGIN, END))

    fresh = build(pairs())
    current = page[i:j + len(END)]
    if current.strip() == fresh.strip():
        print('галерея сходится с tokens.css')
        return

    if check:
        sys.exit('галерея отстала от tokens.css — запустите без --проверить')

    PAGE.write_text(page[:i] + fresh + page[j + len(END):], encoding='utf-8')
    print('палитра галереи переписана из tokens.css: %d ролей' % len(USED))


if __name__ == '__main__':
    main()
