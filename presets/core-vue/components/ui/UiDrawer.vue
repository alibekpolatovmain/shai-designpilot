<script setup>
/* Выдвижная панель. На узком экране заменяет то, что на широком стоит
   колонкой: навигацию, папки, фильтры.

   Собран на примитивах диалога, а не на своём слое: ловушка фокуса, Esc,
   возврат фокуса и блокировка прокрутки фона нужны здесь ровно те же.
   Отличие только в раскладке — панель прижата к краю и во всю высоту.

   Сторона по умолчанию левая: на телефоне палец легче достаёт до края,
   с которого пришёл, а навигация в русском интерфейсе живёт слева. */
import { DialogRoot, DialogTrigger, DialogPortal, DialogOverlay, DialogContent,
         DialogTitle, DialogClose } from 'reka-ui'
import UiIcon from './UiIcon.vue'

defineProps({
  title: { type: String, required: true },
  side: { type: String, default: 'left' }, // left | right
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
        class="w-drawer fixed inset-y-0 z-pop flex flex-col gap-3 border-line bg-raised p-4 shadow-lg"
        :class="side === 'right' ? 'right-0 border-l' : 'left-0 border-r'"
      >
        <div class="flex items-center justify-between gap-3">
          <DialogTitle class="text-title font-semibold text-strong">{{ title }}</DialogTitle>
          <DialogClose
            class="press grid h-ctl-sm w-ctl-sm place-items-center rounded-control text-muted
                   hover:bg-surface hover:text-strong active:bg-surface-2"
            aria-label="Закрыть"
          >
            <UiIcon name="close" :size="16" />
          </DialogClose>
        </div>
        <div class="min-h-0 flex-1 overflow-y-auto scrollbar-brand"><slot /></div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
