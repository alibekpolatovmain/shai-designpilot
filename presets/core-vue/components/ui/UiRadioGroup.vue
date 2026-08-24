<script setup>
/* Выбор одного из нескольких равноправных: период оплаты (год / помесячно),
   шаблон по умолчанию. Всё видно сразу — в этом отличие от выпадающего списка. */
import { RadioGroupRoot, RadioGroupItem, RadioGroupIndicator } from 'reka-ui'

defineProps({
  modelValue: { type: String, default: '' },
  options: { type: Array, required: true }, // [{ value, label, note }]
  label: { type: String, required: true },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <RadioGroupRoot
    :model-value="modelValue" :aria-label="label" class="flex flex-col gap-1.5"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <label
      v-for="o in options" :key="o.value"
      class="flex cursor-pointer items-start gap-2.5 rounded-control border border-line px-3 py-2
             transition-colors hover:border-line-strong has-[[data-state=checked]]:border-accent
             has-[[data-state=checked]]:bg-accent-quiet"
    >
      <RadioGroupItem
        :value="o.value"
        class="mt-0.5 grid h-4 w-4 shrink-0 place-items-center rounded-full border border-line-control
               bg-raised data-[state=checked]:border-accent"
      >
        <RadioGroupIndicator class="h-2 w-2 rounded-full bg-accent" />
      </RadioGroupItem>
      <span class="flex flex-col">
        <span class="text-ui font-medium text-strong">{{ o.label }}</span>
        <span v-if="o.note" class="text-caption text-muted">{{ o.note }}</span>
      </span>
    </label>
  </RadioGroupRoot>
</template>
