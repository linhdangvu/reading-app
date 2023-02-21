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
        <ion-title>Suggestion</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <SuggestionPage />
    </ion-content>
  </ion-page>
</template>
