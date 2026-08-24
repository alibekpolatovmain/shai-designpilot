/* Порядок важен: гарнитуры → токены → базовый слой → приложение.
   Базовый слой читает переменные токенов, поэтому идёт после них. */
import '@fontsource/inter/400.css'
import '@fontsource/inter/500.css'
import '@fontsource/inter/600.css'
import '@fontsource/inter/700.css'
import './design/tokens.css'
import './design/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router.js'

createApp(App).use(router).mount('#app')
