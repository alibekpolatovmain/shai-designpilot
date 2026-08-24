<script setup>
/* Ползунок: громкость, скорость воспроизведения, порог.

   В плеере громкость и позиция были нарисованы вручную дважды, и с
   клавиатуры ни одна не двигалась. Примитив даёт стрелки, Home/End,
   PageUp/PageDown и правильную роль для диктора — это не украшение, а
   единственный способ управлять звуком без мыши. */
import { SliderRoot, SliderTrack, SliderRange, SliderThumb } from 'reka-ui'

defineProps({
  modelValue: { type: Number, required: true },
  label: { type: String, required: true },
  min: { type: Number, default: 0 },
  max: { type: Number, default: 100 },
  step: { type: Number, default: 1 },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <SliderRoot
    :model-value="[modelValue]" :min="min" :max="max" :step="step" :aria-label="label"
    class="relative flex h-ctl w-full min-w-20 touch-none select-none items-center"
    @update:model-value="$emit('update:modelValue', $event[0])"
  >
    <SliderTrack class="relative h-1 w-full grow rounded-full bg-surface-2">
      <SliderRange class="absolute h-full rounded-full bg-accent" />
    </SliderTrack>
    <SliderThumb
      class="block h-3.5 w-3.5 rounded-full border-2 border-accent bg-raised transition-transform
             hover:scale-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus"
    />
  </SliderRoot>
</template>
