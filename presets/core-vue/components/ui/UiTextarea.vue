<script setup>
/* Многострочный ввод: описание своего шаблона, заметка к встрече.
   Растёт до предела, дальше прокручивается — страница от этого не прыгает. */
defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, required: true },
  placeholder: { type: String, default: '' },
  rows: { type: Number, default: 3 },
  size: { type: String, default: 'md' }, // sm | md | lg — поля и кегль, высоту задаёт rows
})
defineEmits(['update:modelValue'])
</script>

<template>
  <textarea
    :value="modelValue" :aria-label="label" :placeholder="placeholder" :rows="rows"
    class="max-h-52 w-full resize-y rounded-control border border-line-control bg-raised text-text
           outline-none transition-[border-color,box-shadow] placeholder:text-muted
           focus-visible:border-accent focus-visible:ring-3 focus-visible:ring-accent-quiet"
    :class="{ sm: 'px-2.5 py-1.5 text-ui', md: 'px-3 py-2 text-ui', lg: 'px-4 py-2.5 text-doc' }[size]"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>
