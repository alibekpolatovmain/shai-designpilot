<script setup>
/* Статус несёт заливку, рамку семейства и ГЛИФ: цвет не единственный канал */
import UiIcon from './UiIcon.vue'

const props = defineProps({ status: { type: String, required: true } })

const tone = {
  done: 'bg-accent-quiet text-accent border-accent-line',
  error: 'bg-danger-soft text-on-danger-soft border-danger/28',
  denied: 'bg-danger-soft text-on-danger-soft border-danger/28',
  live: 'bg-surface text-text-soft border-line-strong',
  work: 'bg-surface text-text-soft border-line-strong',
}
</script>

<template>
  <span
    class="inline-flex shrink-0 items-center gap-1.5 self-start whitespace-nowrap rounded-full border
           px-2 py-0.5 text-caption font-semibold"
    :class="tone[props.status]"
  >
<UiIcon v-if="status === 'done'" name="check" :size="13" :stroke="2.6" />
    <UiIcon v-else-if="status === 'error' || status === 'denied'" name="alert" :size="13" :stroke="2.2" />
<UiIcon v-else-if="status === 'live'" name="live" :size="13" :stroke="2"
            class="motion-safe:animate-fade-pulse" />
<UiIcon v-else name="sync" :size="13" :stroke="2.2" class="motion-safe:animate-spin-slow" />
    <slot />
  </span>
</template>
