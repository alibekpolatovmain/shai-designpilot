/* Внешний вид: тема и плотность.

   Оба переключателя — это два data-атрибута на корне документа, а не два
   набора классов по компонентам. Значения приходят из токенов: тему несёт
   `color-scheme`, плотность — четыре числа метрики. Поэтому здесь нет ни
   одного цвета и ни одного размера, только выбор пользователя и его память.

   «Система» — не третья тема, а отказ от выбора: атрибут снимается, и
   страница снова слушает `prefers-color-scheme`. Значение, с которым
   страница открылась, запоминается: кабинет умеет жить внутри чужой
   оболочки (артефакт, встраивание), и «Система» должна возвращать её выбор,
   а не затирать его. */
import { ref, watch } from 'vue'

const KEY = 'shainote:appearance'
const root = document.documentElement
const host = root.dataset.theme || ''

function stored() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '{}') || {}
  } catch {
    return {} /* приватное окно, запрет на хранилище — просто без памяти */
  }
}

const seed = stored()
export const themes = [
  { value: 'system', label: 'Как в системе', note: 'Следовать настройке устройства' },
  { value: 'light', label: 'Светлая', note: 'Всегда светлый интерфейс' },
  { value: 'dark', label: 'Тёмная', note: 'Всегда тёмный интерфейс' },
]
export const densities = [
  { value: 'comfortable', label: 'Обычная', note: 'Контролы 36px — по умолчанию' },
  { value: 'compact', label: 'Компактная', note: 'Контролы 30px, строки плотнее' },
]

export const theme = ref(['light', 'dark'].includes(seed.theme) ? seed.theme : 'system')
export const density = ref(seed.density === 'compact' ? 'compact' : 'comfortable')

export const themeLabel = () => themes.find((t) => t.value === theme.value).label

function apply() {
  if (theme.value === 'system') {
    if (host) root.dataset.theme = host
    else delete root.dataset.theme
  } else {
    root.dataset.theme = theme.value
  }

  root.dataset.density = density.value

  try {
    localStorage.setItem(KEY, JSON.stringify({ theme: theme.value, density: density.value }))
  } catch { /* без памяти выбор живёт до перезагрузки */ }
}

watch([theme, density], apply, { immediate: true })
