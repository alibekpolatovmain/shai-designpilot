<script setup>
/* Иконочная кнопка — квадрат той же высоты, что и обычная того же размера.

   По умолчанию без рамки: опознаёт её сам глиф, а он несёт 8:1 к фону —
   больше, чем WCAG 1.4.11 требует от кромки. Рамка вокруг маленькой иконки
   добавляет коробку и ничего не сообщает; там, где иконок несколько подряд
   (шапка встречи, строка списка), коробки складывались в забор.

   Наведение даёт заливку, фокус — кольцо: состояние показывается тогда,
   когда оно есть, а не постоянной обводкой на всякий случай. */
const props = defineProps({
  label: { type: String, required: true },
  /* Подсказка по умолчанию включена: у кнопки без рамки и без подписи смысл
     держится на одной иконке, и «догадайся сам» — не интерфейс. Диктор
     читает `label`, глаз получает то же самое по наведению и по фокусу.
     Выключать стоит там, где кнопка уже подписана соседним текстом. */
  tip: { type: Boolean, default: true },
  size: { type: String, default: 'md' },       // sm | md | lg
  variant: { type: String, default: 'ghost' }, // ghost | outline
})
import UiTooltip from './UiTooltip.vue'

const sizes = { sm: 'h-ctl-sm w-ctl-sm', md: 'h-ctl w-ctl', lg: 'h-ctl-lg w-ctl-lg' }
const variants = {
  ghost: 'border-transparent bg-transparent text-text-soft hover:bg-surface hover:text-strong active:bg-surface-2',
  outline: 'border-line-control bg-transparent text-text-soft hover:border-strong hover:text-strong active:bg-surface-2',
}
/* Классы перечислены целиком: Tailwind собирает CSS по тексту исходника,
   и строка, склеенная в рантайме, до сборщика не доедет. */
const glyph = {
  sm: '[&>svg]:h-3.5 [&>svg]:w-3.5',
  md: '[&>svg]:h-4 [&>svg]:w-4',
  lg: '[&>svg]:h-5 [&>svg]:w-5',
}
</script>

<template>
  <component :is="props.tip ? UiTooltip : 'template'" :text="props.tip ? label : undefined">
  <button
    type="button" :aria-label="label"
    class="press grid shrink-0 place-items-center rounded-control border [&>svg]:pointer-events-none"
    :class="[sizes[props.size], glyph[props.size], variants[props.variant]]"
  >
    <slot />
  </button>
  </component>
</template>
