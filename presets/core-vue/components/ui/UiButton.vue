<script setup>
import UiSpinner from './UiSpinner.vue'

/* Кнопка. Три размера, как в любом ките, и у каждого своё место:
   sm — внутри строки или таблицы, где кнопка не главная;
   md — по умолчанию;
   lg — единственное действие на пустом экране, мобильный призыв.

   ── Почему вторичная кнопка больше не в рамке ─────────────
   Контраст обязан нести тот элемент, который **опознаёт** контрол. У кнопки
   с подписью это подпись: слова «Загрузить файл» на тихой заливке уже
   читаются как кнопка. Кромка там работает формой, а не опознанием, и
   волосяной линии для формы достаточно.

   Прежний вариант ставил на каждую вторичную кнопку кромку 3:1 — ту самую,
   что нужна пустому полю ввода, где опознавать нечего, кроме рамки. В итоге
   экран с четырьмя кнопками читался как четыре обведённые коробки: контраст
   тратился там, где его работа уже сделана словом.

   Так же устроено у тех, на кого стоит смотреть: у Claude вторичная кнопка —
   прозрачная с кромкой в 10% белого (замерено), у shadcn `outline` берёт
   светлый `--input`, у Ant `default` — #d9d9d9. Сильную кромку из них не
   ставит никто; её место — поле ввода.

   Цвет рамки задаёт ВАРИАНТ, а не база: две утилиты одного свойства
   (border-transparent и border-line-control) конфликтуют, и в CSS побеждает
   не та, что стоит позже в атрибуте, а та, что позже в сгенерированном
   файле. Из-за этого ghost-кнопки однажды остались без рамки. */
const props = defineProps({
  variant: { type: String, default: 'secondary' }, // primary | secondary | outline | ghost | dark | danger | link
  size: { type: String, default: 'md' },       // sm | md | lg
  small: Boolean,                              // устаревшее: то же, что size="sm"
  block: Boolean,                              // во всю ширину: мобильный призыв, форма
  loading: Boolean,                            // действие пошло, но ещё не завершилось
  as: { type: String, default: 'button' },
})

const variants = {
  /* Заливка и есть акцент. Цветное свечение под кнопкой — язык витрины:
     в инструменте оно читается как украшение, а не как «главное действие». */
  primary: 'border-transparent bg-accent text-on-solid hover:bg-accent-hover active:bg-accent-hover',
  dark: 'border-transparent bg-inverse text-on-inverse hover:bg-inverse-hover active:bg-inverse-hover',
  /* По умолчанию: тихая заливка плюс волосяная кромка */
  secondary: 'border-line-strong bg-surface text-strong hover:border-strong hover:bg-surface-2 active:bg-surface-2',
  /* Кромка 3:1 — для кнопки на чужом фоне (снимок, цветная плашка), где
     заливка системы не отличается от подложки и опознать нечем */
  outline: 'border-line-control bg-transparent text-strong hover:border-strong hover:bg-surface active:bg-surface-2',
  /* Совсем тихая: строка списка, панель инструментов — проявляется наведением */
  ghost: 'border-transparent bg-transparent text-text-soft hover:bg-surface hover:text-strong active:bg-surface-2',
  danger: 'border-transparent bg-danger text-on-solid hover:bg-danger/90 active:bg-danger/80',
  link: 'border-transparent bg-transparent px-0 text-accent underline-offset-4 hover:underline',
}
const sizes = {
  sm: 'h-ctl-sm gap-1.5 px-2.5 text-caption',
  md: 'h-ctl gap-2 px-4 text-ui',
  lg: 'h-ctl-lg gap-2 px-5 text-ui',
}
</script>

<template>
  <component
    :is="props.as"
    class="inline-flex shrink-0 items-center justify-center whitespace-nowrap rounded-control border
           press font-semibold leading-none
           disabled:cursor-not-allowed disabled:border-transparent disabled:bg-surface-2
           disabled:text-muted disabled:shadow-none disabled:hover:bg-surface-2"
    :class="[
      variants[props.variant],
      sizes[props.small ? 'sm' : props.size],
      props.block && 'w-full',
      props.loading && 'pointer-events-none',
    ]"
    :aria-busy="props.loading || undefined"
  >
    <UiSpinner v-if="props.loading" :size="props.size === 'sm' ? 13 : 15" />
    <slot />
  </component>
</template>
