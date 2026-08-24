import { reactive } from 'vue'

/* Тосты: подтверждение действия, у которого нет видимого результата на экране.
   «Скопировано», «Сохранено», «Обработка запущена». Живут 4 секунды и не
   требуют реакции — то, что требует реакции, показывается диалогом. */
const state = reactive({ items: [] })
let seq = 0

export function useToast() {
  return {
    items: state.items,
    push(text, tone = 'plain') {
      const id = ++seq
      state.items.push({ id, text, tone })
      setTimeout(() => {
        const i = state.items.findIndex((t) => t.id === id)
        if (i !== -1) state.items.splice(i, 1)
      }, 4000)
    },
    dismiss(id) {
      const i = state.items.findIndex((t) => t.id === id)
      if (i !== -1) state.items.splice(i, 1)
    },
  }
}
