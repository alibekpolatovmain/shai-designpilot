<script setup>
/* Поле ввода — тот же контрол, что кнопка: три размера из общей метрики.

   У каждого размера своё место, и они те же, что у кнопки:
     sm — поле внутри строки, панели или ячейки (поиск по транскрипту);
     md — по умолчанию: форма, фильтр;
     lg — единственное поле на экране, мобильный ввод.
   Раньше высота была одна, и поле рядом с кнопкой sm выглядело крупнее её,
   хотя стоять они должны в одну линию.

   Кегль ниже 14px не опускается даже на sm: введённое ищут глазами, а не
   читают подряд, и 12px в поле стоит дороже, чем 12px в подписи.

   Кромка остаётся 3:1 (`line-control`): у пустого поля опознавать нечего,
   кроме неё — DESIGN.md, «Контраст несёт то, что опознаёт контрол».

   Фокус — ОДНО кольцо, а не два. Прежде кроме акцентной кромки рисовалось
   ещё отдельное кольцо в двух пикселях от неё: два зелёных контура вокруг
   одного поля с полосой фона между ними. Теперь кромка становится акцентной,
   и вплотную к ней ложится мягкий ореол — вместе это читается как одно
   утолщённое ребро. Контраст держит кромка (5.4:1), ореол только собирает
   их в одно пятно.

   Отдельное кольцо остаётся у того, у кого своего ребра нет: у ссылки,
   призрачной кнопки, строки списка. Утолщать там нечего. */
import { onMounted, ref } from 'vue'
import UiIcon from './UiIcon.vue'

/* Атрибуты идут на сам `input`, а не на обёртку: иначе autocomplete,
   inputmode и maxlength оседали бы на <label>, и браузер их не видел. */
defineOptions({ inheritAttrs: false })

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, default: '' },
  /* Приходят из FormField: подпись, подсказка и ошибка живут там */
  id: { type: String, default: '' },
  describedBy: { type: String, default: undefined },
  icon: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  size: { type: String, default: 'md' }, // sm | md | lg
  invalid: Boolean,
  readonly: Boolean,
  disabled: Boolean,
})
const emit = defineEmits(['update:modelValue'])

/* Автозаполнение браузера не всегда доходит до модели: Chrome подставляет
   значение до того, как компонент начал слушать, и `input` может не
   прилететь вовсе. Поле выглядит заполненным, а форма считает его пустым —
   и кнопка «Войти» остаётся выключенной у человека, который всё ввёл.
   Именно этот дефект виден на живой странице входа.

   Лечится двумя вещами: слушаем ещё и `change` (его автозаполнение шлёт
   надёжнее), а после монтирования сверяем DOM с моделью. */
const field = ref(null)
onMounted(() => {
  const el = field.value
  if (el && el.value && el.value !== props.modelValue) emit('update:modelValue', el.value)
})

const box = {
  sm: 'h-ctl-sm gap-1.5 px-2.5 text-ui',
  md: 'h-ctl gap-2 px-3 text-ui',
  lg: 'h-ctl-lg gap-2.5 px-4 text-doc',
}
const glyph = { sm: 15, md: 17, lg: 19 }
</script>

<template>
  <component
    :is="props.id ? 'div' : 'label'"
    class="flex min-w-0 items-center rounded-control border transition-[color,background-color,border-color,box-shadow]
           focus-within:ring-3 focus-within:ring-accent-quiet"
    :class="[
      box[props.size],
      props.invalid ? 'border-danger text-danger'
        : props.disabled || props.readonly ? 'border-line-control bg-surface text-muted'
        : 'border-line-control bg-raised text-muted focus-within:border-accent',
    ]"
  >
    <UiIcon v-if="icon" :name="icon" :size="glyph[props.size]" />
    <input
      :id="props.id || undefined" :type="type" :placeholder="placeholder"
      :aria-label="props.id ? undefined : label" :aria-describedby="describedBy"
      :aria-invalid="props.invalid || undefined" :readonly="readonly" :disabled="disabled"
      ref="field"
      :value="modelValue"
      v-bind="$attrs"
      class="min-w-0 flex-1 border-0 bg-transparent outline-none placeholder:text-muted
             disabled:cursor-not-allowed"
      :class="props.readonly || props.disabled ? 'text-muted' : 'text-text'"
      @input="emit('update:modelValue', $event.target.value)"
      @change="emit('update:modelValue', $event.target.value)"
    />
    <slot name="suffix" />
  </component>
</template>
