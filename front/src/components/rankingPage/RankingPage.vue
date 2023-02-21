<script setup lang="ts">
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
  import {
    onMounted,
    onUnmounted,
    onUpdated,
    watchEffect,
  } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  import sleep from "../../utils/sleep";
  import checkTextLong from "../../utils/useText";
  import { getBooks } from "../../composable/useApi";
  import axios from "axios";
  import { useRanking } from "../../stores/ranking";

  /* INITIAL VARIABLE */
  const isLoading = ref(true);
  let booksData: any[] | string = [];
  const rank = useRanking();

  /* ----------- MOUNTED ---------- */
  onMounted(async () => {
    await getRankingBooks();
  });

  onUnmounted(() => {
    console.log("Ranking is unmount");
  });

  /* FUNCTIONS */
  const getRankingBooks = async () => {
    isLoading.value = true;
    try {
      booksData = await getBooks("http://127.0.0.1:5000/cosine");

      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  };

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

  onUpdated(() => {
    console.log("Update ranking", rank.loadingRank);
  });

  watchEffect(async () => {
    console.log("Watch ranking", rank.loadingRank);
    if (rank.loadingRank) {
      await getRankingBooks();
      rank.setLoadingRank(false);
    }
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
        <h4>There a no ranking for now.</h4>
      </div>
    </div>
  </div>
</template>
