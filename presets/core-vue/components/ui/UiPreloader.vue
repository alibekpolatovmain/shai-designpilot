<script setup>
/* Прелоадер — голос, по которому идёт распознавание.

   Крутилка одинакова у всех продуктов и не говорит ничего. Здесь ждут не
   «загрузки вообще», а превращения голоса в текст: столбики качаются, как
   звук, и по ряду слева направо пробегает волна цвета — распознавание идёт
   по записи. Те же столбики, которыми на экране встречи нарисована сама
   запись: один язык на продукт, волна значит голос.

   Ряд нечётный (семь), чтобы у волны был центр, и высоты заданы вручную —
   ровный ряд читается как эквалайзер из плеера, неровный как речь.

   При выключенной анимации остаются те же столбики без движения: ожидание
   всё равно видно, а голова не кружится. */
const props = defineProps({
  size: { type: String, default: 'md' },   // sm | md | lg
  label: { type: String, default: '' },
  /* inline — в строке рядом с текстом, без подписи снизу */
  inline: Boolean,
})

const sizes = {
  sm: { w: 'w-0.5', gap: 'gap-0.5', h: 'h-4' },
  md: { w: 'w-1', gap: 'gap-1', h: 'h-7' },
  lg: { w: 'w-1.5', gap: 'gap-1', h: 'h-10' },
}
/* Высоты и задержки — не случайные: волна должна читаться как речь, а не
   как бегущая строка. Центр выше краёв, задержки идут по нарастающей. */
const bars = [
  { h: 45, d: 0 }, { h: 70, d: 90 }, { h: 55, d: 180 }, { h: 100, d: 270 },
  { h: 60, d: 360 }, { h: 80, d: 450 }, { h: 40, d: 540 },
]
</script>

<template>
  <span
    class="inline-flex items-center"
    :class="[props.inline ? 'gap-2' : 'flex-col gap-2.5', sizes[props.size].gap]"
    role="status" :aria-label="label || 'Идёт обработка'"
  >
    <span class="flex items-end" :class="[sizes[props.size].gap, sizes[props.size].h]">
      <span
        v-for="(b, i) in bars" :key="i"
        class="wave-bar block origin-bottom rounded-full bg-line-strong"
        :class="sizes[props.size].w"
        :style="{ height: `${b.h}%`, animationDelay: `${b.d}ms, ${b.d}ms` }"
      />
    </span>
    <span v-if="label" class="text-caption text-muted">{{ label }}</span>
  </span>
</template>
