<script setup>
/* Таблица. Нужна там, где у объектов одинаковый набор полей и их сравнивают
   по колонкам: голосовые профили, места в команде, история списаний. Встречи
   таблицей не показываются — их узнают по содержанию, а не по колонкам.

   ── Что таблица обязана уметь ────────────────────────────
   Сортировка, выделение строк, липкая шапка, загрузка, пустота, действия над
   строкой, итог, перенос в одну колонку на узком экране. Это не список
   пожеланий: ровно эти состояния перечисляют Ant Table, Primer DataTable и
   Material data table, и каждое из них — момент, в который самодельная
   таблица разваливается.

   Полос-зебры нет намеренно. Она появилась в эпоху, когда линии рисовать было
   дорого, и сегодня добавляет строкам вес, которого у них нет: строки
   разделяет волосяная линия, а подсвечивается та, на которую навели.

   Сортировка считается здесь, а не в экране: у нас данные приходят страницей
   и сравнение делает браузер. Для серверной сортировки есть `manual-sort` —
   тогда компонент только сообщает о выборе. Сравнение знает про числа, даты
   «дд.мм.гггг» и русский алфавит: `localeCompare('ru')` ставит «ё» на место,
   а `>` — нет. */
import { computed } from 'vue'
import UiIcon from './UiIcon.vue'
import UiCheckbox from './UiCheckbox.vue'
import UiSkeleton from './UiSkeleton.vue'
import UiLink from './UiLink.vue'

const props = defineProps({
  columns: { type: Array, required: true }, // { key, title, align, width, numeric, sortable }
  rows: { type: Array, required: true },
  caption: { type: String, default: '' },
  rowKey: { type: String, default: 'id' },
  /* Сортировка: { key, dir: 'asc' | 'desc' } или null */
  sort: { type: Object, default: null },
  manualSort: Boolean,
  /* Выделение: массив ключей выбранных строк */
  selected: { type: Array, default: null },
  loading: Boolean,
  /* Липкая шапка нужна там, где строк больше экрана */
  sticky: Boolean,
})
const emit = defineEmits(['update:sort', 'update:selected'])

const DATE = /^(\d{2})\.(\d{2})\.(\d{4})$/

function compare(a, b) {
  if (typeof a === 'number' && typeof b === 'number') return a - b
  const [sa, sb] = [String(a ?? ''), String(b ?? '')]
  const [da, db] = [DATE.exec(sa), DATE.exec(sb)]
  if (da && db) return `${da[3]}${da[2]}${da[1]}`.localeCompare(`${db[3]}${db[2]}${db[1]}`)
  const [na, nb] = [Number(sa.replace(',', '.')), Number(sb.replace(',', '.'))]
  if (!Number.isNaN(na) && !Number.isNaN(nb) && sa !== '' && sb !== '') return na - nb
  return sa.localeCompare(sb, 'ru')
}

const view = computed(() => {
  if (props.manualSort || !props.sort) return props.rows
  const { key, dir } = props.sort
  const sorted = [...props.rows].sort((x, y) => compare(x[key], y[key]))
  return dir === 'desc' ? sorted.reverse() : sorted
})

/* Три состояния по кругу, а не два: третье возвращает исходный порядок —
   иначе из сортировки нельзя выйти, не перезагрузив страницу. */
function toggleSort(col) {
  if (!col.sortable) return
  const cur = props.sort
  if (!cur || cur.key !== col.key) emit('update:sort', { key: col.key, dir: 'asc' })
  else if (cur.dir === 'asc') emit('update:sort', { key: col.key, dir: 'desc' })
  else emit('update:sort', null)
}
function ariaSort(col) {
  if (!col.sortable) return undefined
  if (props.sort?.key !== col.key) return 'none'
  return props.sort.dir === 'asc' ? 'ascending' : 'descending'
}
function sortIcon(col) {
  if (props.sort?.key !== col.key) return 'sort'
  return props.sort.dir === 'asc' ? 'up' : 'down'
}

const selectable = computed(() => props.selected !== null)
const keys = computed(() => view.value.map((r) => r[props.rowKey]))
const allSelected = computed(() => {
  if (!selectable.value || !keys.value.length) return false
  const n = keys.value.filter((k) => props.selected.includes(k)).length
  return n === 0 ? false : n === keys.value.length ? true : 'indeterminate'
})
function toggleAll(on) {
  emit('update:selected', on === true || on === 'indeterminate' ? [...keys.value] : [])
}
function toggleRow(key, on) {
  const next = new Set(props.selected)
  if (on) next.add(key)
  else next.delete(key)
  emit('update:selected', [...next])
}

const cols = computed(() => props.columns.length + (selectable.value ? 1 : 0) + 1)
</script>

<template>
  <div class="flex flex-col gap-2">
    <!-- Панель выделения: появляется вместе с выбором и говорит, сколько
         выбрано, — без неё человек не знает, к чему относится действие -->
    <div
      v-if="selectable && selected.length"
      class="flex flex-wrap items-center gap-3 rounded-control border border-accent-line bg-accent-quiet
             px-3 py-row"
      role="status" aria-live="polite"
    >
      <b class="text-ui font-semibold text-strong">Выбрано: {{ selected.length }}</b>
      <span class="flex flex-wrap items-center gap-2"><slot name="bulk" :selected="selected" /></span>
      <UiLink class="ml-auto" @click="emit('update:selected', [])">Снять выделение</UiLink>
    </div>

    <div
      class="table-stack overflow-x-auto rounded-surface border border-line"
      :class="sticky && 'max-h-table overflow-y-auto scrollbar-brand'"
    >
      <table class="w-full border-collapse text-ui">
        <caption v-if="caption" class="sr-only">{{ caption }}</caption>
        <thead :class="sticky && 'sticky top-0 z-sticky'">
          <tr class="border-b border-line bg-surface">
            <th v-if="selectable" scope="col" class="w-10 px-3 py-2">
              <UiCheckbox
                :model-value="allSelected" label=""
                aria-label="Выбрать все строки" @update:model-value="toggleAll"
              />
            </th>
            <th
              v-for="c in columns" :key="c.key" scope="col"
              class="px-3 py-2 text-caption font-semibold text-muted"
              :class="c.align === 'right' ? 'text-right' : 'text-left'"
              :style="c.width && { width: c.width }"
              :aria-sort="ariaSort(c)"
            >
              <button
                v-if="c.sortable" type="button"
                class="inline-flex items-center gap-1 rounded-hair text-caption font-semibold transition-colors
                       hover:text-strong"
                :class="[sort?.key === c.key ? 'text-strong' : 'text-muted',
                         c.align === 'right' && 'flex-row-reverse']"
                @click="toggleSort(c)"
              >
                {{ c.title }}
                <UiIcon :name="sortIcon(c)" :size="13" :stroke="2.2"
                        :class="sort?.key === c.key ? 'text-accent' : 'text-line-strong'" />
              </button>
              <template v-else>{{ c.title }}</template>
            </th>
            <th v-if="$slots.actions" scope="col" class="w-12 px-3 py-2"><span class="sr-only">Действия</span></th>
          </tr>
        </thead>

        <tbody>
          <!-- Загрузка сохраняет форму таблицы: строки не прыгают, когда придут данные -->
          <tr v-if="loading" v-for="n in 3" :key="`skeleton-${n}`" class="border-b border-line last:border-0">
            <td v-if="selectable" class="px-3 py-row"><UiSkeleton w="w-4" h="h-4" /></td>
            <td v-for="c in columns" :key="c.key" class="px-3 py-row">
              <UiSkeleton :w="c.align === 'right' ? 'w-10' : 'w-32'" />
            </td>
            <td v-if="$slots.actions" class="px-3 py-row"><UiSkeleton w="w-4" h="h-4" /></td>
          </tr>

          <tr v-else-if="!view.length">
            <td :colspan="cols" class="px-3 py-6 text-center text-ui text-muted">
              <slot name="empty">Пока пусто</slot>
            </td>
          </tr>

          <tr
            v-else v-for="row in view" :key="row[rowKey]"
            class="group border-b border-line transition-colors last:border-0 hover:bg-surface"
            :class="selectable && selected.includes(row[rowKey]) && 'bg-accent-quiet'"
          >
            <td v-if="selectable" class="px-3 py-row">
              <UiCheckbox
                :model-value="selected.includes(row[rowKey])"
                :aria-label="`Выбрать строку «${row[columns[0].key]}»`"
                @update:model-value="toggleRow(row[rowKey], $event)"
              />
            </td>

            <!-- Первая ячейка — заголовок строки: диктор называет её, читая
                 остальные, поэтому «24 встречи» не повисает в воздухе -->
            <component
              :is="i === 0 ? 'th' : 'td'" v-for="(c, i) in columns" :key="c.key"
              :scope="i === 0 ? 'row' : undefined" :data-label="c.title"
              class="px-3 py-row"
              :class="[
                i === 0 ? 'font-semibold text-strong' : 'font-normal text-text',
                c.align === 'right' ? 'text-right tabular-nums' : 'text-left',
                c.numeric && 'tabular-nums',
              ]"
            >
              <slot :name="c.key" :row="row">{{ row[c.key] }}</slot>
            </component>

            <td v-if="$slots.actions" class="px-3 py-row text-right">
              <span
                data-actions
                class="inline-flex opacity-0 transition-opacity duration-150 group-hover:opacity-100
                       focus-within:opacity-100 pointer-coarse:opacity-100"
              >
                <slot name="actions" :row="row" />
              </span>
            </td>
          </tr>
        </tbody>

        <!-- Итог живёт в tfoot, а не последней строкой тела: иначе он
             отсортируется вместе с данными и уедет в середину -->
        <tfoot v-if="$slots.summary">
          <tr class="border-t border-line bg-surface font-semibold text-strong">
            <slot name="summary" :rows="view" />
          </tr>
        </tfoot>
      </table>
    </div>
  </div>
</template>
