<script setup>
/* Клавиша в тексте: «⌘K — поиск», «Esc — закрыть». Моноширинная,
   потому что символы сравнивают глазом, а не читают. */
</script>

<template>
  <kbd class="inline-flex h-5 min-w-5 items-center justify-center rounded-hair border border-line-strong
              bg-surface px-1 font-mono text-caption text-text-soft">
    <slot />
  </kbd>
</template>
