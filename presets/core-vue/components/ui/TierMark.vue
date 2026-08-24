<script setup>
/* Маркер тарифа: обещание о данных не выносится на уровень продукта.
   base — то, что действует везде; оно не должно спорить с платными ступенями. */
defineProps({ base: Boolean })
</script>

<template>
  <span
    class="inline-flex shrink-0 items-center whitespace-nowrap rounded-full px-2 py-0.5 text-caption"
    :class="base ? 'bg-surface font-semibold text-muted' : 'bg-accent-quiet font-bold text-accent'"
  >
    <slot />
  </span>
</template>
