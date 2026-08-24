<script setup>
/* Дизайн-система вживую. Инвентарь текстом уже есть в скилле, но текст не
   показывает, как компонент выглядит в состоянии наведения и что контраст
   сходится. Здесь всё считается прямо в браузере из объявленных токенов —
   значит страница не может разойтись с темой. */
import { onMounted, ref, watch } from 'vue'
import AppPage from '../components/app/AppPage.vue'
import { theme, themes, density, densities } from '../design/appearance.js'
import TopBar from '../components/app/TopBar.vue'
import UiIcon from '../components/ui/UiIcon.vue'
import UiButton from '../components/ui/UiButton.vue'
import UiIconButton from '../components/ui/UiIconButton.vue'
import UiField from '../components/ui/UiField.vue'
import UiCheckbox from '../components/ui/UiCheckbox.vue'
import UiToggle from '../components/ui/UiToggle.vue'
import UiTabs from '../components/ui/UiTabs.vue'
import UiTabsPanel from '../components/ui/UiTabsPanel.vue'
import UiMenu from '../components/ui/UiMenu.vue'
import UiMenuItem from '../components/ui/UiMenuItem.vue'
import UiMenuLabel from '../components/ui/UiMenuLabel.vue'
import UiMenuSeparator from '../components/ui/UiMenuSeparator.vue'
import UiDialog from '../components/ui/UiDialog.vue'
import UiTooltip from '../components/ui/UiTooltip.vue'
import UiAvatar from '../components/ui/UiAvatar.vue'
import UiSkeleton from '../components/ui/UiSkeleton.vue'
import UiCard from '../components/ui/UiCard.vue'
import UiRow from '../components/ui/UiRow.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import StatusChip from '../components/ui/StatusChip.vue'
import TierMark from '../components/ui/TierMark.vue'
import UiTable from '../components/ui/UiTable.vue'
import UiSelect from '../components/ui/UiSelect.vue'
import UiRadioGroup from '../components/ui/UiRadioGroup.vue'
import UiBadge from '../components/ui/UiBadge.vue'
import UiToggleGroup from '../components/ui/UiToggleGroup.vue'
import UiPopover from '../components/ui/UiPopover.vue'
import UiCombobox from '../components/ui/UiCombobox.vue'
import UiSlider from '../components/ui/UiSlider.vue'
import UiCollapsible from '../components/ui/UiCollapsible.vue'
import UiPreloader from '../components/ui/UiPreloader.vue'
import UiDrawer from '../components/ui/UiDrawer.vue'
import UiAlertDialog from '../components/ui/UiAlertDialog.vue'
import UiToolbar from '../components/ui/UiToolbar.vue'
import UiNumberField from '../components/ui/UiNumberField.vue'
import UiDatePicker from '../components/ui/UiDatePicker.vue'
import UiChartBars from '../components/ui/UiChartBars.vue'
import UiChartLine from '../components/ui/UiChartLine.vue'
import UiChartDonut from '../components/ui/UiChartDonut.vue'
import UiSparkline from '../components/ui/UiSparkline.vue'
import UiMeter from '../components/ui/UiMeter.vue'
import UiAccordion from '../components/ui/UiAccordion.vue'
import UiProgress from '../components/ui/UiProgress.vue'
import UiPagination from '../components/ui/UiPagination.vue'
import UiTagsInput from '../components/ui/UiTagsInput.vue'
import UiTextarea from '../components/ui/UiTextarea.vue'
import UiBanner from '../components/ui/UiBanner.vue'
import UiFileDrop from '../components/ui/UiFileDrop.vue'
import UiBreadcrumbs from '../components/ui/UiBreadcrumbs.vue'
import UiContextMenu from '../components/ui/UiContextMenu.vue'
import UiContextMenuItem from '../components/ui/UiContextMenuItem.vue'
import FormField from '../components/ui/FormField.vue'
import UiSpinner from '../components/ui/UiSpinner.vue'
import UiDivider from '../components/ui/UiDivider.vue'
import UiKbd from '../components/ui/UiKbd.vue'
import UiStat from '../components/ui/UiStat.vue'
import ErrorState from '../components/ui/ErrorState.vue'
import AppGrid from '../components/app/AppGrid.vue'
import GridCol from '../components/app/GridCol.vue'
import GridOverlay from '../components/app/GridOverlay.vue'
import { useToast } from '../components/ui/toast.js'

const toast = useToast()
const search = ref('')
const checked = ref(true)
const on = ref(true)
const tab = ref('a')
const pane2 = ref('a')
const lang = ref('ru')
const period = ref('year')
const glossary = ref(['ВНД', 'НПА', 'ЕПК', 'Kashagan'])
const note = ref('')
const page = ref(2)
const showGrid = ref(true)
const mode = ref('all')
const folder = ref(null)
const level = ref(60)
const seats = ref(5)
const dates = ref()
const drawer = ref(false)
const confirming = ref(false)
/* Данные примеров — правдоподобные по продукту, но помечены как пример:
   в галерее нельзя показывать числа, которые кто-то примет за настоящие. */
const usage = [
  { label: 'Пн', value: 42 }, { label: 'Вт', value: 78 }, { label: 'Ср', value: 61 },
  { label: 'Чт', value: 120 }, { label: 'Пт', value: 96 }, { label: 'Сб', value: 12 }, { label: 'Вс', value: 0 },
]
const month = Array.from({ length: 30 }, (_, i) => ({
  label: `${i + 1}.08`,
  value: Math.round(40 + 60 * Math.sin(i / 3.2) ** 2 + (i % 7 === 5 || i % 7 === 6 ? -35 : 0)),
}))
const sources = [
  { label: 'Google Meet', value: 54 }, { label: 'Zoom', value: 31 },
  { label: 'Microsoft Teams', value: 18 }, { label: 'Загруженные файлы', value: 9 },
  { label: 'Запись в браузере', value: 3 },
]
const email = ref('не-почта')
const busy = ref(false)

function pretendSave() {
  busy.value = true
  setTimeout(() => { busy.value = false; toast.push('Сохранено') }, 1400)
}

/* Данные примеров — из сценариев продукта, а не выдуманные:
   голосовые профили и глоссарий существуют в кабинете, лимиты — в PRODUCT.md */
const profiles = [
  { id: 1, name: 'Айгерим Сапарова', created: '19.08.2026', meetings: 24 },
  { id: 2, name: 'Данияр Ким', created: '21.08.2026', meetings: 11 },
  { id: 3, name: 'Марат Оспанов', created: '02.09.2026', meetings: 7 },
]
const tableCols = [
  { key: 'name', title: 'Имя и фамилия', sortable: true },
  { key: 'created', title: 'Дата создания', width: '11rem', sortable: true },
  { key: 'meetings', title: 'Встреч', align: 'right', width: '7rem', sortable: true },
]
const sort = ref({ key: 'meetings', dir: 'desc' })
const picked = ref([])
const tableLoading = ref(false)

/* Роли — единственное, чем пользуются компоненты. Слева то, что несёт текст
   или кромку (для них считается контраст), справа — сами поверхности. */
const inkRoles = [
  ['strong', 'заголовок, метка'], ['text', 'основной текст'], ['text-soft', 'вторичный'],
  ['muted', 'подписи'], ['accent', 'действие и акцент'], ['danger', 'сбой'],
  ['warning', 'на исходе'], ['line-control', 'кромка контрола'], ['line-strong', 'граница'],
  ['line', 'волосяная линия'],
]
const surfaceRoles = [
  ['rail', 'сайдбар'], ['canvas', 'грунт'], ['raised', 'карточка, панель'],
  ['surface', 'тихая заливка'], ['surface-2', 'заливка поглубже'],
  ['inverse', 'плашка наоборот'], ['accent', 'заливка действия'],
  ['accent-quiet', 'тихий акцент'], ['danger-soft', 'подложка сбоя'],
  ['warning-soft', 'подложка предупреждения'],
]
const typeRoles = [
  ['caption', 'Метаданные, счётчики, подписи'],
  ['ui', 'Основной кегль интерфейса'],
  ['doc', 'То, что читают подряд'],
  ['title', 'Заголовок секции'],
  ['h2', 'Подзаголовок'],
  ['h1', 'Имя встречи'],
]
const radii = ['hair', 'micro', 'control', 'nested', 'surface', 'panel', 'hero']
const shadows = ['xs', 'sm', 'md', 'lg']
const steps = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12]

const surfaces = ref([])
const roles = ref([])
const ground = ref('')
const types = ref([])
const radiusPx = ref({})

/* Контраст считается по WCAG из вычисленного значения токена, а не берётся
   из документации: так число не может устареть вслед за палитрой. */
function luminance(rgb) {
  const [r, g, b] = rgb.map((v) => {
    const s = v / 255
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}
/* Цвет из вычисленного стиля приходит в двух записях — rgba(255, 255, 255, 0.4)
   и color(srgb 1 1 1 / 0.4), — и в тёмной теме половина ролей полупрозрачна.
   Без учёта альфы линия считалась чистым белым и показывала 17:1 вместо 1.4:1:
   ровно то враньё, ради борьбы с которым эта страница и считает сама. */
function parse(value, bg) {
  const nums = (value.match(/[\d.]+/g) || []).map(Number)
  if (!nums.length) return [255, 255, 255]
  const srgb = value.includes('color(srgb')
  const rgb = nums.slice(0, 3).map((v) => (srgb ? v * 255 : v))
  const alpha = nums.length > 3 ? nums[3] : 1
  if (alpha >= 1 || !bg) return rgb
  return rgb.map((v, i) => v * alpha + bg[i] * (1 - alpha))
}

/* Контраст считается к текущей поверхности, а не к белому: в тёмной теме
   белый грунт — выдумка, и число рядом со свотчем стало бы враньём.
   Пересчитывается при смене темы, поэтому страница честна в обеих. */
function measureAll() {
  const cs = getComputedStyle(document.documentElement)
  const probe = document.createElement('span')
  document.body.appendChild(probe)

  const value = (name) => {
    probe.style.color = `var(--color-${name})`
    return getComputedStyle(probe).color
  }
  probe.style.color = 'var(--color-raised)'
  const bg = parse(getComputedStyle(probe).color)  /* сама панель непрозрачна */
  ground.value = getComputedStyle(probe).color

  const ratioTo = (rgb) => {
    const a = luminance(rgb.slice(0, 3)); const b = luminance(bg)
    return ((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(2)
  }
  roles.value = inkRoles.map(([name, use]) => ({ name, use, ratio: ratioTo(parse(value(name), bg)) }))
  surfaces.value = surfaceRoles.map(([name, use]) => ({ name, use, hex: value(name) }))

  types.value = typeRoles.map(([role, use]) => {
    probe.className = `text-${role}`
    const c = getComputedStyle(probe)
    return { role, use, size: c.fontSize, line: c.lineHeight }
  })
  probe.className = ''

  radiusPx.value = Object.fromEntries(radii.map((r) => [r, cs.getPropertyValue(`--radius-${r}`).trim()]))
  probe.remove()
}

onMounted(measureAll)
watch(theme, () => requestAnimationFrame(measureAll))
onMounted(() => {
  const mq = window.matchMedia('(prefers-color-scheme: dark)')
  mq.addEventListener('change', () => requestAnimationFrame(measureAll))
})
</script>

<template>
  <TopBar title="Дизайн-система" note="токены и компоненты кабинета" />

  <AppPage gap="gap-8">
    <p class="-mt-1 max-w-page text-ui text-text-soft">
      Всё на этой странице читается из темы в момент открытия: контраст считается по WCAG из
      вычисленного цвета, кегли и радиусы берутся у браузера. Поэтому страница не может
      разойтись с системой — если токен изменится, изменится и она.
    </p>

    <!-- ── Цвет ─────────────────────────────────────────────── -->
    <section>
      <h2 class="mb-1 text-title font-semibold text-strong">
        Цвет<span class="ml-2 text-caption font-normal text-muted">две ступени: палитра объявляет роли, разметка знает только роли</span>
      </h2>
      <p class="mb-3 max-w-page text-caption text-muted">
        Контраст посчитан к текущей поверхности ({{ ground }}) и пересчитывается при смене темы:
        число рядом со свотчем верно ровно для того, что сейчас на экране.
        Литералов палитры (`--p-*`) в разметке нет — такого класса не существует.
      </p>

      <p class="mb-2 text-caption font-semibold text-text-soft">Что несёт текст и кромку</p>
      <div class="mb-4 grid gap-2 one:grid-cols-2 split:grid-cols-3">
        <div v-for="c in roles" :key="c.name" class="flex items-center gap-2.5 rounded-surface border border-line p-2">
          <span class="grid h-8 w-8 shrink-0 place-items-center rounded-micro border border-line bg-raised
                       text-ui font-bold" :style="{ color: `var(--color-${c.name})` }">A</span>
          <span class="flex min-w-0 flex-col">
            <b class="truncate text-caption font-semibold text-strong">{{ c.name }}</b>
            <span class="truncate text-caption text-muted">{{ c.use }} · <span class="tabular-nums">{{ c.ratio }}:1</span></span>
          </span>
        </div>
      </div>

      <p class="mb-2 text-caption font-semibold text-text-soft">Поверхности</p>
      <div class="grid gap-2 one:grid-cols-2 split:grid-cols-3">
        <div v-for="c in surfaces" :key="c.name" class="flex items-center gap-2.5 rounded-surface border border-line p-2">
          <span class="h-8 w-8 shrink-0 rounded-micro border border-line" :style="{ background: `var(--color-${c.name})` }" />
          <span class="flex min-w-0 flex-col">
            <b class="truncate text-caption font-semibold text-strong">{{ c.name }}</b>
            <span class="truncate text-caption text-muted">{{ c.use }}</span>
          </span>
        </div>
      </div>
    </section>

    <!-- ── Тема и плотность ─────────────────────────────────── -->
    <section>
      <h2 class="mb-1 text-title font-semibold text-strong">
        Тема и плотность<span class="ml-2 text-caption font-normal text-muted">два атрибута на корне, а не два набора классов</span>
      </h2>
      <p class="mb-3 max-w-page text-caption text-muted">
        Тему несёт `color-scheme`, плотность — четыре числа метрики. Компоненты о теме не знают:
        они ссылаются на роли, роли — на палитру, а палитра объявлена через `light-dark()`.
      </p>
      <div class="grid gap-4 split:grid-cols-2">
        <UiRadioGroup v-model="theme" :options="themes" label="Тема интерфейса" />
        <UiRadioGroup v-model="density" :options="densities" label="Плотность интерфейса" />
      </div>
    </section>

    <!-- ── Плавающие слои и выбор ───────────────────────────── -->
    <section>
      <h2 class="mb-1 text-title font-semibold text-strong">
        Слои и выбор<span class="ml-2 text-caption font-normal text-muted">четыре разных ответа на «показать поверх»</span>
      </h2>
      <p class="mb-3 max-w-page text-caption text-muted">
        Меню — список действий, каждое закрывает меню. Попап — панель, в которой работают
        (фильтр с флажками, форма). Подсказка — текст без интерактива. Диалог — то, без чего
        действие не продолжится. Перепутать их легко, и тогда фильтр с флажками закрывается
        после первого же щелчка.
      </p>
      <div class="flex flex-wrap items-center gap-3">
        <UiToggleGroup
          v-model="mode" label="Пример группы переключателей"
          :items="[{ value: 'all', label: 'Все', n: 10 }, { value: 'new', label: 'Не открыто', n: 3 },
                   { value: 'fail', label: 'Сорвалось', n: 2 }]"
        />
        <UiPopover title="Показывать">
          <template #trigger>
            <UiButton size="sm">Источник<UiIcon name="chevron" :size="13" :stroke="2.2" /></UiButton>
          </template>
          <div class="flex flex-col gap-0.5">
            <UiCheckbox v-model="checked" label="Онлайн-встречи" />
            <UiCheckbox v-model="on" label="Загруженные файлы" />
          </div>
        </UiPopover>
        <span class="flex items-center gap-2 text-caption text-muted">
          Счётчик <UiBadge :value="12" /> <UiBadge tone="accent" :value="3" /> <UiBadge tone="danger" :value="2" />
        </span>
      </div>

      <div class="mt-3 grid gap-4 split:grid-cols-2">
        <span class="flex flex-col gap-1.5">
          <span class="text-caption text-muted">выбор с поиском — от восьми вариантов и дальше</span>
          <UiCombobox
            v-model="folder" label="Куда перенести" placeholder="Найти папку"
            :options="[{ value: 'l', label: 'Личные', note: '2' }, { value: 'p', label: 'Планёрки', note: '3' },
                       { value: 'n', label: 'Найм', note: '2' }]"
          />
        </span>
        <span class="flex flex-col gap-1.5">
          <span class="text-caption text-muted">ползунок — громкость, скорость, порог</span>
          <UiSlider v-model="level" label="Пример ползунка" />
        </span>
      </div>

      <UiCollapsible label="Показать служебные поля" class="mt-3">
        <p class="max-w-note text-caption text-muted">
          Один сворачиваемый блок — не аккордеон: у аккордеона своя роль группы и правило
          «открыт один», здесь блок один и правила нет.
        </p>
      </UiCollapsible>
    </section>

    <!-- ── Ожидание ─────────────────────────────────────────── -->
    <section>
      <h2 class="mb-1 text-title font-semibold text-strong">
        Ожидание<span class="ml-2 text-caption font-normal text-muted">прелоадер продукта, а не крутилка вообще</span>
      </h2>
      <p class="mb-3 max-w-page text-caption text-muted">
        Крутилка одинакова у всех и не говорит ничего. Здесь ждут не «загрузки», а превращения
        голоса в текст: столбики качаются как звук, и по ряду слева направо идёт волна цвета —
        распознавание движется по записи. Те же столбики рисуют запись на экране встречи.
      </p>
      <div class="flex flex-wrap items-end gap-8 rounded-surface border border-line bg-raised p-5">
        <UiPreloader size="sm" inline />
        <UiPreloader label="Расшифровываем" />
        <UiPreloader size="lg" label="Собираем протокол" />
        <span class="flex items-center gap-2 text-caption text-muted">
          для короткого ожидания без смысла<UiSpinner :size="16" />
        </span>
      </div>
    </section>

    <!-- ── Ещё компоненты ───────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">
        Период, число, ящик<span class="ml-2 text-caption font-normal text-muted">то, без чего экраны обходились вручную</span>
      </h2>
      <div class="flex flex-wrap items-start gap-4">
        <span class="flex flex-col gap-1.5">
          <span class="text-caption text-muted">период — неделя начинается с понедельника</span>
          <UiDatePicker v-model="dates" label="Период" />
        </span>
        <span class="flex flex-col gap-1.5">
          <span class="text-caption text-muted">число со стрелками</span>
          <UiNumberField v-model="seats" label="Мест в команде" :min="1" :max="50" />
        </span>
        <span class="flex flex-col gap-1.5">
          <span class="text-caption text-muted">выдвижная панель — узкий экран</span>
          <UiButton size="sm" @click="drawer = true">Открыть ящик</UiButton>
        </span>
        <span class="flex flex-col gap-1.5">
          <span class="text-caption text-muted">подтверждение: мимо-щелчок не закрывает</span>
          <UiButton size="sm" variant="danger" @click="confirming = true">Удалить</UiButton>
        </span>
      </div>

      <div class="mt-4 flex flex-col gap-1.5">
        <span class="text-caption text-muted">панель инструментов — одна остановка Tab, внутри стрелки</span>
        <UiToolbar label="Пример панели">
          <UiButton size="sm"><UiIcon name="download" :size="15" />Экспорт</UiButton>
          <UiButton size="sm">Сменить шаблон</UiButton>
          <UiIconButton size="sm" label="Скопировать протокол"><UiIcon name="copy" :size="15" /></UiIconButton>
          <UiIconButton size="sm" label="Ещё действия"><UiIcon name="more" :size="15" /></UiIconButton>
        </UiToolbar>
      </div>



      <UiDrawer v-model:open="drawer" title="Папки">
        <p class="text-ui text-text-soft">
          На узком экране сюда уезжает то, что на широком стоит колонкой: навигация, папки, фильтры.
        </p>
      </UiDrawer>

      <UiAlertDialog
        v-model:open="confirming" title="Удалить встречу?"
        description="Запись и протокол исчезнут навсегда. Щелчок мимо окна его не закроет — на такой вопрос отвечают, а не отмахиваются."
      >
        <template #cancel><UiButton>Оставить</UiButton></template>
        <template #confirm><UiButton variant="danger" @click="toast.push('Пример: удалено', 'alert')">Удалить</UiButton></template>
      </UiAlertDialog>
    </section>

    <!-- ── Вкладки ──────────────────────────────────────────── -->
    <section>
      <h2 class="mb-1 text-title font-semibold text-strong">
        Вкладки<span class="ml-2 text-caption font-normal text-muted">два начертания и одно условие</span>
      </h2>
      <p class="mb-3 max-w-page text-caption text-muted">
        Условие простое: у вкладки обязана быть панель. Полоска кнопок без панелей — не вкладки,
        а переключатель вида: там нужен `UiToggleGroup`, иначе разметка обещает связь, которой нет.
        Капсула — два-три равноправных вида в строке; подчёркивание — разделы страницы, их бывает
        пять и больше, и полоска прокручивается вместо переноса на вторую строку.
      </p>
      <div class="flex flex-col gap-5">
        <UiTabs v-model="tab" label="Пример: капсула"
                :tabs="[{ value: 'a', label: 'Протокол' }, { value: 'b', label: 'Транскрипт', n: 11 }]">
          <UiTabsPanel value="a">
            <p class="text-ui text-text-soft">Панель существует и связана с кнопкой — это и делает вкладки вкладками.</p>
          </UiTabsPanel>
          <UiTabsPanel value="b">
            <p class="text-ui text-text-soft">Со счётчиком: число живёт в самой вкладке, а не в заголовке рядом.</p>
          </UiTabsPanel>
        </UiTabs>

        <UiTabs v-model="pane2" variant="line" label="Пример: подчёркивание"
                :tabs="[{ value: 'a', label: 'Обзор', icon: 'grid' }, { value: 'b', label: 'Участники', n: 4 },
                        { value: 'c', label: 'Решения', n: 3 }, { value: 'd', label: 'Файлы' },
                        { value: 'e', label: 'История', disabled: true }]">
          <UiTabsPanel value="a">
            <p class="text-ui text-text-soft">
              Подчёркивание для разделов страницы: иконка и счётчик поддерживаются, выключенная
              вкладка не берёт фокус.
            </p>
          </UiTabsPanel>
          <UiTabsPanel v-for="v in ['b', 'c', 'd', 'e']" :key="v" :value="v">
            <p class="text-ui text-text-soft">Раздел «{{ v }}».</p>
          </UiTabsPanel>
        </UiTabs>
      </div>
    </section>

    <!-- ── Графики ──────────────────────────────────────────── -->
    <section>
      <h2 class="mb-1 text-title font-semibold text-strong">
        Графики<span class="ml-2 text-caption font-normal text-muted">четыре типа и одно правило на всех</span>
      </h2>
      <p class="mb-3 max-w-page text-caption text-muted">
        Основание всегда ноль, шкала одна на дашборд, у каждого графика под столбиками стоит
        настоящая таблица для тех, кто форму не видит. Тип выбирается не по вкусу: столбики
        сравнивают периоды поштучно, ломаная показывает ход, кольцо — доли целого, спарклайн
        стоит рядом с числом и не претендует на самостоятельность.
      </p>

      <div class="grid gap-6 split:grid-cols-2">
        <UiChartBars :points="usage" caption="Расход по дням недели" unit=" мин" />
        <UiChartLine :points="month" caption="Расход за месяц" unit=" мин" />
        <UiChartDonut :points="sources" caption="Откуда приходят встречи" unit="встреч" />
        <div class="flex flex-col justify-center gap-5">
          <UiMeter :value="760" :max="1000" label="Минуты в этом месяце" unit=" мин" />
          <UiMeter :value="940" :max="1000" label="Пример: остаток на исходе" unit=" мин" />
          <UiMeter :value="1000" :max="1000" label="Пример: лимит исчерпан" unit=" мин" />
          <span class="flex items-center gap-3 text-ui text-text">
            Встреч за неделю <b class="tabular-nums text-strong">28</b>
            <UiSparkline :values="[12, 18, 15, 22, 19, 26, 28]" label="Встречи за неделю" />
          </span>
        </div>
      </div>
    </section>

    <!-- ── Кегли ────────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Кегли<span class="ml-2 text-caption font-normal text-muted">интерлиньяж объявлен рядом с размером</span></h2>
      <div class="flex flex-col gap-2">
        <div v-for="t in types" :key="t.role" class="flex flex-wrap items-baseline gap-3 rounded-surface border border-line px-3 py-2.5">
          <span :class="`text-${t.role} text-strong`">Съешь ещё этих мягких булок</span>
          <span class="ml-auto shrink-0 text-caption tabular-nums text-muted">
            text-{{ t.role }} · {{ t.size }}/{{ t.line }} · {{ t.use }}
          </span>
        </div>
      </div>
    </section>

    <!-- ── Форма и глубина ──────────────────────────────────── -->
    <section class="grid gap-6 split:grid-cols-2">
      <div>
        <h2 class="mb-3 text-title font-semibold text-strong">Радиусы</h2>
        <div class="flex flex-wrap gap-2">
          <div v-for="r in radii" :key="r" class="flex flex-col items-center gap-1">
            <span class="h-14 w-14 border border-line-control bg-surface" :style="{ borderRadius: `var(--radius-${r})` }" />
            <span class="text-caption text-muted">{{ r }} {{ radiusPx[r] }}</span>
          </div>
        </div>
      </div>
      <div>
        <h2 class="mb-3 text-title font-semibold text-strong">Тени</h2>
        <div class="flex flex-wrap gap-3">
          <div v-for="sh in shadows" :key="sh" class="flex flex-col items-center gap-1.5">
            <span class="h-14 w-14 rounded-surface bg-raised" :style="{ boxShadow: `var(--shadow-${sh})` }" />
            <span class="text-caption text-muted">{{ sh }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Ритм ─────────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Ритм<span class="ml-2 text-caption font-normal text-muted">ступени 2…48px, всё кратно 4 кроме двух мелких</span></h2>
      <div class="flex flex-wrap items-end gap-2">
        <div v-for="s in steps" :key="s" class="flex flex-col items-center gap-1">
          <span class="bg-accent-line" :style="{ width: `calc(${s} * 0.25rem)`, height: `calc(${s} * 0.25rem)` }" />
          <span class="text-caption tabular-nums text-muted">{{ s * 4 }}</span>
        </div>
      </div>
    </section>

    <!-- ── Контролы ─────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Контролы<span class="ml-2 text-caption font-normal text-muted">три размера: 28 / 36 / 44px, на тач 36 / 44 / 48</span></h2>
      <UiCard>
        <div class="flex flex-wrap items-center gap-2">
          <UiButton variant="primary">Основное действие</UiButton>
          <UiButton variant="dark">Тёмное</UiButton>
          <UiButton>Обычное</UiButton>
          <UiButton small>Компактное</UiButton>
          <UiButton variant="primary" as="button" disabled>Выключено</UiButton>
          <UiTooltip text="Иконочная кнопка без подписи">
            <UiIconButton label="Действия">
              <svg viewBox="0 0 24 24" fill="currentColor" class="h-4 w-4" aria-hidden="true">
                <circle cx="12" cy="5" r="1.7" /><circle cx="12" cy="12" r="1.7" /><circle cx="12" cy="19" r="1.7" />
              </svg>
            </UiIconButton>
          </UiTooltip>
        </div>

        <div class="mt-3 flex flex-wrap items-end gap-3 border-t border-line pt-3">
          <span class="flex flex-col gap-1.5">
            <span class="text-caption text-muted">sm — внутри строк и таблиц</span>
            <span class="flex flex-wrap items-center gap-2">
              <UiButton variant="primary" size="sm">Действие</UiButton>
              <UiButton size="sm">Обычная</UiButton>
              <UiIconButton label="sm" size="sm"><UiIcon name="copy" /></UiIconButton>
              <UiField size="sm" label="Поле sm" placeholder="Поле" class="basis-40" />
              <UiSelect size="sm" :options="[{ value: 'a', label: 'Выбор' }]" model-value="a" label="Пример sm" />
            </span>
          </span>
          <span class="flex flex-col gap-1.5">
            <span class="text-caption text-muted">md — по умолчанию</span>
            <span class="flex flex-wrap items-center gap-2">
              <UiButton variant="primary">Действие</UiButton>
              <UiButton>Обычная</UiButton>
              <UiIconButton label="md"><UiIcon name="copy" /></UiIconButton>
              <UiField label="Поле md" placeholder="Поле" class="basis-40" />
              <UiSelect :options="[{ value: 'a', label: 'Выбор' }]" model-value="a" label="Пример md" />
            </span>
          </span>
          <span class="flex flex-col gap-1.5">
            <span class="text-caption text-muted">lg — единственное действие на экране</span>
            <span class="flex flex-wrap items-center gap-2">
              <UiButton variant="primary" size="lg">Действие</UiButton>
              <UiButton size="lg">Обычная</UiButton>
              <UiIconButton label="lg" size="lg"><UiIcon name="copy" /></UiIconButton>
              <UiField size="lg" label="Поле lg" placeholder="Поле" class="basis-40" />
              <UiSelect size="lg" :options="[{ value: 'a', label: 'Выбор' }]" model-value="a" label="Пример lg" />
            </span>
          </span>
        </div>

        <div class="mt-4 flex flex-col gap-1.5">
          <span class="text-caption text-muted">пять вариантов: заливка, тихая заливка, кромка, прозрачная, разрушающее</span>
          <span class="flex flex-wrap items-center gap-2">
            <UiButton variant="primary">Подключить</UiButton>
            <UiButton>Загрузить файл</UiButton>
            <UiButton variant="outline">На чужом фоне</UiButton>
            <UiButton variant="ghost">Тихая</UiButton>
            <UiButton variant="danger">Удалить</UiButton>
            <UiButton variant="link">Показать ещё</UiButton>
          </span>
        </div>

        <div class="mt-3 flex flex-wrap items-center gap-3">
          <UiField v-model="search" icon="search" label="Поиск" placeholder="Поиск" class="basis-60" />
          <UiTabs
            v-model="tab" label="Пример вкладок"
            :tabs="[{ value: 'a', label: 'Первая' }, { value: 'b', label: 'Вторая' }]"
          />
          <UiCheckbox v-model="checked" label="Чекбокс" />
          <span class="inline-flex items-center gap-2 text-ui text-text">
            Тумблер <UiToggle v-model="on" label="Пример тумблера" />
          </span>
        </div>

        <div class="mt-3 flex flex-wrap items-center gap-2">
          <UiMenu>
            <template #trigger><UiButton small>Меню<UiIcon name="chevron" :size="13" :stroke="2.2" /></UiButton></template>
            <UiMenuLabel>Раздел</UiMenuLabel>
            <UiMenuItem current>Текущий пункт<span class="text-caption text-muted">✓</span></UiMenuItem>
            <UiMenuItem>Обычный пункт</UiMenuItem>
            <UiMenuSeparator />
            <UiMenuItem danger>Опасное действие</UiMenuItem>
          </UiMenu>

          <UiDialog
            title="Удалить встречу?"
            description="Запись, транскрипт и протокол будут удалены без возможности вернуть."
          >
            <template #trigger><UiButton small>Диалог</UiButton></template>
            <template #cancel><UiButton small>Оставить</UiButton></template>
            <template #confirm>
              <UiButton variant="danger" small @click="toast.push('Пример: удалено', 'alert')">Удалить</UiButton>
            </template>
          </UiDialog>

          <UiButton small @click="toast.push('Скопировано')">Показать тост</UiButton>
        </div>
      </UiCard>
    </section>

    <!-- ── Меню ─────────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">
        Меню<span class="ml-2 text-caption font-normal text-muted">три вида, и у каждого своя причина существовать</span>
      </h2>
      <UiCard>
        <div class="flex flex-wrap items-start gap-6">
          <div class="flex flex-col gap-2">
            <span class="text-caption text-muted">выпадающее — действия над объектом</span>
            <UiMenu>
              <template #trigger><UiButton size="sm">Действия<UiIcon name="chevron" :size="13" :stroke="2.2" /></UiButton></template>
              <UiMenuLabel>Встреча</UiMenuLabel>
              <UiMenuItem>Переименовать</UiMenuItem>
              <UiMenuItem>Добавить в папку</UiMenuItem>
              <UiMenuSeparator />
              <UiMenuItem danger>Удалить</UiMenuItem>
            </UiMenu>
          </div>

          <div class="flex flex-col gap-2">
            <span class="text-caption text-muted">контекстное — правый клик по строке</span>
            <UiContextMenu>
              <template #trigger>
                <div class="cursor-context-menu rounded-surface border border-line px-3 py-2 text-ui text-text-soft">
                  Нажмите правой кнопкой
                </div>
              </template>
              <UiContextMenuItem>Открыть</UiContextMenuItem>
              <UiContextMenuItem>Переименовать</UiContextMenuItem>
              <UiContextMenuItem danger>Удалить встречу</UiContextMenuItem>
            </UiContextMenu>
          </div>

          <div class="flex flex-col gap-2">
            <span class="text-caption text-muted">командная палитра — переход и поиск</span>
            <span class="flex items-center gap-2 text-ui text-text-soft">
              <UiKbd>⌘</UiKbd><UiKbd>K</UiKbd> в любом месте кабинета
            </span>
          </div>
        </div>
      </UiCard>
    </section>

    <!-- ── Статусы и метки ──────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Статусы и метки<span class="ml-2 text-caption font-normal text-muted">заливка, рамка семейства и глиф — цвет не единственный канал</span></h2>
      <UiCard>
        <div class="flex flex-wrap items-center gap-2">
          <StatusChip status="done">Готово</StatusChip>
          <StatusChip status="live">Пишется</StatusChip>
          <StatusChip status="work">Обработка</StatusChip>
          <StatusChip status="error">Сбой</StatusChip>
          <StatusChip status="denied">Не пустили</StatusChip>
          <TierMark>Enterprise</TierMark>
          <TierMark base>на всех тарифах</TierMark>
          <UiAvatar name="Айгерим Сапарова" size="sm" />
          <UiAvatar name="Данияр" />
          <UiAvatar name="Марат Ким" size="lg" />
        </div>
      </UiCard>
    </section>

    <!-- ── Сетка ────────────────────────────────────────────── -->
    <section>
      <div class="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-title font-semibold text-strong">
          Сетка<span class="ml-2 text-caption font-normal text-muted">4 / 8 / 12 колонок по брейкпоинтам, желоб 16 и 24</span>
        </h2>
        <UiCheckbox v-model="showGrid" label="Показать колонки" />
      </div>
      <UiCard>
        <p class="mb-3 max-w-measure text-ui text-text-soft">
          Колонок меняется по размеру экрана, как в Material 3: до 641px — четыре, до 900 — восемь,
          дальше двенадцать. Классов вида <code class="text-danger">col-md-6</code> нет: колонку задаёт
          CSS Grid, а сетка нужна, чтобы карточки, колонки встречи и поля форм стояли на одних линиях.
        </p>
        <div class="relative">
          <GridOverlay :show="showGrid" />
          <AppGrid>
            <GridCol :span="4" :one="8" :frame="8">
              <div class="rounded-surface border border-line bg-surface px-3 py-4 text-caption text-muted">
                Протокол — 8 из 12
              </div>
            </GridCol>
            <GridCol :span="4" :one="8" :frame="4">
              <div class="rounded-surface border border-line bg-surface px-3 py-4 text-caption text-muted">
                Транскрипт — 4
              </div>
            </GridCol>
            <GridCol v-for="i in 3" :key="i" :span="4" :one="4" :frame="4">
              <div class="rounded-surface border border-line bg-surface px-3 py-4 text-caption text-muted">
                Карточка — 4
              </div>
            </GridCol>
          </AppGrid>
        </div>
      </UiCard>
    </section>

    <!-- ── Данные ───────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Данные<span class="ml-2 text-caption font-normal text-muted">таблица — там, где объекты сравнивают по колонкам</span></h2>
      <div class="flex flex-col gap-3">
        <UiTable
          v-model:sort="sort" v-model:selected="picked"
          caption="Голосовые профили" :columns="tableCols" :rows="profiles" :loading="tableLoading"
        >
          <template #bulk>
            <UiButton size="sm" @click="toast.push(`Пример: объединили ${picked.length}`)">Объединить</UiButton>
            <UiButton size="sm" variant="danger" @click="picked = []">Удалить</UiButton>
          </template>
          <template #actions="{ row }">
            <UiIconButton size="sm" :label="`Действия с профилем «${row.name}»`">
              <UiIcon name="more" :size="16" />
            </UiIconButton>
          </template>
          <template #summary>
            <td class="px-3 py-row" :colspan="3">Всего профилей: {{ profiles.length }}</td>
            <td class="px-3 py-row text-right tabular-nums">{{ profiles.reduce((n, p) => n + p.meetings, 0) }}</td>
            <td />
          </template>
        </UiTable>

        <div class="flex flex-wrap items-center gap-2">
          <UiButton size="sm" @click="tableLoading = !tableLoading">
            {{ tableLoading ? 'Показать данные' : 'Показать загрузку' }}
          </UiButton>
          <span class="text-caption text-muted">
            сортировка по клику на заголовок (по кругу: вверх, вниз, исходный порядок),
            выделение строк, итог в подвале, липкая шапка при длинном списке,
            на узком экране строка разворачивается в блок
          </span>
        </div>

        <UiTable caption="Пример пустой таблицы" :columns="tableCols" :rows="[]">
          <template #empty>Профилей ещё нет — первый появится, когда вы дадите образец речи</template>
        </UiTable>

        <UiPagination v-model:page="page" :total="111" :per-page="10" />
      </div>
    </section>

    <!-- ── Ввод ─────────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Ввод</h2>
      <UiCard>
        <div class="flex flex-col gap-4">
          <div class="flex flex-wrap items-end gap-3">
            <span class="flex flex-col gap-1.5">
              <span class="text-caption font-semibold text-text-soft">Язык интерфейса</span>
              <UiSelect
                v-model="lang" label="Язык интерфейса"
                :options="[{ value: 'ru', label: 'Русский' }, { value: 'kk', label: 'Қазақша' }, { value: 'en', label: 'English' }]"
              />
            </span>
            <span class="flex flex-1 basis-70 flex-col gap-1.5">
              <span class="text-caption font-semibold text-text-soft">Корпоративный глоссарий</span>
              <UiTagsInput v-model="glossary" label="Термины глоссария" />
            </span>
          </div>

          <div class="grid gap-4 split:grid-cols-2">
            <span class="flex flex-col gap-1.5">
              <span class="text-caption font-semibold text-text-soft">Период оплаты</span>
              <UiRadioGroup
                v-model="period" label="Период оплаты"
                :options="[
                  { value: 'year', label: 'За год', note: '9 900 ₸ за место в месяц' },
                  { value: 'month', label: 'Помесячно', note: '15 900 ₸ за место в месяц' },
                ]"
              />
            </span>
            <span class="flex flex-col gap-1.5">
              <span class="text-caption font-semibold text-text-soft">Описание шаблона</span>
              <UiTextarea v-model="note" label="Описание шаблона" placeholder="Из каких разделов собирать протокол" />
            </span>
          </div>

          <UiFileDrop @pick="toast.push('Пример: файл выбран')" />
        </div>
      </UiCard>
    </section>

    <!-- ── Обратная связь ───────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Обратная связь<span class="ml-2 text-caption font-normal text-muted">тост исчезает, баннер остаётся, пока есть причина</span></h2>
      <div class="flex flex-col gap-3">
        <UiBanner>
          <template #title>Осталось 6 часов записи из 80 в этом месяце</template>
          Лимит считается на место. Когда он закончится, новые встречи записываться не будут.
          <template #action><UiButton small>Посмотреть тариф</UiButton></template>
        </UiBanner>
        <UiBanner tone="alert">
          <template #title>Google Calendar отключился</template>
          Встречи из календаря не подтягиваются с 22 августа — их придётся подключать по ссылке.
          <template #action><UiButton small>Подключить снова</UiButton></template>
        </UiBanner>
        <UiCard>
          <div class="flex flex-col gap-4">
            <UiProgress :value="64" label="Загрузка записи" />
            <UiProgress :value="null" label="Расшифровываем и собираем протокол — обычно 2–4 минуты" />
          </div>
        </UiCard>
      </div>
    </section>

    <!-- ── Навигация ────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Навигация</h2>
      <UiCard>
        <UiBreadcrumbs
          :items="[{ label: 'Все встречи', to: '/meetings' }, { label: 'Личные', to: '/meetings' }, { label: 'Собеседования' }]"
        />
        <div class="mt-4">
          <UiAccordion
            :items="[
              { value: 'a', title: 'Что входит в шаблон «Общее резюме»', text: 'Контекст встречи, основные обсуждённые темы, принятые решения, следующие шаги, открытые вопросы.' },
              { value: 'b', title: 'Почему протокол стоит проверить', text: 'Он собран автоматически. Формулировки берутся из речи, а речь бывает неточной — особенно в цифрах и именах.' },
            ]"
          />
        </div>
      </UiCard>
    </section>

    <!-- ── Матрица состояний ────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">
        Состояния<span class="ml-2 text-caption font-normal text-muted">кит без состояний — картинка, а не система</span>
      </h2>
      <UiCard>
        <div class="flex flex-col gap-4">
          <div class="flex flex-wrap items-end gap-4">
            <span class="flex flex-col gap-1.5"><span class="text-caption text-muted">покой</span><UiButton variant="primary">Сохранить</UiButton></span>
            <span class="flex flex-col gap-1.5"><span class="text-caption text-muted">загрузка</span><UiButton variant="primary" loading>Сохраняем</UiButton></span>
            <span class="flex flex-col gap-1.5"><span class="text-caption text-muted">выключено</span><UiButton variant="primary" as="button" disabled>Сохранить</UiButton></span>
            <span class="flex flex-col gap-1.5"><span class="text-caption text-muted">опасное</span><UiButton variant="danger">Удалить</UiButton></span>
            <span class="flex flex-col gap-1.5"><span class="text-caption text-muted">ссылка</span><UiButton variant="link">Показать ещё</UiButton></span>
            <span class="flex flex-col gap-1.5"><span class="text-caption text-muted">по-настоящему</span><UiButton variant="primary" :loading="busy" @click="pretendSave">Проверить</UiButton></span>
          </div>

          <UiDivider label="поле в трёх состояниях" />

          <div class="grid gap-4 split:grid-cols-3">
            <FormField label="Название встречи" hint="Видно только вам" required>
              <template #default="{ id, describedBy }">
                <UiField :id="id" :described-by="describedBy" model-value="Еженедельная планёрка" />
              </template>
            </FormField>

            <FormField label="Почта" :error="'Похоже, здесь опечатка: нет @'" required>
              <template #default="{ id, describedBy, invalid }">
                <UiField :id="id" v-model="email" :described-by="describedBy" :invalid="invalid" />
              </template>
            </FormField>

            <FormField label="Почта администратора" hint="Меняется через администратора">
              <template #default="{ id, describedBy }">
                <UiField :id="id" :described-by="describedBy" model-value="a.saparova@company.kz" readonly />
              </template>
            </FormField>
          </div>

          <UiDivider label="длинный текст и много данных" />

          <div class="grid gap-3 split:grid-cols-2">
            <UiRow>
              <template #icon><UiIcon name="doc" /></template>
              <template #title>Совместное совещание по вопросу приоритизации инициатив на четвёртый квартал</template>
              <template #why>Проверка на длинном заголовке: строка не должна ломать раскладку и выталкивать действие</template>
              <template #actions><UiButton size="sm">Открыть</UiButton></template>
            </UiRow>
            <div class="grid grid-cols-3 gap-2">
              <UiStat value="74 ч" label="Записано" note="из 80 в месяц" tone="warning" />
              <UiStat value="111" label="Встреч" />
              <UiStat value="2" label="Сорвалось" tone="danger" />
            </div>
          </div>

          <UiDivider label="ожидание и подсказки" />

          <div class="flex flex-wrap items-center gap-4">
            <span class="inline-flex items-center gap-2 text-ui text-text-soft"><UiSpinner /> Подключаемся к встрече…</span>
            <span class="text-ui text-text-soft">Поиск по кабинету — <UiKbd>⌘</UiKbd> <UiKbd>K</UiKbd> (работает)</span>
          </div>
        </div>
      </UiCard>
    </section>

    <!-- ── Ошибки ───────────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">
        Экраны ошибок<span class="ml-2 text-caption font-normal text-muted">что случилось, чья это вина и что делать дальше</span>
      </h2>
      <div class="grid gap-3 split:grid-cols-2">
        <ErrorState code="404" title="Такой страницы нет">
          Возможно, встречу удалили или ссылка устарела. Записи и протоколы на месте.
          <template #action><UiButton variant="primary" size="sm">На «Сегодня»</UiButton></template>
        </ErrorState>
        <ErrorState code="403" title="Нет доступа к этой встрече" tone="danger">
          Её создал другой человек и не открыл доступ. Попросите его поделиться протоколом.
          <template #action><UiButton size="sm">Написать организатору</UiButton></template>
        </ErrorState>
      </div>
    </section>

    <!-- ── Поверхности ──────────────────────────────────────── -->
    <section>
      <h2 class="mb-3 text-title font-semibold text-strong">Поверхности и состояния</h2>
      <div class="flex flex-col gap-3">
        <ul class="flex list-none flex-col gap-2 p-0">
          <UiRow>
            <template #icon><UiIcon name="doc" /></template>
            <template #title>Обычная строка</template>
            <template #why>Вторичная строка объясняет, что это и что с этим делать</template>
            <template #actions><UiButton small>Действие</UiButton></template>
          </UiRow>
          <UiRow tone="alert">
            <template #icon><UiIcon name="alert" /></template>
            <template #title>Строка, требующая решения</template>
            <template #why>Причина названа текстом, рядом одно осмысленное действие</template>
            <template #actions><UiButton small>Исправить</UiButton></template>
          </UiRow>
        </ul>

        <div class="grid gap-3 split:grid-cols-2">
          <UiCard>
            <b class="text-ui font-semibold text-strong">Карточка-панель</b>
            <p class="mt-1 text-ui text-muted">Раздел настройки: белая, держится границей.</p>
            <div class="mt-3 flex flex-col gap-2">
              <UiSkeleton w="w-2/3" />
              <UiSkeleton w="w-1/2" h="h-3" />
            </div>
          </UiCard>
          <UiCard quiet>
            <b class="text-ui font-semibold text-strong">Тихая карточка</b>
            <p class="mt-1 text-ui text-muted">Второстепенное: выход из кабинета, разговор про Enterprise.</p>
          </UiCard>
        </div>

        <EmptyState icon="search" title="Пустое состояние">
          <template #text>Объясняет, как устроен поиск, и даёт кнопку сброса — вместо молчания.</template>
          <template #action><UiButton small>Сбросить</UiButton></template>
        </EmptyState>
      </div>
    </section>
  </AppPage>
</template>
