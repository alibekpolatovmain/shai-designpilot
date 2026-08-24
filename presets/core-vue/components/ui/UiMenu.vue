<script setup>
/* Меню на примитивах Reka UI: ловушка фокуса, обход стрелками, Esc,
   возврат фокуса на триггер и aria-разметка приходят из примитива.
   Наше здесь — только внешний вид. */
import { DropdownMenuRoot, DropdownMenuTrigger, DropdownMenuPortal, DropdownMenuContent } from 'reka-ui'

defineProps({ align: { type: String, default: 'end' } })
</script>

<template>
  <DropdownMenuRoot>
    <DropdownMenuTrigger as-child>
      <slot name="trigger" />
    </DropdownMenuTrigger>
    <DropdownMenuPortal>
      <DropdownMenuContent
        :align="align" :side-offset="6"
        class="z-pop min-w-menu rounded-nested border border-line bg-raised p-1 shadow-lg"
      >
        <slot />
      </DropdownMenuContent>
    </DropdownMenuPortal>
  </DropdownMenuRoot>
</template>
