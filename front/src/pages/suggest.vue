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
      <h1>This page for suggestion book ?</h1>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
  import { defineComponent, ref } from "vue";
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
  import AboutModal from "../components/AboutModal.vue";

  export default defineComponent({
    name: "About",
    components: {
      IonHeader,
      IonPage,
      IonButton,
      IonButtons,
      IonBackButton,
      IonContent,
      IonTitle,
      IonToolbar,
      IonModal,
      AboutModal,
    },
    setup() {
      const modalIsOpen = ref(false);
      const showModal = () => {
        modalIsOpen.value = true;
      };

      const closeModal = () => {
        modalIsOpen.value = false;
      };
      return {
        showModal,
        closeModal,
        modalIsOpen,
      };
    },
  });
</script>

<style></style>
