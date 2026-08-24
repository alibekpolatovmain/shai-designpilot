<script setup>
/* Всплывающая панель: не меню и не подсказка.

   Меню — список действий, каждое закрывает меню. Подсказка — текст без
   интерактива. Попап нужен там, где во всплывающем слое **работают**:
   фильтр с несколькими флажками, выбор периода, форма «поделиться».
   Раньше такие места приходилось делать меню, и оно закрывалось после
   первого же щелчка по флажку. */
import { PopoverRoot, PopoverTrigger, PopoverPortal, PopoverContent, PopoverClose } from 'reka-ui'

defineProps({
  align: { type: String, default: 'start' },
  title: { type: String, default: '' },
})
</script>

<template>
  <PopoverRoot>
    <PopoverTrigger as-child><slot name="trigger" /></PopoverTrigger>
    <PopoverPortal>
      <PopoverContent
        :align="align" :side-offset="6"
        class="z-pop w-72 rounded-nested border border-line bg-raised p-3 shadow-lg"
      >
        <p v-if="title" class="mb-2 text-caption font-semibold text-muted">{{ title }}</p>
        <slot :close="PopoverClose" />
      </PopoverContent>
    </PopoverPortal>
  </PopoverRoot>
</template>
