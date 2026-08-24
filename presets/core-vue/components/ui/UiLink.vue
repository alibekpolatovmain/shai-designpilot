<script setup>
/* Ссылка-действие: «Все встречи →», «Снять выделение», «Забыли пароль?».

   Появилась по факту повтора: одна и та же строка классов — акцентный цвет,
   полужирный, подчёркивание по наведению с отступом в четыре пикселя — была
   написана в семи местах, и в двух из них по-разному.

   Может быть маршрутом, внешней ссылкой или кнопкой. Это не косметика:
   «Все встречи» ведут на адрес и обязаны открываться в новой вкладке средним
   щелчком, а «Снять выделение» ничего не открывает и обязано быть кнопкой,
   иначе диктор объявит её ссылкой и человек будет ждать перехода.

   Подчёркивание появляется по наведению, а не стоит всегда: в плотном
   интерфейсе постоянные подчёркивания рябят. Цвет при этом делает ссылку
   опознаваемой и без него — акцент не используется больше нигде в тексте. */
defineProps({
  to: { type: [String, Object], default: null },
  href: { type: String, default: '' },
  size: { type: String, default: 'caption' }, // caption | ui
})

const base = 'inline-flex items-center gap-1 rounded-hair font-semibold text-accent transition-colors ' +
  'hover:text-accent-hover hover:underline hover:underline-offset-4 active:text-accent-hover'
</script>

<template>
  <RouterLink v-if="to" :to="to" :class="[base, size === 'ui' ? 'text-ui' : 'text-caption']">
    <slot />
  </RouterLink>
  <!-- Внешняя ссылка честно говорит, что уводит: rel обязателен, иначе чужая
       страница получает доступ к нашей через window.opener -->
  <a
    v-else-if="href" :href="href" target="_blank" rel="noopener noreferrer"
    :class="[base, size === 'ui' ? 'text-ui' : 'text-caption']"
  ><slot /></a>
  <button v-else type="button" :class="[base, size === 'ui' ? 'text-ui' : 'text-caption']">
    <slot />
  </button>
</template>
