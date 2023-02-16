<script setup lang="ts">
  import axios from "axios";
  import {
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardSubtitle,
    IonCardTitle,
    IonChip,
  } from "@ionic/vue";
  import { onMounted } from "@vue/runtime-core";
  import { computed, ref } from "vue";

  /* INITIAL VARIABLE */
  let booksData: any[] = [];
  const isLoading = ref(true);

  /* MOUNTED */
  onMounted(async () => {
    isLoading.value = true;
    try {
      booksData = await getBooks();
      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  });

  /* FUNCTIONS */
  const getBooks = async () => {
    try {
      const data = await axios.get("http://127.0.0.1:5000/getbooks");
      return data.data;
    } catch (e: any) {
      console.log(e);
      return [];
    }
  };

  const checkTextLong = (text: string) => {
    if (text.split("").length >= 50) {
      return text.slice(0, 51) + "...";
    }
    return text;
  };

  /* COMPUTED */
  const allBooksData = computed(() => {
    if (!isLoading.value) {
      return booksData;
    }
    return [];
  });
</script>

<template>
  <div v-if="allBooksData.length === 0">Loading ...</div>
  <div v-else>
    <div>Keywords: <ion-chip :outline="true">Outline</ion-chip></div>
    <div class="book-cards">
      <ion-card v-for="item in allBooksData" :key="item.id" class="book-card">
        <img :alt="item.title" :src="item.formats['image/jpeg']" />
        <ion-card-header>
          <ion-card-title>{{ checkTextLong(item.title) }}</ion-card-title>
          <ion-card-subtitle>{{ item.authors[0].name }}</ion-card-subtitle>
        </ion-card-header>
      </ion-card>
    </div>
  </div>
</template>

<style scoped lang="scss">
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

  /* iOS places the subtitle above the title */
  ion-card-header.ios {
    display: flex;
    flex-flow: column-reverse;
  }
</style>
