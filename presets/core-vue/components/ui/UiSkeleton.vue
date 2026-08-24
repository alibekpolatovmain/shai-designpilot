<script setup>
/* Заглушка загрузки. У неё обязан быть предел: в живом кабинете скелетон
   на месте плеера висел, пока аудио не пришло, и читался как «звука нет».
   Поэтому она всегда парная к состоянию, а не вечная. */
defineProps({ w: { type: String, default: 'w-full' }, h: { type: String, default: 'h-4' } })
</script>

<template>
  <span :class="['block rounded-hair bg-surface-2 motion-safe:animate-fade-pulse', w, h]" aria-hidden="true" />
</template>
