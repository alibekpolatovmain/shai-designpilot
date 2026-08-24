<script setup>
import { ContextMenuItem } from 'reka-ui'
defineProps({ danger: Boolean })
</script>

<template>
  <ContextMenuItem
    class="flex h-ctl-inner w-full cursor-pointer items-center justify-between gap-2.5 whitespace-nowrap
           rounded-control px-2.5 text-ui font-medium outline-none press transition-colors duration-150
           data-[highlighted]:bg-surface"
    :class="danger ? 'text-danger data-[highlighted]:bg-danger-soft' : 'text-text'"
  >
    <slot />
  </ContextMenuItem>
</template>
