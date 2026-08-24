#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Линтер дизайн-системы shainote.

Две проверки:

1. **Единство словаря.** Токены объявлены дважды — в `assets/css/main.css`
   (лендинг, ванильный CSS) и в `webapp/src/design/tokens.css` (тема Tailwind
   для кабинета). Две копии одних чисел расходятся молча, поэтому цвет,
   радиус и тень сверяются значение в значение.

2. **Значения из системы, а не с потолка** — в разметке кабинета. Для Tailwind
   это критично: `p-[13px]` и `text-[#1a3b3c]` пишутся так же легко, как раньше
   `.58rem`, и бардак просто переезжает в строку классов.

Запуск:  python3 tools/design-lint.py
Ненулевой код возврата = расхождение.

Проверять сам линтер подсунутым нарушением, прежде чем верить его «чисто».
"""
import re
import sys
import pathlib

LANDING_TOKENS = pathlib.Path('assets/css/main.css')
VUE_TOKENS = pathlib.Path('webapp/src/design/tokens.css')
VUE_DIR = pathlib.Path('webapp/src')

# ─────────────────────── Единство словаря ───────────────────────

# Слева имя в main.css, справа — в палитре кабинета (ярус 1, `--p-*`).
#
# Сверять роли (`--color-*`) бессмысленно: они ссылаются на палитру и в
# тёмной теме меняют значение. Общая правда у двух поверхностей — сама
# палитра, её светлая половина: лендинг тёмной темы не имеет.
#
# Сверяются цвет и тень: это бренд, он один на обе поверхности, и расхождение
# в нём — всегда ошибка. Радиусы и кегли НЕ сверяются намеренно: лендинг
# продаёт (капсулы, крупный кегль), кабинет обслуживает работу (8px, 14px).
# Одна система, две калибровки — см. DESIGN.md, «Форма по режиму поверхности».
SHARED = {
    'ink': 'p-strong', 'ink-900': 'p-inverse-hover',
    'brand-600': 'p-focus', 'brand-700': 'p-accent', 'brand-800': 'p-accent-hover',
    'brand-200': 'p-accent-line', 'brand-100': 'p-accent-soft', 'brand-50': 'p-accent-quiet',
    'white': 'p-raised', 'surface': 'p-surface', 'surface-2': 'p-surface-2',
    'line': 'p-line', 'line-strong': 'p-line-strong', 'line-control': 'p-line-control',
    'text': 'p-text', 'text-soft': 'p-text-soft', 'muted': 'p-muted',
    'caution': 'p-danger', 'on-dark': 'p-on-inverse',
    'shadow-xs': 'shadow-xs', 'shadow-sm': 'shadow-sm', 'shadow-md': 'shadow-md',
    'shadow-lg': 'shadow-lg', 'shadow-brand': 'shadow-brand',
}


def declared(css):
    out = {}
    for m in re.finditer(r'--([a-z0-9-]+):\s*([^;]+);', css):
        out[m.group(1)] = ' '.join(m.group(2).split())
    return out


def light_half(v):
    """Светлая половина light-dark(): та, что должна совпасть с лендингом.

    Запятую ищем на нулевой глубине скобок — внутри аргумента она своя,
    у rgba() их три, и наивный split() резал цвет пополам."""
    v = v.strip()
    if not v.startswith('light-dark('):
        return v
    body = v[len('light-dark('):]
    depth, i = 0, 0
    while i < len(body):
        c = body[i]
        if c == '(':
            depth += 1
        elif c == ')':
            if depth == 0:
                break
            depth -= 1
        elif c == ',' and depth == 0:
            return body[:i].strip()
        i += 1
    return body[:i].strip()


def resolve(v, table, depth=3):
    """Разворачивает var(--p-…) до литерала: тени собраны из палитры."""
    for _ in range(depth):
        def sub(m):
            name = m.group(1)
            return light_half(table[name]) if name in table else m.group(0)
        nv = re.sub(r'var\(--([a-z0-9-]+)\)', sub, v)
        if nv == v:
            break
        v = nv
    return light_half(v)


def norm(v):
    return v.replace(', ', ',').replace('0.', '.').lower()


def lint_tokens():
    problems = []
    if not (LANDING_TOKENS.exists() and VUE_TOKENS.exists()):
        return problems
    landing = declared(LANDING_TOKENS.read_text(encoding='utf-8'))
    vue = declared(VUE_TOKENS.read_text(encoding='utf-8'))
    for a, b in SHARED.items():
        if a not in landing:
            problems.append(('словарь', 0, '--%s нет в %s' % (a, LANDING_TOKENS)))
        elif b not in vue:
            problems.append(('словарь', 0, '--%s нет в %s' % (b, VUE_TOKENS)))
        elif norm(light_half(landing[a])) != norm(resolve(vue[b], vue)):
            problems.append(('словарь', 0, '--%s = %s, а --%s = %s' % (
                a, landing[a], b, resolve(vue[b], vue))))
    return problems


# ─────────────────────── Vue + Tailwind ───────────────────────

CLASS_ATTR = re.compile(r'(?:^|\s)(?::?class|active-class)="([^"]*)"', re.M)

# Половина классов живёт не в разметке, а в объектах внутри <script>:
# variants у кнопки, box у поля, sizes у иконочной кнопки. Линтер их не видел
# и молчал о `px-[13px]`, написанном там, — то есть проверял ровно ту часть
# системы, которая и так на виду. Строковые литералы скрипта разбираются по
# тому же словарю; чтобы не принимать за классы обычный текст, литерал берётся
# только когда в нём минимум два токена похожи на утилиты Tailwind.
SCRIPT_BLOCK = re.compile(r'<script[^>]*>(.*?)</script>', re.S)
STRING_LIT = re.compile(r"'([^'\n]{4,400})'|\"([^\"\n]{4,400})\"|`([^`]{4,400})`")
LOOKS_UTILITY = re.compile(
    r'^-?(?:bg|text|border|ring|outline|divide|fill|stroke|shadow|rounded|opacity|'
    r'h|w|min|max|p|px|py|pt|pr|pb|pl|m|mx|my|mt|mr|mb|ml|gap|space|flex|grid|col|row|'
    r'items|justify|place|self|inline|block|hidden|absolute|relative|fixed|sticky|'
    r'top|right|bottom|left|inset|z|font|leading|tracking|whitespace|truncate|'
    r'transition|duration|ease|animate|cursor|pointer|select|overflow|object|'
    r'translate|scale|rotate|backdrop|underline|uppercase|tabular|shrink|grow|basis)'
    r'(?:-|$)')


def class_lists(src):
    """Все места, где в файле перечислены классы: и разметка, и скрипт."""
    for m in CLASS_ATTR.finditer(src):
        yield m.start(), m.group(1)
    for block in SCRIPT_BLOCK.finditer(src):
        for lit in STRING_LIT.finditer(block.group(1)):
            value = next(g for g in lit.groups() if g is not None)
            parts = value.split()
            if len(parts) < 2:
                continue
            hits = sum(1 for p in parts if LOOKS_UTILITY.match(p.split(':')[-1]))
            if hits >= 2:
                yield block.start(1) + lit.start(), value

# Ступени ритма — 2,4,6,8,10,12,16,20,24,32,40,48px в записи Tailwind
RHYTHM_STEPS = {'0', '0.5', '1', '1.5', '2', '2.5', '3', '4', '5', '6', '8', '10', '12', 'px', 'auto'}
NAMED_SPACE = {'ctl', 'ctl-inner', 'side', 'rail', 'topbar', 'playbar', 'tsc', 'row', 'stack'}
RHYTHM = re.compile(r'^-?(?:p|m)[xytrbles]?-(.+)$|^-?gap(?:-[xy])?-(.+)$')

# Утилиты, где часть после дефиса — толщина, сторона или ключевое слово, а не цвет
NOT_COLOR = re.compile(r'^(?:[xytrbles]-)?(?:0|1|2|3|4|8|x|y|t|r|b|l|e|s|none|solid|dashed|dotted|hidden|collapse|separate|auto)$'
                       r'|^offset-(?:0|1|2|4|8)$')
ARBITRARY_OK = ('data-', 'aria-', 'group-', 'peer-', 'transition-', 'grid-cols-', 'grid-rows-')
TEXT_KEYWORDS = {'left', 'right', 'center', 'justify', 'balance', 'pretty', 'wrap',
                 'nowrap', 'ellipsis', 'clip', 'start', 'end'}


def theme_names(css, prefix):
    names = {m.group(1) for m in re.finditer(r'--' + prefix + r'-([a-z0-9-]+):', css)}
    # --text-ui--line-height объявляет интерлиньяж, а не отдельный кегль
    return {n for n in names if not n.endswith('--line-height')}


def lint_vue():
    if not VUE_DIR.exists():
        return []
    theme = VUE_TOKENS.read_text(encoding='utf-8')
    colors = theme_names(theme, 'color') | {'transparent', 'current', 'inherit'}
    texts = theme_names(theme, 'text')
    problems = []

    for f in sorted(VUE_DIR.rglob('*.vue')):
        src = f.read_text(encoding='utf-8')
        rel = str(f)
        for at, value in class_lists(src):
            ln = src.count('\n', 0, at) + 1
            for raw in value.split():
                token = raw.strip('\'",`[]()').split(':')[-1].lstrip('!')
                if not token or token in ('&&', '||', '?'):
                    continue

                if '-[' in token and not token.startswith(ARBITRARY_OK):
                    problems.append(('произвольное', ln, '%s — значение мимо темы (%s)' % (raw, rel)))
                    continue

                r = RHYTHM.match(token)
                if r:
                    v = r.group(1) or r.group(2)
                    if v not in RHYTHM_STEPS and v not in NAMED_SPACE:
                        problems.append(('ритм', ln, '%s — ступень вне шкалы (%s)' % (raw, rel)))
                    continue

                c = re.match(r'^(?:bg|border|fill|stroke|ring|outline|decoration|caret|accent|divide)(?:-[xytrbles])?-([a-z0-9-]+?)(?:/\d+)?$', token)
                if c:
                    v = c.group(1)
                    if not NOT_COLOR.match(v) and v not in colors:
                        problems.append(('цвет', ln, '%s — нет такого цвета в теме (%s)' % (raw, rel)))
                    continue

                t = re.match(r'^text-([a-z0-9-]+?)(?:/\d+)?$', token)
                if t:
                    v = t.group(1)
                    if v not in colors and v not in texts and v not in TEXT_KEYWORDS:
                        problems.append(('кегль/цвет', ln, '%s — нет ни такого кегля, ни цвета (%s)' % (raw, rel)))
    return problems


def main():
    problems = lint_tokens() + lint_vue()
    if not problems:
        print('design-lint: чисто — словарь сходится, значения в классах из системы')
        return 0
    print('design-lint: расхождений %d' % len(problems))
    for kind, ln, msg in problems:
        if msg.endswith(')') and ' (' in msg:
            text, where = msg.rsplit(' (', 1)
            print('  %-13s %s:%s  %s' % (kind, where.rstrip(')'), ln or '-', text))
        else:
            print('  %-13s %s' % (kind, msg))
    return 1


if __name__ == '__main__':
    sys.exit(main())
