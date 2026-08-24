<script setup>
/* Загрузка записи. Подтверждённые продуктом ограничения названы прямо
   в зоне, а не в тексте где-то рядом: MP3, WAV, M4A, OGG, OPUS, FLAC, MP4
   до 500 МБ. Ошибка формата объясняет, что не так, а не «файл не подходит». */
import { ref } from 'vue'
import UiIcon from './UiIcon.vue'
import UiButton from './UiButton.vue'

defineProps({
  accept: { type: String, default: 'MP3, WAV, M4A, OGG, OPUS, FLAC, MP4' },
  limit: { type: String, default: '500 МБ' },
})
const emit = defineEmits(['pick'])

const over = ref(false)
const name = ref('')

function take(file) {
  if (!file) return
  name.value = file.name
  emit('pick', file)
}
</script>

<template>
  <label
    class="flex cursor-pointer flex-col items-center gap-2 rounded-panel border border-dashed px-5 py-6
           text-center transition-colors"
    :class="over ? 'border-accent bg-accent-quiet' : 'border-line-control bg-raised hover:border-strong'"
    @dragover.prevent="over = true" @dragleave="over = false"
    @drop.prevent="over = false; take($event.dataTransfer.files[0])"
  >
    <span class="grid h-10 w-10 place-items-center rounded-full bg-surface text-muted">
      <UiIcon name="download" :size="19" :stroke="1.8" class="rotate-180" />
    </span>
    <b class="text-ui font-semibold text-strong">{{ name || 'Перетащите запись сюда' }}</b>
    <span class="text-caption text-muted">{{ accept }} · до {{ limit }}</span>
    <UiButton small as="span">Выбрать файл</UiButton>
    <input type="file" class="sr-only" @change="take($event.target.files[0])" />
  </label>
</template>
