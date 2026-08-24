<script setup>
/* Карточка раздела. Заголовок — часть примитива, а не отдельная разметка на
   каждом экране: иначе кегль и отступ шапки расходятся от карточки к карточке. */
/* `tone` — заливка карточки. Появился, когда выяснилось, что на боевой
   «Главной» шапка залита брендом на 6% и читается как блок, а наша белая
   карточка на белом грунте держалась на одной кромке. Сверка этого не
   поймала: элементы все на месте, разошлась заливка. */
defineProps({
  quiet: Boolean,
  tone: { type: String, default: 'plain' }, // plain | accent
  title: String,
  note: String,
})
const tones = {
  plain: 'border border-line bg-raised',
  accent: 'border border-accent-line bg-accent-quiet',
}
</script>

<template>
  <section
    class="rounded-panel p-4 frame:p-6"
    :class="quiet ? 'bg-surface' : tones[tone]"
  >
    <header v-if="title" class="mb-3 flex flex-col gap-0.5">
      <h2 class="text-title font-semibold tracking-title text-strong">{{ title }}</h2>
      <p v-if="note" class="max-w-note text-caption text-muted">{{ note }}</p>
    </header>
    <slot />
  </section>
</template>
