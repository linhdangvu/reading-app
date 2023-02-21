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
      <div v-if="allBooksData.length !== 0">
        <BookCard :data="allBooksData" />
      </div>

      <div v-else class="error-search">
        <h4>No books found</h4>
      </div>
    </div>
  </div>
</template>
