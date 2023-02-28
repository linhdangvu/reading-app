import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Pages from "vite-plugin-pages";
import Components from "unplugin-vue-components/vite";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    // proxy: {
    //   "/books": {
    //     target: "http://localhost:5000/ping",
    //     changeOrigin: true,
    //     secure: false,
    //     rewrite: (path) => path.replace(/^\/reading/, ""),
    //   },
    // },
    // A changer dependire
    host: "172.16.4.28",
    port: 5173,
  },
  plugins: [
    vue(),
    Pages({
      nuxtStyle: false,
      pagesDir: [
        {
          dir: "src/pages",
          baseRoute: "",
        },
      ],
    }),
    Components({
      /* options */
      dirs: ["documentation", "src/components", "src/layouts"],
      extensions: ["vue", "md"],
      dts: true,
      include: [/\.vue$/, /\.vue\?vue/, /\.md$/],
    }),
  ],
});
