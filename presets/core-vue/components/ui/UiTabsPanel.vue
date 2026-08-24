<script setup>
/* Панель вкладки. Существует затем, чтобы у кнопки было что открывать:
   примитив связывает их через aria-controls и переводит фокус в панель по
   Tab из полоски.

   Вертикальный ритм внутри — тот же, что у страницы: панель не отдельный
   остров, а продолжение экрана. */
import { TabsContent } from 'reka-ui'

defineProps({ value: { type: String, required: true } })
</script>

<template>
  <TabsContent :value="value" class="flex flex-col gap-stack outline-none">
    <slot />
  </TabsContent>
</template>
