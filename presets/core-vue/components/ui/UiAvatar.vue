<script setup>
/* Аватар: инициалы на мягкой подложке. Брендовым зелёным не заливается —
   человек не является действием (правило одного голоса). */
import { AvatarRoot, AvatarImage, AvatarFallback } from 'reka-ui'

defineProps({
  name: { type: String, required: true },
  src: { type: String, default: '' },
  size: { type: String, default: 'md' }, // sm | md | lg
})

const box = { sm: 'h-6 w-6 text-caption', md: 'h-8 w-8 text-caption', lg: 'h-11 w-11 text-ui' }
const initials = (n) => n.split(/\s+/).slice(0, 2).map((w) => w[0]).join('').toUpperCase()
</script>

<template>
  <AvatarRoot :class="['inline-flex shrink-0 overflow-hidden rounded-full bg-accent-soft', box[size]]">
    <AvatarImage v-if="src" :src="src" :alt="name" class="h-full w-full object-cover" />
    <AvatarFallback class="grid h-full w-full place-items-center font-semibold text-strong">
      {{ initials(name) }}
    </AvatarFallback>
  </AvatarRoot>
</template>
