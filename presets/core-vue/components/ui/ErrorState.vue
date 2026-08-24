<script setup>
/* Экран ошибки. Обязан говорить три вещи: что случилось, почему это
   не вина смотрящего и что сделать дальше. «Что-то пошло не так» не
   говорит ничего из трёх. */
import UiIcon from './UiIcon.vue'
import UiButton from './UiButton.vue'

defineProps({
  code: { type: String, default: '' },
  title: { type: String, required: true },
  tone: { type: String, default: 'plain' }, // plain | danger
})
</script>

<template>
  <div class="flex flex-col items-center gap-2 rounded-panel border border-line bg-raised px-5 py-10 text-center">
    <span
      class="mb-1 grid h-12 w-12 place-items-center rounded-full"
      :class="tone === 'danger' ? 'bg-danger-soft text-danger' : 'bg-surface text-muted'"
      aria-hidden="true"
    >
      <UiIcon name="alert" :size="22" :stroke="1.8" />
    </span>
    <span v-if="code" class="font-mono text-caption text-muted">{{ code }}</span>
    <b class="text-h2 font-semibold text-strong">{{ title }}</b>
    <p class="max-w-note text-ui text-muted"><slot /></p>
    <div class="mt-2 flex flex-wrap justify-center gap-2"><slot name="action" /></div>
  </div>
</template>
