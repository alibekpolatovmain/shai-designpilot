<script setup>
/* Один сворачиваемый блок — не аккордеон.

   Аккордеон управляет группой и держит правило «открыт один»; здесь блок
   один и правила нет: «показать ещё», «подробности сбоя», «служебные поля».
   Разница не в оформлении, а в разметке для диктора: у аккордеона своя
   роль группы, у одиночного блока её быть не должно. */
import { CollapsibleRoot, CollapsibleTrigger, CollapsibleContent } from 'reka-ui'
import UiIcon from './UiIcon.vue'

defineProps({ label: { type: String, required: true }, open: Boolean })
</script>

<template>
  <CollapsibleRoot :default-open="open" class="flex flex-col gap-1.5">
    <CollapsibleTrigger
      class="press group flex h-ctl-sm w-fit items-center gap-1.5 rounded-control px-2 text-caption
             font-semibold text-accent hover:bg-surface active:bg-surface-2"
    >
      {{ label }}
      <UiIcon
        name="chevron" :size="13" :stroke="2.2"
        class="transition-transform duration-200 group-data-[state=open]:rotate-180"
      />
    </CollapsibleTrigger>
    <CollapsibleContent
      class="overflow-hidden data-[state=closed]:animate-acc-up data-[state=open]:animate-acc-down"
    >
      <slot />
    </CollapsibleContent>
  </CollapsibleRoot>
</template>
