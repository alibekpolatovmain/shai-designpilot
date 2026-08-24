<script setup>
/* Столбики: сравнение периодов между собой — минуты по дням, встречи по
   неделям, расход по участникам.

   Основание всегда ноль. Обрезанное основание увеличивает разницу в разы:
   столбики 96 и 120 при оси от 90 выглядят как «втрое больше». Это самый
   частый способ соврать графиком, и он запрещён здесь на уровне компонента —
   вертикальной оси с произвольным началом просто нет.

   Каждый столбик — цель для клавиатуры: Tab проходит по ним, значение
   произносится. Наведение мышью и фокус показывают одно и то же. */
import ChartFrame from './ChartFrame.vue'
import { num } from '../../lib/chart.js'

defineProps({
  points: { type: Array, required: true },  // [{ label, value }]
  caption: { type: String, required: true },
  unit: { type: String, default: '' },
  height: { type: String, default: 'h-30' },
})
</script>

<template>
  <ChartFrame :caption="caption" :points="points" :unit="unit" :height="height">
    <template #default="{ top }">
    <div class="flex h-full items-end gap-1.5">
      <button
        v-for="p in points" :key="p.label" type="button"
        class="group relative flex h-full min-w-0 flex-1 cursor-default flex-col justify-end rounded-micro"
        :aria-label="`${p.label}: ${num(p.value)}${unit}`"
      >
        <span
          class="rounded-micro bg-accent-line transition-colors group-hover:bg-accent group-focus-visible:bg-accent"
          :style="{ height: `${Math.max(1.5, (p.value / top) * 100)}%` }"
        />
        <span
          class="pointer-events-none absolute -top-5 left-1/2 z-sticky -translate-x-1/2 whitespace-nowrap
                 rounded-hair bg-inverse px-1.5 text-caption tabular-nums text-on-inverse opacity-0
                 transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100"
        >{{ num(p.value) }}{{ unit }}</span>
      </button>
    </div>
    </template>
    <template #legend>
      <span class="flex w-full gap-1.5" aria-hidden="true">
        <span v-for="p in points" :key="p.label" class="min-w-0 flex-1 truncate text-center text-caption text-muted">
          {{ p.label }}
        </span>
      </span>
    </template>
  </ChartFrame>
</template>
