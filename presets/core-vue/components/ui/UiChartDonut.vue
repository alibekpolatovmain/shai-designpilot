<script setup>
/* Доли целого: откуда приходят встречи — Zoom, Meet, Teams, загруженные файлы.

   Кольцо, а не пирог: в центре остаётся место для главного числа, и глаз
   сравнивает длины дуг, а не площади секторов — площади человек оценивает
   плохо, это старый и подтверждённый результат.

   Долей не больше пяти, мелочь ниже пяти процентов сворачивается в «прочее»:
   сектор в три процента на кольце 160px — дуга в несколько пикселей, её
   нельзя ни навести, ни подписать.

   Подписи стоят рядом со значениями, а не в легенде сбоку: легенда заставляет
   глаз ходить между цветом и словом, и на четырёх цветах это уже утомляет. */
import { computed } from 'vue'
import { parts, num } from '../../lib/chart.js'

const props = defineProps({
  points: { type: Array, required: true },  // [{ label, value }]
  caption: { type: String, required: true },
  unit: { type: String, default: '' },
})

/* Оттенки одного цвета, а не радуга: категории здесь не спорят, а
   складываются в целое, и разные краски сообщили бы противоположное. */
const shades = ['var(--color-accent)', 'var(--color-accent-hover)', 'var(--color-accent-line)',
                'var(--color-surface-2)', 'var(--color-line-strong)']
const R = 54
const C = 2 * Math.PI * R

const data = computed(() => parts(props.points))
const arcs = computed(() => {
  let acc = 0
  return data.value.items.map((i, idx) => {
    const dash = i.share * C
    const arc = { ...i, dash, offset: -acc, color: shades[idx % shades.length] }
    acc += dash
    return arc
  })
})
</script>

<template>
  <figure class="flex flex-wrap items-center gap-5">
    <div class="relative shrink-0">
      <svg viewBox="0 0 128 128" class="h-32 w-32 -rotate-90" role="presentation">
        <circle
          v-for="a in arcs" :key="a.label" cx="64" cy="64" :r="R" fill="none" stroke-width="16"
          :stroke="a.color" :stroke-dasharray="`${a.dash} ${C - a.dash}`" :stroke-dashoffset="a.offset"
        />
      </svg>
      <span class="absolute inset-0 flex flex-col items-center justify-center">
        <b class="text-h2 font-semibold tabular-nums tracking-h2 text-strong">{{ num(data.total) }}</b>
        <span class="text-caption text-muted">{{ unit || 'всего' }}</span>
      </span>
    </div>

    <figcaption class="flex min-w-0 flex-1 flex-col gap-1.5">
      <span class="text-ui font-semibold text-strong">{{ caption }}</span>
      <ul class="flex list-none flex-col gap-1 p-0">
        <li v-for="a in arcs" :key="a.label" class="flex items-center gap-2 text-caption">
          <span class="h-2.5 w-2.5 shrink-0 rounded-hair" :style="{ background: a.color }" aria-hidden="true" />
          <span class="min-w-0 truncate text-text">{{ a.label }}</span>
          <span class="ml-auto shrink-0 tabular-nums text-muted">
            {{ num(a.value) }} · {{ Math.round(a.share * 100) }}%
          </span>
        </li>
      </ul>
      <span v-if="arcs.some((a) => a.rest)" class="text-caption text-muted">
        В «прочее» свёрнуто: {{ arcs.find((a) => a.rest).rest.join(', ') }}
      </span>
    </figcaption>
  </figure>
</template>
