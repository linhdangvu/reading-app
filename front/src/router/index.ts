import { createRouter, createWebHistory } from "@ionic/vue-router";
// import { RouteRecordRaw } from "vue-router";

import routes from "~pages";

// const routes: Array<RouteRecordRaw> = [
//   {
//     path: "/",
//     redirect: "/home",
//   },
//   {
//     path: "/home",
//     component: Home,
//   },
//   {
//     path: "/about",
//     component: About,
//   },
//   {
//     path: "/search",
//     component: Search,
//   },
// ];
console.log(routes);

// https://vitejs.dev/guide/env-and-mode.html
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
