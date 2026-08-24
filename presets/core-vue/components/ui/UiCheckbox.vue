<script setup>
/* Чекбокс: сам квадрат 16px, но цель нажатия — вся строка с подписью.

   Третье состояние обязательно: «выбрать все» в таблице, когда отмечена
   часть строк. Без него флажок врёт — показывает «ничего не выбрано» там,
   где выбрано три из десяти. */
import { CheckboxRoot, CheckboxIndicator } from 'reka-ui'
import UiIcon from './UiIcon.vue'

/* Атрибуты идут на сам флажок, а не на обёртку-<label>. Иначе aria-label
   оседает на подписи, а кнопка с role="checkbox" остаётся безымянной: диктор
   читает «флажок», не говоря, что именно выбирают. В списке из десяти строк
   это делает выделение бесполезным. */
defineOptions({ inheritAttrs: false })

defineProps({
  modelValue: { type: [Boolean, String], default: false }, // true | false | 'indeterminate'
  label: { type: String, default: '' },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <!-- Цель нажатия — не сам квадрат 16px, а поле вокруг него: WCAG 2.5.8
       требует 24×24. Без подписи метка сжималась ровно до квадрата, и в
       списке из десяти строк промахнуться было легче, чем попасть. -->
  <label class="inline-flex min-h-6 min-w-6 cursor-pointer items-start justify-center gap-2 p-1
                pointer-coarse:min-h-11 pointer-coarse:min-w-11 has-[span]:justify-start">
    <CheckboxRoot
      v-bind="$attrs"
      :model-value="modelValue"
      class="mt-0.5 grid h-4 w-4 shrink-0 place-items-center rounded-hair border border-line-control
             bg-raised transition-colors data-[state=checked]:border-accent data-[state=checked]:bg-accent
             data-[state=indeterminate]:border-accent data-[state=indeterminate]:bg-accent"
      @update:model-value="$emit('update:modelValue', $event)"
    >
      <CheckboxIndicator class="text-on-solid">
        <UiIcon :name="modelValue === 'indeterminate' ? 'minus' : 'check'" :size="12" :stroke="3.2" />
      </CheckboxIndicator>
    </CheckboxRoot>
    <!-- Подпись принимает разметку: в согласии с условиями внутри строки
         живёт ссылка, а строкой в проп её не передать -->
    <span v-if="label || $slots.default" class="text-ui text-text"><slot>{{ label }}</slot></span>
  </label>
</template>
