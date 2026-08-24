<script setup>
/* Индикатор ожидания без прогресса. Внутри кнопки заменяет иконку,
   отдельно — сопровождается подписью: крутящийся круг без слов
   не говорит, чего именно ждать. */
defineProps({ size: { type: Number, default: 16 } })
</script>

<template>
  <span
    class="inline-block shrink-0 rounded-full border-2 border-current border-t-transparent
           opacity-70 motion-safe:animate-spin-slow"
    :style="{ width: size + 'px', height: size + 'px' }"
    aria-hidden="true"
  />
</template>
