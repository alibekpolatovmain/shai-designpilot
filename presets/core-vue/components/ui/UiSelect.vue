<script setup>
/* Выбор одного значения: язык интерфейса, папка при переносе встречи,
   тариф. Отличается от меню тем, что показывает текущее значение —
   меню только предлагает действия. */
import { SelectRoot, SelectTrigger, SelectValue, SelectIcon, SelectPortal, SelectContent, SelectViewport, SelectItem, SelectItemText, SelectItemIndicator } from 'reka-ui'
import UiIcon from './UiIcon.vue'

defineProps({
  modelValue: { type: String, default: '' },
  options: { type: Array, required: true }, // [{ value, label }]
  label: { type: String, required: true },
  placeholder: { type: String, default: 'Выберите' },
  size: { type: String, default: 'md' }, // sm | md | lg — как у поля и кнопки
})
defineEmits(['update:modelValue'])
</script>

<template>
  <SelectRoot :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)">
    <SelectTrigger
      :aria-label="label"
      class="inline-flex min-w-40 shrink-0 items-center justify-between rounded-control border
             border-line-control bg-raised text-text press hover:border-strong
             data-[placeholder]:text-muted"
      :class="{ sm: 'h-ctl-sm gap-1.5 px-2.5 text-ui', md: 'h-ctl gap-2 px-3 text-ui',
                lg: 'h-ctl-lg gap-2.5 px-4 text-doc' }[size]"
    >
      <SelectValue :placeholder="placeholder" />
      <SelectIcon><UiIcon name="chevron" :size="14" :stroke="2.2" class="text-muted" /></SelectIcon>
    </SelectTrigger>
    <SelectPortal>
      <SelectContent
        position="popper" :side-offset="6"
        class="z-pop min-w-(--reka-select-trigger-width) rounded-nested border border-line bg-raised p-1 shadow-lg"
      >
        <SelectViewport>
          <SelectItem
            v-for="o in options" :key="o.value" :value="o.value"
            class="flex h-ctl-inner cursor-pointer items-center justify-between gap-2 rounded-control px-2.5
                   text-ui text-text outline-none data-[highlighted]:bg-surface"
          >
            <SelectItemText>{{ o.label }}</SelectItemText>
            <SelectItemIndicator class="text-accent"><UiIcon name="check" :size="14" :stroke="2.6" /></SelectItemIndicator>
          </SelectItem>
        </SelectViewport>
      </SelectContent>
    </SelectPortal>
  </SelectRoot>
</template>
