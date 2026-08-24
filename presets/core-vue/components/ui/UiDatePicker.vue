<script setup>
/* Выбор периода: «встречи за неделю», «расход с 1 по 30».

   Период, а не одна дата, потому что в кабинете спрашивают именно про
   отрезок: одна дата нужна разве что в напоминании, и для неё есть тот же
   примитив с одним значением.

   Календарь берёт локаль ru: неделя начинается с понедельника, месяцы и дни
   склоняются правильно, «сегодня» подписано. Своя сетка дат — это всегда
   чужая неделя с воскресенья и «Sun» в шапке.

   Дни недели сокращением, а не одной буквой: по-русски однобуквенный ряд
   «П В С Ч П С В» неразличим — П это понедельник или пятница, С это среда
   или суббота. В английском «M T W T F S S» тоже неоднозначен, но там к
   нему привыкли; здесь привычки нет, и гадать человек не должен. */
import { DateRangePickerRoot, DateRangePickerTrigger, DateRangePickerContent,
         DateRangePickerField, DateRangePickerInput, DateRangePickerCalendar,
         DateRangePickerHeader, DateRangePickerPrev, DateRangePickerHeading, DateRangePickerNext,
         DateRangePickerGrid, DateRangePickerGridHead, DateRangePickerGridRow, DateRangePickerHeadCell,
         DateRangePickerGridBody, DateRangePickerCell, DateRangePickerCellTrigger } from 'reka-ui'
import { today, getLocalTimeZone } from '@internationalized/date'
import UiIcon from './UiIcon.vue'

defineProps({
  modelValue: { type: Object, default: undefined }, // { start, end } из @internationalized/date
  label: { type: String, required: true },
})

/* Пока период не выбран, полю нужен ориентир — иначе оно не знает, какие
   разряды показывать и какой месяц открыть. Это не значение, а точка
   отсчёта: поле остаётся пустым, а календарь открывается на текущем месяце. */
const anchor = today(getLocalTimeZone())
defineEmits(['update:modelValue'])
</script>

<template>
  <DateRangePickerRoot
    :model-value="modelValue" :placeholder="anchor" locale="ru-RU" weekday-format="short"
    :aria-label="label"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <DateRangePickerField
      v-slot="{ segments }"
      class="flex h-ctl w-fit items-center gap-1 rounded-control border border-line-control bg-raised px-3
             text-ui text-text transition-[border-color,box-shadow] focus-within:border-accent
             focus-within:ring-3 focus-within:ring-accent-quiet"
    >
      <!-- У периода два поля, и слот отдаёт их раздельно: segments.start и
           segments.end. Плоский перебор давал пустое поле — разряды просто
           не находились. -->
      <template v-for="type in ['start', 'end']" :key="type">
        <span v-if="type === 'end'" class="px-1 text-muted" aria-hidden="true">—</span>
        <template v-for="item in segments[type]" :key="`${type}-${item.part}`">
          <DateRangePickerInput
            v-if="item.part !== 'literal'" :part="item.part" :type="type"
            class="rounded-hair px-0.5 tabular-nums outline-none data-[placeholder]:text-muted
                   focus:bg-accent-quiet focus:text-accent"
          >{{ item.value }}</DateRangePickerInput>
          <span v-else class="text-muted">{{ item.value }}</span>
        </template>
      </template>
      <DateRangePickerTrigger class="press ml-1 text-muted hover:text-strong" aria-label="Открыть календарь">
        <UiIcon name="calendar" :size="16" />
      </DateRangePickerTrigger>
    </DateRangePickerField>

    <DateRangePickerContent
      :side-offset="6" class="z-pop rounded-nested border border-line bg-raised p-3 shadow-lg"
    >
      <DateRangePickerCalendar v-slot="{ weekDays, grid }">
        <DateRangePickerHeader class="mb-2 flex items-center justify-between gap-2">
          <DateRangePickerPrev
            class="press grid h-ctl-sm w-ctl-sm place-items-center rounded-control text-muted
                   hover:bg-surface hover:text-strong active:bg-surface-2"
            aria-label="Предыдущий месяц"
          ><UiIcon name="back" :size="16" /></DateRangePickerPrev>
          <DateRangePickerHeading class="text-ui font-semibold text-strong" />
          <DateRangePickerNext
            class="press grid h-ctl-sm w-ctl-sm place-items-center rounded-control text-muted
                   hover:bg-surface hover:text-strong active:bg-surface-2"
            aria-label="Следующий месяц"
          ><UiIcon name="back" :size="16" class="rotate-180" /></DateRangePickerNext>
        </DateRangePickerHeader>

        <DateRangePickerGrid v-for="month in grid" :key="month.value.toString()" class="w-full border-collapse">
          <DateRangePickerGridHead>
            <DateRangePickerGridRow class="flex w-full">
              <DateRangePickerHeadCell
                v-for="day in weekDays" :key="day"
                class="w-9 text-caption font-semibold text-muted"
              >{{ day }}</DateRangePickerHeadCell>
            </DateRangePickerGridRow>
          </DateRangePickerGridHead>
          <DateRangePickerGridBody>
            <DateRangePickerGridRow
              v-for="(week, i) in month.rows" :key="`week-${i}`" class="flex w-full"
            >
              <DateRangePickerCell v-for="d in week" :key="d.toString()" :date="d" class="p-0">
                <DateRangePickerCellTrigger
                  :day="d" :month="month.value"
                  class="press grid h-9 w-9 place-items-center rounded-control text-ui tabular-nums text-text
                         hover:bg-surface data-[outside-view]:text-line-strong
                         data-[selected]:bg-accent-quiet data-[selected]:text-accent
                         data-[selection-start]:bg-accent data-[selection-start]:text-on-solid
                         data-[selection-end]:bg-accent data-[selection-end]:text-on-solid
                         data-[today]:font-bold data-[unavailable]:line-through"
                />
              </DateRangePickerCell>
            </DateRangePickerGridRow>
          </DateRangePickerGridBody>
        </DateRangePickerGrid>
      </DateRangePickerCalendar>
    </DateRangePickerContent>
  </DateRangePickerRoot>
</template>
