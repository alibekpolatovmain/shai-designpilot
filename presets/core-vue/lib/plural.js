/* Русское число словом.

   «Перенести 2 встреч» — та самая мелочь, по которой видно, что интерфейс
   переводили, а не писали. Правило одно и общее: 1 — единственное,
   2–4 — родительный единственного, 5–20 и всё на 0/5–9 — родительный
   множественного.

   Формы передаются в порядке «одна, две, пять» — так их короче держать
   рядом со строкой, где они нужны. */
export function plural(n, one, few, many) {
  const abs = Math.abs(n) % 100
  const last = abs % 10
  if (abs > 10 && abs < 20) return many
  if (last > 1 && last < 5) return few
  if (last === 1) return one
  return many
}

/* Число вместе со словом: 1 встреча, 2 встречи, 5 встреч */
export function count(n, one, few, many) {
  return `${n} ${plural(n, one, few, many)}`
}
