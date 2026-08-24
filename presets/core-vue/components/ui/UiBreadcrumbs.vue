<script setup>
/* Путь по папкам: Все встречи → Личные → Собеседования. Нужен там, где
   вложенность реальная; на плоском экране это украшение. */
import UiIcon from './UiIcon.vue'
defineProps({ items: { type: Array, required: true } }) // [{ label, to }]
</script>

<template>
  <nav aria-label="Где я" class="flex flex-wrap items-center gap-1 text-caption">
    <template v-for="(item, i) in items" :key="i">
      <UiIcon v-if="i" name="chevron" :size="13" :stroke="2.2" class="-rotate-90 text-line-strong" />
      <RouterLink
        v-if="item.to && i < items.length - 1" :to="item.to"
        class="rounded-hair px-1 py-0.5 text-muted transition-colors hover:text-strong"
      >{{ item.label }}</RouterLink>
      <span v-else class="px-1 py-0.5 font-semibold text-strong" aria-current="page">{{ item.label }}</span>
    </template>
  </nav>
</template>
