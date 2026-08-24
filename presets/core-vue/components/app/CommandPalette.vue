<script setup>
/* Командная палитра ⌘K. При 111 встречах это самый короткий путь: набрать
   часть названия и попасть в неё, не проходя список глазами. Фильтрация,
   стрелки, Enter и typeahead — из примитива Listbox, наше только оформление.

   Появилась потому, что подсказка «⌘K» уже стояла в интерфейсе: обещание
   без функции — тот же дефект, что плашки-языки, которые не нажимаются. */
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { DialogRoot, DialogPortal, DialogOverlay, DialogContent, DialogTitle, DialogDescription,
         ListboxRoot, ListboxFilter, ListboxContent, ListboxItem, ListboxGroup, ListboxGroupLabel } from 'reka-ui'
import UiIcon from '../ui/UiIcon.vue'
import UiKbd from '../ui/UiKbd.vue'

/* Палитра ничего не знает о встречах: разделы и записи приходят пропами.

   Так она переносится в любой продукт, и — что важнее — перестаёт тянуть за
   собой данные экрана. Компонент, который импортирует `data/meetings.js`,
   переносится только вместе со встречами. */
const props = defineProps({
  /* [{ to, icon, label }] — куда можно перейти */
  sections: { type: Array, default: () => [] },
  /* [{ to, title, lead, day }] — записи продукта: встречи, документы, задачи */
  items: { type: Array, default: () => [] },
  itemsLabel: { type: String, default: 'Записи' },
})

const router = useRouter()
const open = ref(false)
const query = ref('')


const q = computed(() => query.value.trim().toLowerCase())
const foundSections = computed(() => props.sections.filter((s) => !q.value || s.label.toLowerCase().includes(q.value)))
const foundMeetings = computed(() =>
  props.items.filter((m) => !q.value || (m.title + ' ' + (m.lead || '')).toLowerCase().includes(q.value)).slice(0, 6),
)
const empty = computed(() => !foundSections.value.length && !foundMeetings.value.length)

function hotkey(e) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault()
    open.value = !open.value
  }
}
function go(to) {
  open.value = false
  router.push(to)
}
watch(open, (v) => { if (!v) query.value = '' })
onMounted(() => window.addEventListener('keydown', hotkey))
onBeforeUnmount(() => window.removeEventListener('keydown', hotkey))

defineExpose({ open })
</script>

<template>
  <DialogRoot v-model:open="open">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-pop bg-overlay backdrop-blur-xs" />
      <DialogContent
        class="fixed left-1/2 top-24 z-pop w-dialog -translate-x-1/2 overflow-hidden rounded-panel
               border border-line bg-raised shadow-lg"
      >
        <DialogTitle class="sr-only">Поиск по кабинету</DialogTitle>
        <DialogDescription class="sr-only">
          Начните вводить название встречи или раздела, стрелки — выбор, Enter — перейти
        </DialogDescription>

        <ListboxRoot :highlight-on-hover="true" class="flex flex-col">
          <div class="flex items-center gap-2 border-b border-line px-3">
            <UiIcon name="search" :size="16" class="text-muted" />
            <ListboxFilter
              v-model="query" auto-focus placeholder="Встреча или раздел"
              class="h-12 min-w-0 flex-1 border-0 bg-transparent text-doc text-text outline-none placeholder:text-muted"
            />
            <UiKbd>Esc</UiKbd>
          </div>

          <ListboxContent class="max-h-80 overflow-y-auto p-1.5 scrollbar-brand">
            <p v-if="empty" class="px-2.5 py-6 text-center text-ui text-muted">
              Ничего не нашли. Поиск идёт по разделам и по названиям встреч.
            </p>

            <ListboxGroup v-if="foundSections.length">
              <ListboxGroupLabel class="flex h-ctl-inner items-center px-2.5 text-caption font-semibold text-muted">
                Разделы
              </ListboxGroupLabel>
              <ListboxItem
                v-for="s in foundSections" :key="s.to" :value="s.to" @select="go(s.to)"
                class="flex h-ctl cursor-pointer items-center gap-2.5 rounded-control px-2.5 text-ui text-text
                       outline-none data-[highlighted]:bg-surface"
              >
                <UiIcon :name="s.icon" :size="16" class="text-muted" />{{ s.label }}
              </ListboxItem>
            </ListboxGroup>

            <ListboxGroup v-if="foundMeetings.length">
              <ListboxGroupLabel class="flex h-ctl-inner items-center px-2.5 text-caption font-semibold text-muted">
                {{ itemsLabel }}
              </ListboxGroupLabel>
              <ListboxItem
                v-for="m in foundMeetings" :key="m.id" :value="m.id" @select="go(m.to)"
                class="flex cursor-pointer flex-col gap-0.5 rounded-control px-2.5 py-1.5 outline-none
                       data-[highlighted]:bg-surface"
              >
                <span class="text-ui text-text">{{ m.title }}</span>
                <span class="truncate text-caption text-muted">{{ m.day }} · {{ m.lead }}</span>
              </ListboxItem>
            </ListboxGroup>
          </ListboxContent>

          <div class="flex items-center gap-3 border-t border-line px-3 py-2 text-caption text-muted">
            <span class="flex items-center gap-1"><UiKbd>↑</UiKbd><UiKbd>↓</UiKbd> выбор</span>
            <span class="flex items-center gap-1"><UiKbd>↵</UiKbd> перейти</span>
          </div>
        </ListboxRoot>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
