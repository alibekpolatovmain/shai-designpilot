<script setup>
/* Группа взаимоисключающих переключателей: ось статуса во встречах, период
   оплаты, режим показа.

   Отличается от вкладок тем, что не переключает содержимое целиком, а
   сужает то же самое; и от радиокнопок — тем, что живёт в строке и читается
   как панель инструментов.

   Сделано на примитиве, а не своими кнопками: примитив даёт roving tabindex
   — в группу входят одним Tab, а между вариантами ходят стрелками. Своя
   версия из десяти кнопок заставляла нажимать Tab десять раз, чтобы пройти
   фильтры насквозь. */
import { ToggleGroupRoot, ToggleGroupItem } from 'reka-ui'
import UiBadge from './UiBadge.vue'

defineProps({
  modelValue: { type: String, required: true },
  items: { type: Array, required: true }, // [{ value, label, n }]
  label: { type: String, required: true },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <ToggleGroupRoot
    :model-value="modelValue" type="single" :aria-label="label"
    class="flex flex-wrap gap-1.5"
    @update:model-value="$emit('update:modelValue', $event || modelValue)"
  >
    <ToggleGroupItem
      v-for="i in items" :key="i.value" :value="i.value"
      class="press inline-flex h-ctl shrink-0 items-center gap-1.5 whitespace-nowrap rounded-control border
             px-2.5 text-ui font-medium leading-none border-line-control bg-raised text-text-soft
             hover:border-strong hover:text-strong active:bg-surface-2
             data-[state=on]:border-inverse data-[state=on]:bg-inverse data-[state=on]:text-on-inverse"
    >
      {{ i.label }}
      <span v-if="i.n !== undefined" class="tabular-nums text-caption"
            :class="modelValue === i.value ? 'text-on-inverse-soft' : 'text-muted'">{{ i.n }}</span>
    </ToggleGroupItem>
  </ToggleGroupRoot>
</template>
