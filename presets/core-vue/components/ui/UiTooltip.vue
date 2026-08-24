<script setup>
/* Подсказка для иконочных кнопок: у них нет подписи, и без неё смысл
   действия угадывается. Появляется по наведению и по фокусу. */
import { TooltipProvider, TooltipRoot, TooltipTrigger, TooltipPortal, TooltipContent } from 'reka-ui'

defineProps({ text: { type: String, required: true }, side: { type: String, default: 'top' } })
</script>

<template>
  <TooltipProvider :delay-duration="350">
    <TooltipRoot>
      <TooltipTrigger as-child><slot /></TooltipTrigger>
      <TooltipPortal>
        <TooltipContent
          :side="side" :side-offset="6"
          class="z-pop rounded-micro bg-inverse px-2 py-1 text-caption font-medium text-on-inverse shadow-md"
        >
          {{ text }}
        </TooltipContent>
      </TooltipPortal>
    </TooltipRoot>
  </TooltipProvider>
</template>
