<script setup>
/* Страницы. Нужны там, где список длинный и в нём ищут глазами: 111 встреч.
   Кнопка «Показать ещё» уместна в ленте, но не даёт вернуться на страницу,
   где что-то было. */
import { PaginationRoot, PaginationList, PaginationListItem, PaginationFirst, PaginationPrev, PaginationNext, PaginationLast, PaginationEllipsis } from 'reka-ui'
import UiIcon from './UiIcon.vue'

defineProps({
  page: { type: Number, default: 1 },
  total: { type: Number, required: true },
  perPage: { type: Number, default: 10 },
})
defineEmits(['update:page'])

const btn = 'grid h-ctl min-w-ctl place-items-center rounded-control border border-line-control bg-raised px-2 ' +
            'text-ui font-medium text-text-soft press transition-colors hover:border-strong hover:text-strong ' +
            'disabled:cursor-not-allowed disabled:border-line disabled:text-muted'
</script>

<template>
  <PaginationRoot
    :page="page" :total="total" :items-per-page="perPage" :sibling-count="1" show-edges
    class="flex justify-center" @update:page="$emit('update:page', $event)"
  >
    <PaginationList v-slot="{ items }" class="flex items-center gap-1.5">
      <PaginationPrev :class="btn" aria-label="Предыдущая страница"><UiIcon name="back" :size="15" /></PaginationPrev>
      <template v-for="(item, i) in items" :key="i">
        <PaginationListItem
          v-if="item.type === 'page'" :value="item.value"
          :class="[btn, 'data-[selected]:border-inverse data-[selected]:bg-inverse data-[selected]:text-on-inverse']"
        >{{ item.value }}</PaginationListItem>
        <PaginationEllipsis v-else class="px-1 text-ui text-muted">…</PaginationEllipsis>
      </template>
      <PaginationNext :class="btn" aria-label="Следующая страница">
        <UiIcon name="back" :size="15" class="rotate-180" />
      </PaginationNext>
    </PaginationList>
  </PaginationRoot>
</template>
