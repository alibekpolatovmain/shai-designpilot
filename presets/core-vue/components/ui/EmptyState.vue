<script setup>
import UiIcon from './UiIcon.vue'
defineProps({ icon: { type: String, default: 'search' }, title: { type: String, required: true } })
</script>

<template>
  <div class="flex flex-col items-center gap-1.5 rounded-panel border border-line bg-raised px-5 py-6
              text-center frame:py-10">
    <span class="mb-1 grid h-10 w-10 place-items-center rounded-full bg-surface text-muted" aria-hidden="true">
      <UiIcon :name="icon" :size="19" :stroke="1.6" />
    </span>
    <b class="text-ui font-semibold text-strong">{{ title }}</b>
    <p class="max-w-note text-ui text-muted"><slot name="text" /></p>
    <div class="mt-1"><slot name="action" /></div>
  </div>
</template>
