import {
  createRouter as createClientRouter,
  createWebHistory,
} from "vue-router";

/**
 * routes are generated using vite-plugin-pages
 * each .vue files located in the ./src/pages are registered as a route
 * @see https://github.com/hannoeru/vite-plugin-pages
 */
// import routes from "pages-generated";
import routes from "~pages";

console.log(routes);

export function createRouter() {
  const router = createClientRouter({
    history: createWebHistory(),
    routes,
  });

  return router;
}
