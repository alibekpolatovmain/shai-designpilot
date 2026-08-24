/* Расчётная часть графиков: шкала, деления, формат чисел.

   Почему без библиотеки. Chart.js — 65 КБ gzip, Recharts тянет за собой
   d3-модули на ~90 КБ. За эти деньги мы получили бы анимации, легенды и
   двадцать типов графиков, из которых нужны четыре, и чужую типографику
   поверх нашей. Всё, что нам действительно нужно, — «нормальные» деления и
   форматирование, а это тридцать строк.

   Общая для всех графиков, потому что расхождение шкал внутри одного
   дашборда — самый заметный вид вранья: два столбца рядом, у одного ось до
   120, у другого до 100, и глаз сравнивает высоты, а не числа. */

/* «Нормальные» деления: шаг из ряда 1, 2, 5 и их десятков.

   Считается именно ШАГ, а не максимум: если взять максимум и поделить его на
   четыре, получается ось с подписями 0, 38, 75, 113, 150 — арифметически
   верно и нечитаемо. Сначала выбирается шаг, потом максимум округляется
   вверх до кратного ему, и делений выходит столько, сколько вышло. */
export function scale(value, steps = 4) {
  if (value <= 0) return { max: steps, step: 1, ticks: [0, 1] }
  const raw = value / steps
  const mag = 10 ** Math.floor(Math.log10(raw))
  const norm = raw / mag
  const step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10) * mag
  const max = Math.ceil(value / step) * step
  const ticks = []
  for (let t = 0; t <= max + step / 2; t += step) ticks.push(Math.round(t * 1e6) / 1e6)
  return { max, step, ticks }
}

export const niceMax = (value, steps = 4) => scale(value, steps).max

/* Разряды разделяются узким неразрывным пробелом — по-русски так, а не
   запятой: 1 240, не 1,240. */
export function num(n) {
  return new Intl.NumberFormat('ru-RU').format(n)
}

/* Минуты словом там, где число стоит рядом с существительным */
export function minutes(n) {
  const abs = Math.abs(n) % 100
  const last = abs % 10
  const word = abs > 10 && abs < 20 ? 'минут' : last === 1 ? 'минута' : last > 1 && last < 5 ? 'минуты' : 'минут'
  return `${num(n)} ${word}`
}

/* Ломаная в координатах SVG. Точки приходят значениями, уходят точками
   внутри viewBox 0…w × 0…h; ось Y перевёрнута, потому что в SVG ноль сверху. */
export function line(values, max, w, h) {
  const step = values.length > 1 ? w / (values.length - 1) : 0
  return values.map((v, i) => [i * step, h - (v / max) * h])
}

export function path(points) {
  return points.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ')
}

/* Доли целого: проценты считаются от суммы, мелочь сворачивается в «прочее».

   Порог не вкус: сектор меньше пяти процентов на круге диаметром 160px
   занимает дугу в несколько пикселей — его нельзя ни навести, ни различить,
   а подпись к нему длиннее самого сектора. */
export function parts(items, limit = 5, minShare = 0.05) {
  const total = items.reduce((n, i) => n + i.value, 0) || 1
  const sorted = [...items].sort((a, b) => b.value - a.value)
  const keep = sorted.filter((i, idx) => idx < limit && i.value / total >= minShare)
  const rest = sorted.filter((i) => !keep.includes(i))
  const out = keep.map((i) => ({ ...i, share: i.value / total }))
  if (rest.length) {
    const value = rest.reduce((n, i) => n + i.value, 0)
    out.push({ label: 'Прочее', value, share: value / total, rest: rest.map((i) => i.label) })
  }
  return { total, items: out }
}
