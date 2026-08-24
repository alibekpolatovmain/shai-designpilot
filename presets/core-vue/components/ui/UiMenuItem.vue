<script setup>
import { DropdownMenuItem } from 'reka-ui'
defineProps({ danger: Boolean, accent: Boolean, current: Boolean })
</script>

<template>
  <DropdownMenuItem
    class="press flex h-ctl-inner w-full cursor-pointer items-center justify-between gap-2.5
           whitespace-nowrap rounded-control px-2.5 text-ui font-medium outline-none
           data-[highlighted]:bg-surface active:bg-surface-2"
    :class="[
      danger ? 'text-danger data-[highlighted]:bg-danger-soft' : 'text-text',
      accent && 'justify-start font-semibold text-accent',
      current && 'font-semibold text-strong',
    ]"
  >
    <slot />
  </DropdownMenuItem>
</template>
