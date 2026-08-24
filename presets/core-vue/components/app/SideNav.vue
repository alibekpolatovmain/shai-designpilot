<script setup>
import { ref } from 'vue'
import UiIcon from '../ui/UiIcon.vue'
import UiIconButton from '../ui/UiIconButton.vue'

import BrandMark from './BrandMark.vue'

defineProps({
  nav: { type: Array, required: true },
  brand: { type: String, default: 'продукт' },
})

const collapsed = ref(false)

</script>

<template>
  <aside
    class="flex gap-2 overflow-x-auto border-b border-line bg-rail px-2.5 py-2
           frame:sticky frame:top-0 frame:h-screen frame:flex-col frame:gap-4 frame:overflow-visible
           frame:border-r frame:border-b-0 frame:px-2 frame:py-3
           scrollbar-none"
    :class="collapsed ? 'frame:w-rail' : 'frame:w-side'"
  >
    <div class="flex shrink-0 items-center justify-between gap-2 frame:px-1">
      <RouterLink to="/today" class="flex min-h-11 items-center gap-2 frame:min-h-0" :aria-label="`${brand} — на главную`">
        <span class="grid h-7 w-7 shrink-0 place-items-center rounded-micro bg-accent text-on-solid">
          <BrandMark :size="17" />
        </span>
        <span v-if="!collapsed" class="font-display text-logo font-bold tracking-tight text-strong">{{ brand }}</span>
      </RouterLink>
      <UiIconButton
        size="sm" class="hidden frame:grid"
        :aria-expanded="!collapsed" label="Свернуть меню"
        @click="collapsed = !collapsed"
      >
        <UiIcon name="panel" />
      </UiIconButton>
    </div>

    <nav class="flex shrink-0 gap-1 frame:flex-col" aria-label="Основная навигация">
      <template v-for="(item, i) in nav" :key="i">
        <hr v-if="item.divider" class="my-2 hidden h-px border-0 bg-line frame:block" />
        <RouterLink
          v-else :to="item.to"
          active-class="bg-accent-quiet font-semibold text-accent"
          class="press flex h-ctl items-center gap-2.5 whitespace-nowrap rounded-control px-2.5 text-ui
                 font-medium text-text-soft hover:bg-surface hover:text-strong active:bg-surface-2"
          :class="collapsed && 'frame:justify-center frame:px-2.5'"
        >
          <UiIcon :name="item.icon" />
          <span v-if="!collapsed">{{ item.label }}</span>
        </RouterLink>
      </template>
    </nav>

    <div class="hidden flex-1 frame:block" />

    <!-- Низ сайдбара — продуктовый: тариф, статус, ссылка на галерею.
         В наборе это слоты, потому что у каждого продукта здесь своё, а
         зашитый «Тариф Pro» переезжает в чужой проект и живёт там месяцами. -->
    <slot name="footer" :collapsed="collapsed" />
  </aside>
</template>
