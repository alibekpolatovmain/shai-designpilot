<script setup>
/* Показатель: число и что оно значит. На «Сегодня» такие плитки сняты
   намеренно — они не помогают принять решение. Живут там, где число само
   является ответом: расход квоты, счёт в биллинге. */
defineProps({
  value: { type: String, required: true },
  label: { type: String, required: true },
  note: { type: String, default: '' },
  tone: { type: String, default: 'plain' }, // plain | warning | danger
})
const tones = { plain: 'text-strong', warning: 'text-warning', danger: 'text-danger' }
</script>

<template>
  <div class="flex flex-col gap-0.5 rounded-surface border border-line bg-raised px-3 py-2.5">
    <span class="text-h2 font-extrabold tabular-nums" :class="tones[tone]">{{ value }}</span>
    <span class="text-caption font-medium text-text-soft">{{ label }}</span>
    <span v-if="note" class="text-caption text-muted">{{ note }}</span>
  </div>
</template>
