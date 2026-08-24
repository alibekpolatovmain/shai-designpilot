<script setup>
/* Контекстное меню по правому клику. Даёт те же действия, что и «⋮»,
   но там, где рука уже находится. Дублирование намеренное: меню-кнопка
   остаётся для тач-экранов и клавиатуры, где правого клика нет. */
import { ContextMenuRoot, ContextMenuTrigger, ContextMenuPortal, ContextMenuContent } from 'reka-ui'
</script>

<template>
  <ContextMenuRoot>
    <ContextMenuTrigger as-child><slot name="trigger" /></ContextMenuTrigger>
    <ContextMenuPortal>
      <ContextMenuContent
        class="z-pop min-w-menu rounded-nested border border-line bg-raised p-1 shadow-lg"
      >
        <slot />
      </ContextMenuContent>
    </ContextMenuPortal>
  </ContextMenuRoot>
</template>
