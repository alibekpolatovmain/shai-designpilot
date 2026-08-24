<script setup>
/* Диалог на примитиве Reka: ловушка фокуса, Esc, возврат фокуса на триггер,
   разметка aria и блокировка прокрутки фона приходят из примитива. */
import { DialogRoot, DialogTrigger, DialogPortal, DialogOverlay, DialogContent, DialogTitle, DialogDescription, DialogClose } from 'reka-ui'
import UiIcon from './UiIcon.vue'

/* Окно открывается двумя способами, и оба нужны:
     · слотом #trigger — когда рядом есть кнопка, которая его вызывает;
     · через v-model:open — когда вызов приходит из меню. Меню закрывается
       при выборе пункта и уносит с собой триггер, поэтому там окно должно
       управляться состоянием, а не жить внутри исчезающего элемента. */
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  open: { type: Boolean, default: undefined },
})
defineEmits(['update:open'])
</script>

<template>
  <DialogRoot :open="open" @update:open="$emit('update:open', $event)">
    <DialogTrigger v-if="$slots.trigger" as-child><slot name="trigger" /></DialogTrigger>
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-pop bg-overlay backdrop-blur-xs" />
      <DialogContent
        class="fixed left-1/2 top-1/2 z-pop w-dialog -translate-x-1/2 -translate-y-1/2
               rounded-panel border border-line bg-raised p-5 shadow-lg"
      >
        <!-- Заголовок нейтральный даже у разрушающего окна: красным говорит
             кнопка, и одного красного пятна на действие достаточно. Два —
             заголовок и кнопка — спорят, и глаз перестаёт понимать, где здесь
             собственно опасное место. -->
        <DialogTitle class="text-title font-semibold text-strong">{{ title }}</DialogTitle>
        <DialogDescription v-if="description" class="mt-1.5 text-ui text-muted">
          {{ description }}
        </DialogDescription>

        <div v-if="$slots.default" class="mt-4"><slot /></div>

        <div class="mt-5 flex flex-wrap justify-end gap-2">
          <DialogClose as-child><slot name="cancel" /></DialogClose>
          <slot name="confirm" />
        </div>

        <DialogClose
          class="absolute right-3 top-3 grid h-7 w-7 place-items-center rounded-micro text-muted
                 transition-colors hover:bg-surface hover:text-strong"
          aria-label="Закрыть"
        >
          <UiIcon name="close" :size="15" />
        </DialogClose>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
