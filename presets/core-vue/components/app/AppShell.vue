<script setup>
/* Каркас приложения: сайдбар, рабочая область, командная палитра, тосты.

   Данные приходят пропами и только пропами. Оболочка, которая импортирует
   `data/meetings.js`, переносится в другой продукт вместе со встречами —
   и первое, что делает разработчик на новом проекте, это вырезает их
   вручную, попутно ломая палитру. */
import SideNav from './SideNav.vue'
import UiToaster from '../ui/UiToaster.vue'
import CommandPalette from './CommandPalette.vue'

defineProps({
  /* [{ to, icon, label } | { divider: true }] — разделы */
  nav: { type: Array, required: true },
  /* [{ to, title, lead }] — записи продукта для поиска в палитре */
  items: { type: Array, default: () => [] },
  itemsLabel: { type: String, default: 'Записи' },
  brand: { type: String, default: 'продукт' },
})
</script>

<template>
  <div class="min-h-screen bg-canvas frame:grid frame:grid-shell">
    <a
      href="#main"
      class="sr-only rounded-control bg-inverse px-3 py-2 text-ui font-semibold text-on-inverse
             focus:not-sr-only focus:fixed focus:left-1/2 focus:top-2 focus:z-pop focus:-translate-x-1/2"
    >К содержимому</a>
    <SideNav :nav="nav" :brand="brand" />
    <main id="main" tabindex="-1" class="flex min-w-0 flex-col outline-none"><slot /></main>
    <CommandPalette
      :sections="nav.filter((n) => !n.divider)" :items="items" :items-label="itemsLabel"
    />
    <UiToaster />
  </div>
</template>
