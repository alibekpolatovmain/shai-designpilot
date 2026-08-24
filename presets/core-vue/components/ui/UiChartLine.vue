<script setup>
/* Ломаная с заливкой: величина во времени, когда точек много — минуты за
   тридцать дней, встречи за квартал.

   Столбики или ломаная — не вкус. Столбики сравнивают периоды поштучно и
   разваливаются, когда столбиков тридцать: получается частокол шириной в
   три пикселя. Ломаная показывает ход, но требует, чтобы между соседними
   точками был смысл: «понедельник → вторник» такой смысл имеет, «Марат →
   Айгерим» нет, поэтому для людей и источников — только столбики.

   Заливка под линией слабая: она помогает увидеть объём, но данные несёт
   линия, и заливка не должна с ней спорить. */
import { computed } from 'vue'
import ChartFrame from './ChartFrame.vue'
import { scale, line, path, num } from '../../lib/chart.js'

const props = defineProps({
  points: { type: Array, required: true },  // [{ label, value }]
  caption: { type: String, required: true },
  unit: { type: String, default: '' },
  height: { type: String, default: 'h-30' },
})

/* Координаты считаются в условной сетке 100×40 и растягиваются
   preserveAspectRatio="none": так график занимает любую ширину, а толщина
   линии остаётся честной — она задана в пикселях через vector-effect. */
const W = 100
const H = 40
const top = computed(() => scale(Math.max(...props.points.map((p) => p.value), 0)).max)
const pts = computed(() => line(props.points.map((p) => p.value), top.value, W, H))
const stroke = computed(() => path(pts.value))
const area = computed(() => `${stroke.value} L${W},${H} L0,${H} Z`)
</script>

<template>
  <ChartFrame :caption="caption" :points="points" :unit="unit" :height="height" :max="top">
    <svg
      :viewBox="`0 0 ${W} ${H}`" preserveAspectRatio="none" class="h-full w-full overflow-visible"
      role="presentation"
    >
      <path :d="area" class="fill-accent-quiet" />
      <path
        :d="stroke" fill="none" class="stroke-accent" stroke-width="2"
        stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"
      />
    </svg>

    <!-- Точки — отдельным слоем в обычных координатах: круг внутри
         растянутого viewBox превратился бы в эллипс -->
    <div class="pointer-events-none absolute inset-0 flex items-stretch">
      <span
        v-for="(p, i) in points" :key="p.label"
        class="group pointer-events-auto relative flex-1"
        tabindex="0" :aria-label="`${p.label}: ${num(p.value)}${unit}`"
      >
        <span
          class="absolute h-2 w-2 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-accent
                 bg-raised opacity-0 transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100"
          :style="{ left: `${(i / Math.max(1, points.length - 1)) * 100}%`, top: `${(pts[i][1] / H) * 100}%` }"
        />
        <span
          class="pointer-events-none absolute left-1/2 z-sticky -translate-x-1/2 -translate-y-full whitespace-nowrap
                 rounded-hair bg-inverse px-1.5 text-caption tabular-nums text-on-inverse opacity-0
                 transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100"
          :style="{ top: `${(pts[i][1] / H) * 100}%` }"
        >{{ p.label }} · {{ num(p.value) }}{{ unit }}</span>
      </span>
    </div>
  </ChartFrame>
</template>
