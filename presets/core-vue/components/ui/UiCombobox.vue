<script setup>
/* Выбор из списка с поиском.

   Отличие от UiSelect простое и решающее: список короткий — выпадающий
   список, список длинный — поиск. Папок у человека три, а голосовых профилей
   и терминов глоссария бывает сотня; листать сотню стрелками — не выбор,
   а наказание.

   Правило: до семи вариантов — UiSelect, дальше — этот компонент. Семь
   потому, что список длиннее уже не охватывается взглядом целиком, и глаз
   начинает искать, а не выбирать. */
import { ComboboxRoot, ComboboxAnchor, ComboboxInput, ComboboxTrigger, ComboboxPortal,
         ComboboxContent, ComboboxViewport, ComboboxItem, ComboboxItemIndicator, ComboboxEmpty } from 'reka-ui'
import UiIcon from './UiIcon.vue'

const props = defineProps({
  modelValue: { type: [String, null], default: null },
  options: { type: Array, required: true }, // [{ value, label, note }]
  label: { type: String, required: true },
  placeholder: { type: String, default: 'Начните вводить' },
  empty: { type: String, default: 'Ничего не нашли' },
})
defineEmits(['update:modelValue'])

const nameOf = (v) => props.options.find((o) => o.value === v)?.label ?? ''
</script>

<template>
  <ComboboxRoot
    :model-value="modelValue" :aria-label="label"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <ComboboxAnchor
      class="flex h-ctl w-full items-center gap-2 rounded-control border border-line-control bg-raised px-3
             transition-[border-color,box-shadow] focus-within:border-accent focus-within:ring-3
             focus-within:ring-accent-quiet"
    >
      <UiIcon name="search" :size="17" class="text-muted" />
      <ComboboxInput
        :placeholder="placeholder" :display-value="nameOf"
        class="min-w-0 flex-1 border-0 bg-transparent text-ui text-text outline-none placeholder:text-muted"
      />
      <ComboboxTrigger class="shrink-0 text-muted">
        <UiIcon name="chevron" :size="14" :stroke="2.2" />
      </ComboboxTrigger>
    </ComboboxAnchor>

    <ComboboxPortal>
      <ComboboxContent
        position="popper" :side-offset="6"
        class="z-pop max-h-64 w-(--reka-combobox-trigger-width) overflow-y-auto rounded-nested border
               border-line bg-raised p-1 shadow-lg scrollbar-brand"
      >
        <ComboboxViewport>
          <ComboboxEmpty class="px-2.5 py-2 text-caption text-muted">{{ empty }}</ComboboxEmpty>
          <ComboboxItem
            v-for="o in options" :key="o.value" :value="o.value"
            class="press flex min-h-ctl-inner cursor-pointer items-center justify-between gap-2 rounded-control
                   px-2.5 py-1 text-ui text-text outline-none data-[highlighted]:bg-surface"
          >
            <span class="flex min-w-0 flex-col">
              <span class="truncate">{{ o.label }}</span>
              <span v-if="o.note" class="text-caption text-muted">{{ o.note }}</span>
            </span>
            <ComboboxItemIndicator class="shrink-0 text-accent">
              <UiIcon name="check" :size="14" :stroke="2.6" />
            </ComboboxItemIndicator>
          </ComboboxItem>
        </ComboboxViewport>
      </ComboboxContent>
    </ComboboxPortal>
  </ComboboxRoot>
</template>
