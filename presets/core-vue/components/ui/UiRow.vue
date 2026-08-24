<script setup>
/* Строка очереди и списка настроек: иконка, тело, действия.
   tone="alert" — семейство «внимание»: рамка и подложка, причина текстом. */
defineProps({ tone: { type: String, default: 'plain' } })
</script>

<template>
  <li
    class="flex flex-wrap items-center gap-3 rounded-surface border px-3 py-row"
    :class="tone === 'alert' ? 'border-danger/32 bg-danger/3' : 'border-line bg-raised'"
  >
    <!-- Время в расписании — не иконка: своя ячейка без плитки -->
    <span v-if="$slots.lead" class="flex shrink-0 flex-col leading-none"><slot name="lead" /></span>

    <span
      v-else-if="$slots.icon"
      class="grid h-8 w-8 shrink-0 place-items-center rounded-control"
      :class="tone === 'alert' ? 'bg-danger/10 text-danger' : 'bg-surface text-muted'"
    >
      <slot name="icon" />
    </span>

    <span class="flex min-w-0 flex-1 flex-col gap-0.5">
      <b class="text-ui font-semibold text-strong"><slot name="title" /></b>
      <span class="text-caption text-muted"><slot name="why" /></span>
    </span>

    <span class="flex shrink-0 items-center gap-2.5 max-frame:w-full max-frame:pl-10">
      <slot name="actions" />
    </span>
  </li>
</template>
