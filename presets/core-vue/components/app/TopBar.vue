<script setup>
import UiIcon from '../ui/UiIcon.vue'
import UiButton from '../ui/UiButton.vue'
import AppearanceMenu from './AppearanceMenu.vue'
defineProps({ backTo: String, backLabel: String, title: String, note: String })
</script>

<template>
  <header
    class="sticky top-0 z-header flex h-topbar shrink-0 items-center justify-between gap-4
           border-b border-line bg-canvas/85 px-4 backdrop-blur-bar frame:px-6"
  >
    <RouterLink
      v-if="backTo" :to="backTo"
      class="inline-flex items-center gap-1.5 text-ui font-semibold text-text-soft transition-colors hover:text-strong"
    >
      <UiIcon name="back" :size="16" />{{ backLabel }}
    </RouterLink>
    <h1 v-else class="flex flex-wrap items-baseline gap-2.5 text-title font-semibold tracking-title text-strong">
      {{ title }}<span v-if="note" class="text-caption font-normal tracking-normal text-muted">{{ note }}</span>
    </h1>

    <div class="flex shrink-0 items-center gap-2">
      <AppearanceMenu />
    <UiButton as="button" aria-label="Сменить язык, текущий русский">
        <UiIcon name="globe" :size="15" />Русский<UiIcon name="chevron" :size="13" :stroke="2.2" />
      </UiButton>
    </div>
  </header>
</template>
