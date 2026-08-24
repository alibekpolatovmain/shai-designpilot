<script setup>
/* Внешний вид одним меню: тема и плотность. Стоит в верхней панели, потому
   что это переключатель просмотра — как масштаб или язык, а не настройка
   аккаунта. Полная версия с пояснениями живёт в Профиле. */
import UiIcon from '../ui/UiIcon.vue'
import UiIconButton from '../ui/UiIconButton.vue'
import UiMenu from '../ui/UiMenu.vue'
import UiMenuItem from '../ui/UiMenuItem.vue'
import UiMenuLabel from '../ui/UiMenuLabel.vue'
import UiMenuSeparator from '../ui/UiMenuSeparator.vue'
import { theme, themes, density, densities } from '../../design/appearance.js'
</script>

<template>
  <UiMenu>
    <template #trigger>
      <UiIconButton label="Внешний вид: тема и плотность">
        <UiIcon name="theme" :size="16" />
      </UiIconButton>
    </template>

    <UiMenuLabel>Тема</UiMenuLabel>
    <UiMenuItem
      v-for="t in themes" :key="t.value" :current="theme === t.value"
      @select="theme = t.value"
    >
      {{ t.label }}
      <UiIcon v-if="theme === t.value" name="check" :size="15" :stroke="2.2" class="text-accent" />
    </UiMenuItem>

    <UiMenuSeparator />

    <UiMenuLabel>Плотность</UiMenuLabel>
    <UiMenuItem
      v-for="d in densities" :key="d.value" :current="density === d.value"
      @select="density = d.value"
    >
      {{ d.label }}
      <UiIcon v-if="density === d.value" name="check" :size="15" :stroke="2.2" class="text-accent" />
    </UiMenuItem>
  </UiMenu>
</template>
