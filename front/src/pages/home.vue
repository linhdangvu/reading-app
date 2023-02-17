<script setup lang="ts">
  import {
    IonContent,
    IonButton,
    IonPage,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonCard,
    IonCardContent,
  } from "@ionic/vue";
</script>

<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Home</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <HomePage />
    </ion-content>
  </ion-page>
</template>
