<script setup>
/* Раскрывающийся раздел: состав шаблона протокола («Посмотреть разделы»),
   длинные пояснения в настройках. Высота анимируется переменной примитива,
   а не измеряется скриптом — поэтому не прыгает. */
import { AccordionRoot, AccordionItem, AccordionHeader, AccordionTrigger, AccordionContent } from 'reka-ui'
import UiIcon from './UiIcon.vue'

defineProps({ items: { type: Array, required: true } }) // [{ value, title, text }]
</script>

<template>
  <AccordionRoot type="single" collapsible class="flex flex-col gap-1.5">
    <AccordionItem
      v-for="i in items" :key="i.value" :value="i.value"
      class="overflow-hidden rounded-control border border-line bg-raised"
    >
      <AccordionHeader>
        <AccordionTrigger
          class="group flex w-full items-center justify-between gap-3 px-3 py-2.5 text-left text-ui
                 font-medium text-strong transition-colors hover:bg-surface"
        >
          {{ i.title }}
          <UiIcon
            name="chevron" :size="15" :stroke="2.2"
            class="text-muted transition-transform duration-200 group-data-[state=open]:rotate-180"
          />
        </AccordionTrigger>
      </AccordionHeader>
      <AccordionContent
        class="overflow-hidden data-[state=closed]:animate-acc-up data-[state=open]:animate-acc-down"
      >
        <p class="px-3 pb-3 text-ui text-text-soft">{{ i.text }}</p>
      </AccordionContent>
    </AccordionItem>
  </AccordionRoot>
</template>
