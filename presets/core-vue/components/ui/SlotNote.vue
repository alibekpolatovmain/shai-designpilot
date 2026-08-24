<script setup>
/* Метка непроверенного: место, где данные или поведение ещё не подтверждены
   владельцем продукта.

   Правило системы: **ничего не выдумывать**. Если неизвестно, что происходит
   после кнопки или откуда берётся число, это не повод придумать правдоподобно
   — это повод пометить. Пунктир и подпись видны и на макете, и в прототипе,
   поэтому непроверенное не проезжает в продакшн незамеченным.

   Метка намеренно некрасивая: она должна мешать. Аккуратная серая подпись
   живёт в интерфейсе годами, пунктирная рамка — до первого разговора. */
defineProps({ label: { type: String, default: 'Уточнить у владельца' } })
</script>

<template>
  <p
    class="flex items-start gap-2 rounded-control border border-dashed border-warning bg-warning-soft
           px-3 py-2 text-caption text-on-warning-soft"
    role="note"
  >
    <b class="shrink-0 font-semibold">{{ label }}:</b>
    <span class="min-w-0"><slot /></span>
  </p>
</template>
