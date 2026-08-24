<script setup>
/* Страничная раскладка одним местом: ширина, поля и вертикальный ритм.
   Шесть экранов повторяли одну и ту же строку классов — это ровно тот дрейф,
   из-за которого отступы потом расходятся по экранам. */
defineProps({ gap: { type: String, default: 'gap-stack' } })
</script>

<template>
  <div class="flex w-full max-w-page flex-col p-4 frame:p-6" :class="gap">
    <slot />
  </div>
</template>
