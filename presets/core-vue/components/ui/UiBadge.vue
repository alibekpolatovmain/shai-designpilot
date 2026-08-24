<script setup>
/* Счётчик рядом с названием: сколько встреч в папке, сколько ждёт решения,
   сколько строк под фильтром.

   Появился по факту дублирования: одна и та же связка «круглая плашка,
   табличные цифры, кегль подписи» была написана в пяти местах, и в трёх из
   них по-разному — где-то `text-text-soft`, где-то `text-muted`, где-то
   своя высота. Счётчик — не оформление, а элемент со своим смыслом:
   он всегда про количество и всегда стоит справа от того, что считает. */
defineProps({
  tone: { type: String, default: 'quiet' }, // quiet | accent | danger | inverse
  value: { type: [Number, String], required: true },
})

const tones = {
  quiet: 'bg-surface-2 text-text-soft',
  accent: 'bg-accent-quiet text-accent',
  /* Сплошной цвет — только там, где число само по себе требует решения */
  danger: 'bg-danger text-on-solid',
  inverse: 'bg-inverse text-on-inverse',
}
</script>

<template>
  <span
    class="inline-flex h-5 min-w-5 items-center justify-center rounded-full px-1.5 align-middle
           text-caption font-bold tabular-nums"
    :class="tones[tone]"
  >{{ value }}</span>
</template>
