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
  let booksData: any;

  const keyword = ref("");
  let tableIndexList: string[] = [];

  /* ----------- MOUNTED ---------- */
  onMounted(async () => {
    isLoading.value = true;
    try {
      booksData = await getBooks("http://127.0.0.1:5000/suggestion");

      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  });

  /* COMPUTED */
  const suggestionData = computed(() => {
    if (!isLoading.value && booksData["suggestion"]) {
      return booksData["suggestion"];
    }
    return [];
  });

  const lastSearchData = computed(() => {
    if (!isLoading.value && booksData["lastSearch"]) {
      return booksData["lastSearch"];
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
      <div>
        <h3>Your last search</h3>
        <div v-if="lastSearchData.length !== 0">
          <BookCard :data="lastSearchData" />
        </div>

        <div v-else class="error-search">
          <h4>You haven't search anything yet.</h4>
        </div>
      </div>
      <div>
        <h3>Suggestion</h3>
        <div v-if="suggestionData.length !== 0">
          <BookCard :data="suggestionData" />
        </div>

        <div v-else class="error-search">
          <h4>No suggestion for now.</h4>
        </div>
      </div>
    </div>
  </div>
</template>
