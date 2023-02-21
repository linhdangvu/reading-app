<script setup lang="ts">
  import checkTextLong from "../../utils/useText";
  import { Book } from "/@src/interfaces/books.interface";
  import {
    IonCard,
    IonCardHeader,
    IonCardContent,
    IonCardSubtitle,
    IonCardTitle,
  } from "@ionic/vue";

  const props = defineProps<{
    data: Book[];
  }>();
</script>
<template>
  <div class="book-cards">
    <ion-card v-for="item in props.data" :key="item.id" class="book-card">
      <img
        v-if="item.formats"
        :alt="item.title"
        :src="item.formats['image/jpeg']"
      />
      <ion-card-header>
        <ion-card-title v-if="item.title">{{
          checkTextLong(item.title)
        }}</ion-card-title>
        <ion-card-subtitle v-if="item.authors">{{
          item.authors.length !== 0 ? item.authors[0].name : "No author"
        }}</ion-card-subtitle>
      </ion-card-header>
    </ion-card>
  </div>
</template>

<style lang="scss">
  .book-cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;

    .book-card {
      width: 140px;

      img {
        width: 100%;
        height: 200px;
        border: solid 1px black;
      }

      ion-card-title {
        font-size: 1rem;
      }

      ion-card-subtitle {
        font-size: 0.8rem;
      }
    }
  }
</style>
