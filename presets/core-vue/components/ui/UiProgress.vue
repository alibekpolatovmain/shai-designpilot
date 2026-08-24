<script setup>
/* Прогресс. Определённый — загрузка файла (проценты известны).
   Неопределённый — обработка записи: время предсказать нельзя, поэтому
   вместо процента честная полоса и подпись «обычно 2–4 минуты». */
import { ProgressRoot, ProgressIndicator } from 'reka-ui'

defineProps({
  value: { type: Number, default: null }, // null — неопределённый
  label: { type: String, required: true },
})
</script>

<template>
  <div class="flex flex-col gap-1.5">
    <div class="flex items-baseline justify-between gap-3">
      <span class="text-caption text-muted">{{ label }}</span>
      <span v-if="value !== null" class="text-caption font-semibold tabular-nums text-text-soft">{{ value }}%</span>
    </div>
    <ProgressRoot
      :model-value="value" :aria-label="label"
      class="relative h-1.5 w-full overflow-hidden rounded-full bg-surface-2"
    >
      <ProgressIndicator
        v-if="value !== null"
        class="h-full rounded-full bg-accent transition-[width] duration-300"
        :style="{ width: value + '%' }"
      />
      <span v-else class="absolute inset-y-0 w-1/3 rounded-full bg-accent motion-safe:animate-slide" />
    </ProgressRoot>
  </div>
</template>
