<script setup>
/* Обёртка поля: подпись, подсказка, ошибка, обязательность, счётчик.
   Без неё каждый экран собирает это заново и по-своему — а именно здесь
   живут требования доступности: label связан с полем, ошибка объявлена
   через aria-describedby и произносится экранным диктором. */
import { useId } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  hint: { type: String, default: '' },
  error: { type: String, default: '' },
  required: Boolean,
  counter: { type: String, default: '' },
})

const id = useId()
const hintId = `${id}-hint`
const errorId = `${id}-error`
</script>

<template>
  <div class="flex flex-col gap-1.5">
    <label :for="id" class="flex items-center gap-1 text-caption font-semibold text-text-soft">
      {{ label }}
      <span v-if="required" class="text-danger" aria-hidden="true">*</span>
      <span v-if="required" class="sr-only">обязательное поле</span>
    </label>

    <slot :id="id" :described-by="[hint && hintId, error && errorId].filter(Boolean).join(' ') || undefined" :invalid="!!error" />

    <div v-if="hint || error || counter" class="flex items-start justify-between gap-3">
      <span v-if="error" :id="errorId" class="text-caption text-danger" role="alert">{{ error }}</span>
      <span v-else-if="hint" :id="hintId" class="text-caption text-muted">{{ hint }}</span>
      <span v-if="counter" class="ml-auto shrink-0 text-caption tabular-nums text-muted">{{ counter }}</span>
    </div>
  </div>
</template>
