<script setup>
/* Иконочная кнопка — квадрат той же высоты, что и обычная того же размера.

   По умолчанию без рамки: опознаёт её сам глиф, а он несёт 8:1 к фону —
   больше, чем WCAG 1.4.11 требует от кромки. Рамка вокруг маленькой иконки
   добавляет коробку и ничего не сообщает; там, где иконок несколько подряд
   (шапка встречи, строка списка), коробки складывались в забор.

   ── Почему здесь ровно один корень ──────────────────────────────
   Раньше кнопка сама заворачивалась в подсказку, и корнем компонента
   оказывался `UiTooltip`. Провайдер и корень подсказки в Reka безрелевые —
   они рендерят слот и не имеют своего элемента, поэтому падающие атрибуты
   до кнопки не доезжали. А `DropdownMenuTrigger as-child` передаёт именно
   атрибутами: `onClick`, `aria-expanded`, `aria-haspopup` и ссылку на
   элемент для привязки меню.

   Итог: **все семь меню на иконочных кнопках были мертвы** — шаблоны,
   встречи, папки, интеграции, экран встречи, «Сегодня» и переключатель
   темы. Разметка безупречна, контраст в норме, линтер чист; кнопка просто
   ничего не делала. Нашлось это не проверкой, а тем, что владелец нажал.

   Поэтому корень теперь — сам `<button>`, а подсказка навешивается снаружи:
   `<UiTooltip text="…"><UiIconButton …/></UiTooltip>`. */
defineOptions({ inheritAttrs: false })

const props = defineProps({
  label: { type: String, required: true },
  size: { type: String, default: 'md' },       // sm | md | lg
  variant: { type: String, default: 'ghost' }, // ghost | outline
})

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
  <button
    v-bind="$attrs"
    type="button" :aria-label="label"
    class="press grid shrink-0 place-items-center rounded-control border [&>svg]:pointer-events-none"
    :class="[sizes[props.size], glyph[props.size], variants[props.variant]]"
  >
    <slot />
  </button>
</template>
