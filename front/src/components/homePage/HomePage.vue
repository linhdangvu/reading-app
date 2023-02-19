<script setup lang="ts">
  import axios from "axios";
  import {
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardSubtitle,
    IonCardTitle,
    IonChip,
    IonSearchbar,
    IonSkeletonText,
    IonItem,
    IonList,
    IonLabel,
    IonSpinner,
  } from "@ionic/vue";
  import { onMounted, watchEffect } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  import sleep from "../../utils/sleep";
  import checkTextLong from "../../utils/useText";
  import { getBooks } from "../../../src/composable/useApi";

  /* INITIAL VARIABLE */
  const isLoading = ref(true);
  const loadingTableIndex = ref(false);
  const showSuggestion = ref(false);
  const search = ref("");
  const inputSearch = ref("");
  let booksData: any[] | string = [];
  const keyword = ref("");
  let tableIndexList: string[] = [];

  /* ----------- MOUNTED ---------- */
  onMounted(async () => {
    isLoading.value = true;
    try {
      booksData = await getBooks("http://127.0.0.1:5000/getbooks");
      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  });

  /* COMPUTED */
  const allBooksData = computed(() => {
    if (!isLoading.value) {
      // console.log(booksData);
      if (booksData === "NOT_FOUND") {
        return [];
      }
      return booksData;
    }
    return [];
  });

  watchEffect(() => {
    console.log(search.value);
  });
</script>

<template>
  <div>
    <div class="book-loading" v-if="isLoading">
      <ion-spinner name="lines-sharp"></ion-spinner>
    </div>
    <div v-else>
      <div v-if="allBooksData.length !== 0" class="book-cards">
        <ion-card v-for="item in allBooksData" :key="item.id" class="book-card">
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
      <div v-else>
        <h4>No books found</h4>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .book-loading {
    margin: 50% auto;
    text-align: center;
  }

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
