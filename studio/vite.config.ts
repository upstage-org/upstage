import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tsconfigPaths from "vite-tsconfig-paths";
import Components from "unplugin-vue-components/vite";
import { AntDesignVueResolver } from "unplugin-vue-components/resolvers";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/studio/",
  plugins: [
    vue(),
    tsconfigPaths(),
    Components({
      resolvers: [
        AntDesignVueResolver({ importStyle: "less", resolveIcons: true }),
      ],
    }),
  ],
  server: {
    fs: {
      // Allow serving files from one level up to the project root
      allow: [".."],
    },
  },
  css: {
    preprocessorOptions: {
      less: {
        modifyVars: {
          dark: true,
          "primary-color": "#007011",
          "border-radius-base": "4px",
          "font-size-base": "16px",
          "font-family": "Josefin Sans, sans-serif",
          "table-padding-vertical": "8px",
        },
        javascriptEnabled: true,
      },
    },
  },
});
