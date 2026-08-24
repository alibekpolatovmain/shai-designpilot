#!/usr/bin/env bash
# Установка навыка designpilot.
#
#   ./install.sh            → ~/.claude/skills/designpilot
#   ./install.sh /путь      → в указанный каталог навыков
#
# Ставится копированием, а не симлинком: навык самодостаточен, и копия
# переживает удаление исходника. Повторный запуск обновляет установленное.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
DST="${1:-$HOME/.claude/skills}/designpilot"

mkdir -p "$(dirname "$DST")"
rm -rf "$DST"
cp -R "$SRC" "$DST"
rm -rf "$DST/.git" "$DST/install.sh"
chmod +x "$DST/scripts/sync.py"

echo "designpilot установлен: $DST"
echo "Вызов: /designpilot [автопилот|ручной] <ссылка на Figma / сайт / путь к файлам>"
