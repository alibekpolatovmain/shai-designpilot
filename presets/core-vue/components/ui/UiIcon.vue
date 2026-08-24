<script setup>
/* Обёртка над набором: экраны просят иконку по имени из языка продукта,
   а не импортируют глиф напрямую. Размер и толщина — часть системы, поэтому
   объявлены здесь, а не подбираются на месте. */
import { icons } from './icons.js'

const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 18 },
  /* 1.75 при сетке 24: на кегле 16px даёт штрих в 1.17px — ровно вес Inter
     Medium рядом. Родные для Lucide 2 рядом с нашим текстом выглядят жирнее
     подписи, а 1.5 распадается на светлом фоне. */
  stroke: { type: [Number, String], default: 1.75 },
})
</script>

<template>
  <component
    :is="icons[props.name]"
    :size="Number(props.size)"
    :stroke-width="Number(props.stroke)"
    aria-hidden="true"
    class="shrink-0"
  />
</template>
