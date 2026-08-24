<script setup>
/* Разделитель. С подписью — граница между смысловыми частями списка;
   без подписи — просто линия и роль presentation, чтобы диктор не читал её. */
defineProps({ label: { type: String, default: '' } })
</script>

<template>
  <div v-if="label" class="flex items-center gap-3" role="separator" :aria-label="label">
    <span class="h-px flex-1 bg-line" />
    <span class="text-caption text-muted">{{ label }}</span>
    <span class="h-px flex-1 bg-line" />
  </div>
  <hr v-else class="h-px border-0 bg-line" role="presentation" />
</template>
