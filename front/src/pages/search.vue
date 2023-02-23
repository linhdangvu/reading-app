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
        <ion-title>Search</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <SearchPage />
    </ion-content>
  </ion-page>
</template>
