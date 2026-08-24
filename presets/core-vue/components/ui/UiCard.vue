<script setup>
/* Карточка раздела. Заголовок — часть примитива, а не отдельная разметка на
   каждом экране: иначе кегль и отступ шапки расходятся от карточки к карточке. */
defineProps({ quiet: Boolean, title: String, note: String })
</script>

<template>
  <section
    class="rounded-panel p-4 frame:p-6"
    :class="quiet ? 'bg-surface' : 'border border-line bg-raised'"
  >
    <header v-if="title" class="mb-3 flex flex-col gap-0.5">
      <h2 class="text-title font-semibold tracking-title text-strong">{{ title }}</h2>
      <p v-if="note" class="max-w-note text-caption text-muted">{{ note }}</p>
    </header>
    <slot />
  </section>
</template>
