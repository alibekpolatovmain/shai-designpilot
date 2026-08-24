<script setup>
/* Подтверждение разрушающего действия.

   Отличается от обычного окна не видом, а поведением: щелчок мимо и Esc его
   НЕ закрывают, фокус приходит на безопасную кнопку. Обычный диалог
   закрывается мимо-щелчком — для «Удалить встречу» это значит, что вопрос
   можно смахнуть случайным движением и не заметить, что ничего не спросили.

   Роль тоже другая — alertdialog: диктор объявляет его немедленно и целиком,
   а не как «диалог, перейдите к содержимому». */
import { AlertDialogRoot, AlertDialogTrigger, AlertDialogPortal, AlertDialogOverlay,
         AlertDialogContent, AlertDialogTitle, AlertDialogDescription,
         AlertDialogCancel, AlertDialogAction } from 'reka-ui'

defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  open: { type: Boolean, default: undefined },
})
defineEmits(['update:open'])
</script>

<template>
  <AlertDialogRoot :open="open" @update:open="$emit('update:open', $event)">
    <AlertDialogTrigger v-if="$slots.trigger" as-child><slot name="trigger" /></AlertDialogTrigger>
    <AlertDialogPortal>
      <AlertDialogOverlay class="fixed inset-0 z-pop bg-overlay backdrop-blur-xs" />
      <AlertDialogContent
        class="fixed left-1/2 top-1/2 z-pop w-dialog -translate-x-1/2 -translate-y-1/2 rounded-panel
               border border-line bg-raised p-5 shadow-lg"
      >
        <AlertDialogTitle class="text-title font-semibold text-strong">{{ title }}</AlertDialogTitle>
        <AlertDialogDescription v-if="description" class="mt-1.5 text-ui text-muted">
          {{ description }}
        </AlertDialogDescription>
        <div v-if="$slots.default" class="mt-4"><slot /></div>
        <div class="mt-5 flex flex-wrap justify-end gap-2">
          <AlertDialogCancel as-child><slot name="cancel" /></AlertDialogCancel>
          <AlertDialogAction as-child><slot name="confirm" /></AlertDialogAction>
        </div>
      </AlertDialogContent>
    </AlertDialogPortal>
  </AlertDialogRoot>
</template>
