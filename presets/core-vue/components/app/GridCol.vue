<script setup>
/* Сколько колонок занимает блок на каждом размере.
   Значения — доли от 4 / 8 / 12; по умолчанию блок занимает всю ширину. */
const props = defineProps({
  span: { type: Number, default: 4 },        // до 641px, из 4
  one: { type: Number, default: null },      // 641–900, из 8
  frame: { type: Number, default: null },    // 901+, из 12
})

/* Классы перечислены целиком: Tailwind собирает CSS по исходнику,
   и строка, склеенная в рантайме, до него не доедет. */
const base = {
  1: 'col-span-1', 2: 'col-span-2', 3: 'col-span-3', 4: 'col-span-4',
}
const onCols = {
  1: 'one:col-span-1', 2: 'one:col-span-2', 3: 'one:col-span-3', 4: 'one:col-span-4',
  5: 'one:col-span-5', 6: 'one:col-span-6', 7: 'one:col-span-7', 8: 'one:col-span-8',
}
const frameCols = {
  1: 'frame:col-span-1', 2: 'frame:col-span-2', 3: 'frame:col-span-3', 4: 'frame:col-span-4',
  5: 'frame:col-span-5', 6: 'frame:col-span-6', 7: 'frame:col-span-7', 8: 'frame:col-span-8',
  9: 'frame:col-span-9', 10: 'frame:col-span-10', 11: 'frame:col-span-11', 12: 'frame:col-span-12',
}
</script>

<template>
  <div :class="[base[props.span], props.one && onCols[props.one], props.frame && frameCols[props.frame]]">
    <slot />
  </div>
</template>
