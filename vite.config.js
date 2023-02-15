import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Pages from "vite-plugin-pages";
import Components from "unplugin-vue-components/vite";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    // proxy: {
    //   "/produits": {
    //     target: "http://51.255.166.155:1353/logAccordsVente/1664/?format=json",
    //     changeOrigin: true,
    //     secure: false,
    //     rewrite: (path) => path.replace(/^\/health/, ""),
    //   },
    //   "/vente": {
    //     target: "http://51.255.166.155:1353/logAccordsVente/1664/?format=json",
    //     changeOrigin: true,
    //     secure: false,
    //     rewrite: (path) => path.replace(/^\/health/, ""),
    //   },
    // },
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => {
            return tag.startsWith("ion-"); // (return true)
          },
        },
      },
    }),
    Pages({
      nuxtStyle: false,
      pagesDir: [
        {
          dir: "src/views",
          baseRoute: "",
        },
      ],
    }),
    Components({
      /* options */
      dirs: ["src/components"],
      extensions: ["vue"],
      dts: true,
      include: [/\.vue$/, /\.vue\?vue/],
    }),
  ],
});
