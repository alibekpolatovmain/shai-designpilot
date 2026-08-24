<script setup>
/* Шкала расхода: сколько израсходовано из того, что доступно.

   Это не прогресс. Прогресс идёт к завершению и радует, когда полон; шкала
   расхода наоборот — полная означает «кончилось». Поэтому у неё есть порог:
   заполнение меняет цвет, когда остаётся мало, и подпись говорит остаток,
   а не израсходованное. Человеку важно «осталось 240 минут», а не
   «израсходовано 760».

   Роль meter, а не progressbar: диктор произносит «столько-то из столько-то»,
   а не проценты выполнения. */
import { computed } from 'vue'
import { num } from '../../lib/chart.js'

const props = defineProps({
  value: { type: Number, required: true },
  max: { type: Number, required: true },
  label: { type: String, required: true },
  unit: { type: String, default: '' },
  /* Доля остатка, ниже которой шкала предупреждает */
  warnAt: { type: Number, default: 0.2 },
})

const left = computed(() => Math.max(0, props.max - props.value))
const share = computed(() => Math.min(1, props.value / (props.max || 1)))
const state = computed(() => (left.value <= 0 ? 'over' : left.value / props.max <= props.warnAt ? 'warn' : 'ok'))
const fill = { ok: 'bg-accent', warn: 'bg-warning', over: 'bg-danger' }
</script>

<template>
  <div class="flex flex-col gap-1.5">
    <div class="flex flex-wrap items-baseline justify-between gap-2">
      <span class="text-ui font-semibold text-strong">{{ label }}</span>
      <span
        class="text-caption tabular-nums"
        :class="state === 'ok' ? 'text-muted' : state === 'warn' ? 'text-on-warning-soft' : 'text-on-danger-soft'"
      >
        {{ state === 'over' ? 'лимит исчерпан' : `осталось ${num(left)}${unit}` }}
      </span>
    </div>
    <div
      class="h-2 w-full overflow-hidden rounded-full bg-surface-2"
      role="meter" :aria-valuenow="value" :aria-valuemin="0" :aria-valuemax="max"
      :aria-label="`${label}: израсходовано ${num(value)} из ${num(max)}${unit}`"
    >
      <span class="block h-full rounded-full transition-[width] duration-slow" :class="fill[state]"
            :style="{ width: `${share * 100}%` }" />
    </div>
    <span class="text-caption tabular-nums text-muted">
      израсходовано {{ num(value) }} из {{ num(max) }}{{ unit }}
    </span>
  </div>
</template>
