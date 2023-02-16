<script setup lang="ts">
  import { defineComponent } from "vue";
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
      <h1>Home</h1>
      <!-- <ion-button router-link="/about">About</ion-button> -->
    </ion-content>
  </ion-page>
</template>
