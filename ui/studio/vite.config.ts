import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/V4.0/studio/',
  plugins: [
    vue(),
    Components({
      resolvers: [AntDesignVueResolver({ importStyle: 'less', resolveIcons: true })]
    })
  ],
  css: {
    preprocessorOptions: {
      less: {
        modifyVars: {
          'primary-color': '#007011',
          'border-radius-base': '4px',
          'font-size-base': '16px',
          'font-family': 'Josefin Sans, sans-serif',
        },
        javascriptEnabled: true,
      },
    },
  },
})
