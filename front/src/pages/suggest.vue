<script setup lang="ts">
  import {
    IonContent,
    IonPage,
    IonHeader,
    IonTitle,
    IonToolbar,
  } from "@ionic/vue";
</script>

<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>From your last searched...</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <SuggestionPage />
    </ion-content>
  </ion-page>
</template>
