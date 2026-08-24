<script setup>
/* Тумблер на примитиве: role="switch", клавиатура и aria — из Reka UI */
import { SwitchRoot, SwitchThumb } from 'reka-ui'

defineProps({ modelValue: Boolean, label: { type: String, required: true } })
defineEmits(['update:modelValue'])
</script>

<template>
  <SwitchRoot
    :model-value="modelValue" :aria-label="label"
    class="relative h-6 w-11 shrink-0 cursor-pointer rounded-full bg-line-control transition-colors
           duration-200 data-[state=checked]:bg-accent"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <SwitchThumb
      class="block h-4.5 w-4.5 translate-x-1 rounded-full bg-raised shadow-xs transition-transform
             duration-200 data-[state=checked]:translate-x-5.5"
    />
  </SwitchRoot>
</template>
