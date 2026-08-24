<script setup>
/* Число со стрелками: длительность, лимит, количество мест в команде.

   Обычное текстовое поле для числа принимает «двадцать», «20 мин» и пустоту;
   здесь значение всегда число, стрелки и колесо работают, а шаг задаётся
   один раз. */
import { NumberFieldRoot, NumberFieldInput, NumberFieldIncrement, NumberFieldDecrement } from 'reka-ui'
import UiIcon from './UiIcon.vue'

defineProps({
  modelValue: { type: Number, required: true },
  label: { type: String, required: true },
  min: { type: Number, default: 0 },
  max: { type: Number, default: Infinity },
  step: { type: Number, default: 1 },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <NumberFieldRoot
    :model-value="modelValue" :min="min" :max="max" :step="step" :aria-label="label"
    class="flex h-ctl w-32 items-center rounded-control border border-line-control bg-raised
           transition-[border-color,box-shadow] focus-within:border-accent focus-within:ring-3
           focus-within:ring-accent-quiet"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <NumberFieldDecrement
      class="press grid h-full w-8 place-items-center rounded-l-control text-muted hover:bg-surface
             hover:text-strong active:bg-surface-2 disabled:cursor-not-allowed disabled:text-line-strong"
    >
      <UiIcon name="minus" :size="15" :stroke="2.4" />
    </NumberFieldDecrement>
    <NumberFieldInput
      class="min-w-0 flex-1 border-0 bg-transparent text-center text-ui tabular-nums text-text outline-none"
    />
    <NumberFieldIncrement
      class="press grid h-full w-8 place-items-center rounded-r-control text-muted hover:bg-surface
             hover:text-strong active:bg-surface-2 disabled:cursor-not-allowed disabled:text-line-strong"
    >
      <UiIcon name="plus" :size="15" :stroke="2.4" />
    </NumberFieldIncrement>
  </NumberFieldRoot>
</template>
