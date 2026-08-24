<script setup>
/* Вкладки: один объект, несколько его частей — разделы профиля, части встречи.

   ── Вкладка обязана иметь панель ──────────────────────────
   Прежняя версия рисовала только полоску с кнопками, а содержимое экран
   показывал сам через `v-if`. Внешне то же самое, а по разметке — обман:
   три `role="tab"`, ноль `role="tabpanel"`, ни одного `aria-controls`.
   Диктор объявлял «вкладка 1 из 3» и не мог сказать, что она открывает; с
   клавиатуры из полоски было некуда перейти. Теперь панель — часть
   компонента, и связь между кнопкой и содержимым делает примитив.

   Если панелей нет и переключается вид одного и того же (протокол/транскрипт
   в узкой раскладке), это не вкладки, а переключатель — `UiToggleGroup`.
   Разница не в оформлении, а в том, что обещает разметка.

   ── Два начертания ────────────────────────────────────────
   `segment` — капсула с тёмным сегментом: два-три равноправных вида, стоит
   в строке рядом с другими контролами.
   `line` — подчёркивание: разделы страницы, их бывает пять и больше, полоска
   прокручивается на узком экране и не превращается в длинную капсулу. */
import { TabsRoot, TabsList, TabsTrigger } from 'reka-ui'
import UiBadge from './UiBadge.vue'
import UiIcon from './UiIcon.vue'

const props = defineProps({
  modelValue: { type: String, required: true },
  tabs: { type: Array, required: true }, // [{ value, label, n, icon, disabled }]
  variant: { type: String, default: 'segment' }, // segment | line
  grow: Boolean,
  label: { type: String, default: 'Разделы' },
})
defineEmits(['update:modelValue'])

const list = {
  segment: 'inline-flex gap-0.5 rounded-control border border-line bg-raised p-0.5',
  line: 'flex gap-4 border-b border-line',
}
const trigger = {
  segment: 'h-ctl-inner rounded-micro px-3 text-ui font-semibold text-text-soft hover:text-strong ' +
    'data-[state=active]:bg-inverse data-[state=active]:text-on-inverse',
  line: 'h-ctl border-b-2 border-transparent px-0.5 text-ui font-medium text-text-soft -mb-px ' +
    'hover:text-strong data-[state=active]:border-accent data-[state=active]:font-semibold ' +
    'data-[state=active]:text-strong',
}
</script>

<template>
  <TabsRoot
    :model-value="modelValue" class="flex min-w-0 flex-col gap-4"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <!-- Полоска прокручивается, а не переносится: перенесённая вторая строка
         вкладок читается как второй уровень навигации, которого нет -->
    <TabsList
      :aria-label="label"
      class="max-w-full overflow-x-auto scrollbar-none"
      :class="[list[props.variant], grow && 'w-full']"
    >
      <TabsTrigger
        v-for="t in tabs" :key="t.value" :value="t.value" :disabled="t.disabled"
        class="press flex shrink-0 cursor-pointer items-center gap-1.5 whitespace-nowrap leading-none
               disabled:cursor-not-allowed disabled:text-line-strong"
        :class="[trigger[props.variant], grow && 'flex-1 justify-center']"
      >
        <UiIcon v-if="t.icon" :name="t.icon" :size="15" />
        {{ t.label }}
        <UiBadge
          v-if="t.n !== undefined"
          :tone="modelValue === t.value && props.variant === 'segment' ? 'inverse' : 'quiet'" :value="t.n"
        />
      </TabsTrigger>
    </TabsList>

    <slot />
  </TabsRoot>
</template>
