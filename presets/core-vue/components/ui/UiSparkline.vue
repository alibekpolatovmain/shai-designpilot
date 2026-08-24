<script setup>
/* Спарклайн: ход величины внутри строки или карточки показателя.

   Без осей, подписей и наведения — это не график, а знак направления рядом
   с числом. Как только к нему хочется добавить подпись, значит нужен
   настоящий график, а не спарклайн.

   Слово вместо цвета: рост окрашен акцентом, падение — приглушённым, но
   рядом обязательно стоит знак и число, потому что цветом одним разницу
   «вверх/вниз» видят не все. */
import { computed } from 'vue'
import { line, path, num } from '../../lib/chart.js'

const props = defineProps({
  values: { type: Array, required: true },
  label: { type: String, required: true },
  unit: { type: String, default: '' },
})

const W = 64
const H = 20
const max = computed(() => Math.max(...props.values, 1))
const pts = computed(() => line(props.values, max.value, W, H))
const d = computed(() => path(pts.value))
const delta = computed(() => {
  const [first, last] = [props.values[0] || 0, props.values.at(-1) || 0]
  return first ? Math.round(((last - first) / first) * 100) : 0
})
</script>

<template>
  <span class="inline-flex items-center gap-2">
    <svg :viewBox="`0 0 ${W} ${H}`" class="h-5 w-16 shrink-0 overflow-visible" role="img"
         :aria-label="`${label}: ${num(values.at(-1))}${unit}, ${delta >= 0 ? 'рост' : 'снижение'} на ${Math.abs(delta)}%`">
      <path :d="d" fill="none" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"
            :class="delta >= 0 ? 'stroke-accent' : 'stroke-muted'" vector-effect="non-scaling-stroke" />
    </svg>
    <span class="text-caption tabular-nums" :class="delta >= 0 ? 'text-accent' : 'text-muted'" aria-hidden="true">
      {{ delta >= 0 ? '+' : '−' }}{{ Math.abs(delta) }}%
    </span>
  </span>
</template>
