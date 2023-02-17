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
    IonModal,
  } from "@ionic/vue";
  // import AboutModal from "../components/AboutModal.vue";
</script>

<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button></ion-back-button>
        </ion-buttons>
        <ion-title>Library</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <h1>This page for reading book ?</h1>
      <!-- MODAL CODE -->
    </ion-content>
  </ion-page>
</template>
