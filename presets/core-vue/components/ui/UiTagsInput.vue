<script setup>
/* Ввод набора значений. Прямой сценарий продукта — корпоративный глоссарий:
   термины, аббревиатуры, названия проектов, на которые опирается
   распознавание (PRODUCT.md). Значение вводится и становится тегом. */
import { TagsInputRoot, TagsInputItem, TagsInputItemText, TagsInputItemDelete, TagsInputInput } from 'reka-ui'
import UiIcon from './UiIcon.vue'

defineProps({
  modelValue: { type: Array, default: () => [] },
  label: { type: String, required: true },
  placeholder: { type: String, default: 'Добавить и нажать Enter' },
  size: { type: String, default: 'md' }, // sm | md | lg
})
defineEmits(['update:modelValue'])
</script>

<template>
  <TagsInputRoot
    :model-value="modelValue" :aria-label="label"
    class="flex w-full flex-wrap items-center gap-1.5 rounded-control border border-line-control
           bg-raised transition-[border-color,box-shadow] focus-within:border-accent
           focus-within:ring-3 focus-within:ring-accent-quiet"
    :class="{ sm: 'min-h-ctl-sm px-1.5 py-1', md: 'min-h-ctl px-2 py-1.5',
              lg: 'min-h-ctl-lg px-2.5 py-2' }[size]"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <TagsInputItem
      v-for="tag in modelValue" :key="tag" :value="tag"
      class="flex items-center gap-1 rounded-micro bg-accent-quiet py-0.5 pl-2 pr-1 text-caption font-medium text-accent"
    >
      <TagsInputItemText />
      <TagsInputItemDelete class="grid h-4 w-4 place-items-center rounded-hair hover:bg-accent-soft">
        <UiIcon name="close" :size="11" :stroke="2.4" />
      </TagsInputItemDelete>
    </TagsInputItem>
    <TagsInputInput
      :placeholder="placeholder"
      class="min-w-32 flex-1 border-0 bg-transparent px-1 text-ui text-text outline-none placeholder:text-muted"
    />
  </TagsInputRoot>
</template>
