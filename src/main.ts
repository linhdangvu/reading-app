// import { createApp } from "vue";

import { createApp as createClientApp, h, Suspense } from "vue";
import App from "./App.vue";
import { createRouter } from "./router";

import { IonicVue } from "@ionic/vue";

/* Core CSS required for Ionic components to work properly */
import "@ionic/vue/css/core.css";

/* Basic CSS for apps built with Ionic */
import "@ionic/vue/css/normalize.css";
import "@ionic/vue/css/structure.css";
import "@ionic/vue/css/typography.css";

/* Optional CSS utils that can be commented out */
import "@ionic/vue/css/padding.css";
import "@ionic/vue/css/float-elements.css";
import "@ionic/vue/css/text-alignment.css";
import "@ionic/vue/css/text-transformation.css";
import "@ionic/vue/css/flex-utils.css";
import "@ionic/vue/css/display.css";

/* Theme variables - copied from existing project */
import "./theme/variables.css";

async function createApp() {
  // const head = createHead();
  //   const i18n = createI18n()
  const router = createRouter();
  //   const pinia = createPinia()

  const app = createClientApp({
    // This is the global app setup function
    setup() {
      return () => {
        return h(Suspense, null, {
          default: () => h(App),
        });
      };
    },
  });

  const ReadingApp = {
    app,
    router,
    // head,
  };

  app.use(ReadingApp.router);
  app.use(IonicVue);

  return ReadingApp;
}

createApp().then(async (ReadingApp) => {
  // wait for the app to be ready
  await ReadingApp.router.isReady();

  // finaly mount the app to the DOM
  ReadingApp.app.mount("#app");
});
