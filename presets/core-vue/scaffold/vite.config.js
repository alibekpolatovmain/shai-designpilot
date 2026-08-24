import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwind from '@tailwindcss/vite'

/* Tailwind как плагин Vite, без postcss.config: тема объявлена прямо в
   design/tokens.css через @theme static, и второй конфигурации не нужно. */
export default defineConfig({ plugins: [vue(), tailwind()] })
