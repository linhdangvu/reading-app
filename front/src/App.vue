<script setup lang="ts">
  import {
    IonPage,
    IonTabs,
    IonRouterOutlet,
    IonTabBar,
    IonTabButton,
    IonLabel,
    IonIcon,
  } from "@ionic/vue";

  import { radio, library, search, home } from "ionicons/icons";
  import { useRoute } from "vue-router";
  const route = useRoute();
</script>

<template>
  <ion-page :key="route.fullPath">
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="home" href="/home">
          <ion-icon :icon="home" />
          <ion-label>Home</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="library" href="/ranking">
          <ion-icon :icon="library" />
          <ion-label>Ranking</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="suggest" href="/suggest">
          <ion-icon :icon="radio" />
          <ion-label>Suggest</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="search" href="/search">
          <ion-icon :icon="search" />
          <ion-label>Search</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>
