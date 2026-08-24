<script setup>
/* Сетку не проверить рассуждением — её надо увидеть поверх экрана.
   Оверлей рисует те же 4 / 8 / 12 колонок и тот же желоб. */
defineProps({ show: Boolean })
</script>

<template>
  <div
    v-if="show"
    class="pointer-events-none absolute inset-0 grid grid-cols-4 gap-4 one:grid-cols-8 frame:grid-cols-12 frame:gap-6"
    aria-hidden="true"
  >
    <span
      v-for="i in 12" :key="i"
      class="rounded-hair bg-danger-soft"
      :class="[i > 8 ? 'hidden frame:block' : i > 4 ? 'hidden one:block' : '']"
    />
  </div>
</template>
