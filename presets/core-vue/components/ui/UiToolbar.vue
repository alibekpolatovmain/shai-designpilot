<script setup>
/* Панель инструментов: ряд действий над одним объектом — шапка встречи,
   действия над выделением.

   Смысл не в оформлении, а в клавиатуре: примитив даёт roving tabindex, и
   вся панель — одна остановка Tab, внутри ходят стрелками. Ряд из шести
   отдельных кнопок стоит шести нажатий Tab, прежде чем добраться до текста
   под ним. */
import { ToolbarRoot } from 'reka-ui'

defineProps({ label: { type: String, required: true } })
</script>

<template>
  <ToolbarRoot :aria-label="label" class="flex flex-wrap items-center gap-2">
    <slot />
  </ToolbarRoot>
</template>
