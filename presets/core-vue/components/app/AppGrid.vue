<script setup>
/* Колоночная сетка: 4 / 8 / 12 по брейкпоинтам, желоб из токена.
   Дочерние элементы занимают колонки через GridCol — так карточки на
   «Сегодня», колонки экрана встречи и поля в формах стоят на одних линиях. */
</script>

<template>
  <div class="grid grid-cols-4 gap-4 one:grid-cols-8 frame:grid-cols-12 frame:gap-6">
    <slot />
  </div>
</template>
