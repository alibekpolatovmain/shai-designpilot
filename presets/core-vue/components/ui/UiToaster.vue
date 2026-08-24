<script setup>
import { useToast } from './toast.js'
import UiIcon from './UiIcon.vue'

const toast = useToast()
</script>

<template>
  <div
    class="pointer-events-none fixed bottom-4 left-1/2 z-pop flex -translate-x-1/2 flex-col items-center gap-2"
    role="status" aria-live="polite"
  >
    <TransitionGroup
      enter-active-class="transition duration-200 ease-out" leave-active-class="transition duration-150 ease-in"
      enter-from-class="translate-y-2 opacity-0" leave-to-class="translate-y-1 opacity-0"
    >
      <div
        v-for="t in toast.items" :key="t.id"
        class="pointer-events-auto flex items-center gap-2 rounded-control px-3 py-2 text-ui font-medium shadow-md"
        :class="t.tone === 'alert' ? 'bg-danger text-on-solid' : 'bg-inverse text-on-inverse'"
      >
        <UiIcon :name="t.tone === 'alert' ? 'alert' : 'check'" :size="15" :stroke="2.4" />
        {{ t.text }}
      </div>
    </TransitionGroup>
  </div>
</template>
