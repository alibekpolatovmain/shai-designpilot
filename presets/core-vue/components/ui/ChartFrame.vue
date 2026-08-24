<script setup>
/* Оправа графика: подпись, ось значений, сетка и текстовый эквивалент.

   Вынесена отдельно, потому что это и есть та часть, которую в самодельных
   графиках забывают, а забыв — получают четыре разных подписи, три разных
   шага сетки и ни одной таблицы для тех, кто форму не видит.

   Сетка только горизонтальная и волосяная: вертикальные линии в столбиковом
   графике повторяют сами столбики, а жирная сетка спорит с данными.

   Таблица sr-only — не любезность, а условие: диаграмма показывает форму,
   данные она не заменяет. `aria-label="график расхода"` данными не является. */
import { computed } from 'vue'
import { scale, num } from '../../lib/chart.js'

const props = defineProps({
  caption: { type: String, required: true },
  /* [{ label, value }] — для оси, таблицы и итога */
  points: { type: Array, required: true },
  unit: { type: String, default: '' },
  /* Высота поля данных; подписи осей стоят снаружи */
  height: { type: String, default: 'h-30' },
  max: { type: Number, default: 0 },
  axis: { type: Boolean, default: true },
  total: { type: Boolean, default: true },
})

const axisScale = computed(() => scale(Math.max(...props.points.map((p) => p.value), 0)))
const top = computed(() => props.max || axisScale.value.max)
const ticks = computed(() =>
  (props.max ? scale(props.max).ticks : axisScale.value.ticks).slice().reverse())
const sum = computed(() => props.points.reduce((n, p) => n + p.value, 0))
defineExpose({ top })
</script>

<template>
  <figure class="flex min-w-0 flex-col gap-2">
    <figcaption class="flex flex-wrap items-baseline justify-between gap-2">
      <span class="text-ui font-semibold text-strong">{{ caption }}</span>
      <span v-if="total" class="text-caption tabular-nums text-muted">всего {{ num(sum) }}{{ unit }}</span>
    </figcaption>

    <div class="flex min-w-0 gap-2">
      <!-- Ось значений: подписи выключены из чтения — те же числа стоят
           в таблице ниже, и диктор не должен читать их дважды -->
      <div
        v-if="axis" class="flex shrink-0 flex-col justify-between text-caption tabular-nums text-muted"
        :class="height" aria-hidden="true"
      >
        <span v-for="t in ticks" :key="t">{{ num(Math.round(t)) }}</span>
      </div>

      <div class="relative min-w-0 flex-1" :class="height">
        <div class="absolute inset-0 flex flex-col justify-between" aria-hidden="true">
          <span v-for="t in ticks" :key="t" class="h-px w-full bg-line" />
        </div>
        <div class="relative h-full"><slot :top="top" /></div>
      </div>
    </div>

    <div v-if="$slots.legend" class="flex flex-wrap gap-3"><slot name="legend" /></div>

    <table class="sr-only">
      <caption>{{ caption }}</caption>
      <tbody>
        <tr v-for="p in points" :key="p.label">
          <th scope="row">{{ p.label }}</th>
          <td>{{ num(p.value) }}{{ unit }}</td>
        </tr>
      </tbody>
      <tfoot v-if="total"><tr><th scope="row">Всего</th><td>{{ num(sum) }}{{ unit }}</td></tr></tfoot>
    </table>
  </figure>
</template>
