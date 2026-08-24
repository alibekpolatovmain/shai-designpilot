<script setup>
/* Сообщение в потоке страницы: лимит записей на исходе, календарь отключился,
   тариф заканчивается. От тоста отличается тем, что не исчезает: у него есть
   причина оставаться до тех пор, пока причина не устранена. */
import UiIcon from './UiIcon.vue'

defineProps({ tone: { type: String, default: 'info' } }) // info | alert
</script>

<template>
  <div
    class="flex items-start gap-2.5 rounded-control border px-3 py-2.5"
    :class="tone === 'alert' ? 'border-danger/32 bg-danger-soft' : 'border-accent-line bg-accent-quiet'"
  >
    <UiIcon
      :name="tone === 'alert' ? 'alert' : 'info'" :size="16"
      :class="tone === 'alert' ? 'mt-0.5 text-on-danger-soft' : 'mt-0.5 text-accent'"
    />
    <span class="flex min-w-0 flex-1 flex-col gap-0.5">
      <b class="text-ui font-semibold" :class="tone === 'alert' ? 'text-on-danger-soft' : 'text-strong'"><slot name="title" /></b>
      <span class="text-caption text-text-soft"><slot /></span>
    </span>
    <span class="shrink-0"><slot name="action" /></span>
  </div>
</template>
