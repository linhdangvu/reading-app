<script setup lang="ts">
  import {
    IonContent,
    IonButton,
    IonButtons,
    IonBackButton,
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
        <ion-buttons slot="start">
          <ion-back-button></ion-back-button>
        </ion-buttons>
        <ion-title>Hot search</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <RankingPage />
    </ion-content>
  </ion-page>
</template>
