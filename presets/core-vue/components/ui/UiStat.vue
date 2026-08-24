<script setup>
/* Показатель: число и что оно значит. На «Сегодня» такие плитки сняты
   намеренно — они не помогают принять решение. Живут там, где число само
   является ответом: расход квоты, счёт в биллинге.

   `icon` необязателен и меняет строй: без него число сверху, подпись снизу;
   с ним — плитка слева, число и подпись справа. Второй вид появился, когда
   выяснилось, что на боевой «Главной» у каждого показателя есть свой глиф,
   и вёрстка без него теряла опознавательный знак строки. */
import UiIcon from './UiIcon.vue'

defineProps({
  value: { type: String, required: true },
  label: { type: String, required: true },
  note: { type: String, default: '' },
  icon: { type: String, default: '' },
  tone: { type: String, default: 'plain' }, // plain | warning | danger
})
const tones = { plain: 'text-strong', warning: 'text-warning', danger: 'text-danger' }
</script>

<template>
  <div
    class="rounded-surface border border-line bg-raised px-3 py-2.5"
    :class="icon ? 'flex items-center gap-3' : 'flex flex-col gap-0.5'"
  >
    <span
      v-if="icon"
      class="grid h-10 w-10 shrink-0 place-items-center rounded-surface bg-accent-quiet text-accent"
    >
      <UiIcon :name="icon" :size="20" />
    </span>
    <span class="flex min-w-0 flex-col gap-0.5">
      <span class="text-h2 font-extrabold tabular-nums" :class="tones[tone]">{{ value }}</span>
      <span class="text-caption font-medium text-text-soft">{{ label }}</span>
      <span v-if="note" class="text-caption text-muted">{{ note }}</span>
    </span>
  </div>
</template>
