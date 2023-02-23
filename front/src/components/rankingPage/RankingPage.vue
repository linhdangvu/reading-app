<script setup lang="ts">
  import {
    IonSpinner,
    IonSegment,
    IonSegmentButton,
    IonLabel,
    IonCard,
  } from "@ionic/vue";
  import { onMounted, watchEffect } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  // import sleep from "../../utils/sleep";
  import { getBooks } from "../../composable/useApi";
  import { useRanking } from "../../stores/ranking";

  /* INITIAL VARIABLE */
  const isLoading = ref(true);
  const loadindMostRead = ref(true);
  const optionTop = ref("searched");
  let booksData: any[] | string = [];
  let mostReadData: any[] | string = [];
  const rank = useRanking();

  /* ----------- MOUNTED ---------- */
  onMounted(async () => {
    await getRankingBooks();
  });

  onMounted(async () => {
    loadindMostRead.value = true;
    try {
      mostReadData = await getBooks("http://127.0.0.1:5000/mostread");
      loadindMostRead.value = false;
    } catch (e: any) {
      console.log(e);
    }
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
      if (booksData === "NOT_FOUND") {
        return [];
      }
      return booksData;
    }
    return [];
  });

  const allMostRead = computed(() => {
    if (!loadindMostRead.value) {
      return mostReadData;
    }
    return [];
  });

  watchEffect(async () => {
    // console.log("Watch ranking", rank.loadingRank);
    if (rank.loadingRank) {
      await getRankingBooks();
      rank.setLoadingRank(false);
    }

    console.log(optionTop.value);
  });
</script>

<template>
  <div>
    <ion-segment :value="optionTop">
      <ion-segment-button value="searched" @click="optionTop = 'searched'">
        <ion-label>Most searched</ion-label>
      </ion-segment-button>
      <ion-segment-button value="read" @click="optionTop = 'read'">
        <ion-label>Most read</ion-label>
      </ion-segment-button>
    </ion-segment>
    <div v-if="optionTop === 'searched'" :key="optionTop">
      <div class="book-loading" v-if="isLoading">
        <ion-spinner name="lines-sharp"></ion-spinner>
      </div>
      <div v-else>
        <div class="book-cards" v-if="allBooksData.length !== 0">
          <ion-card v-for="item in allBooksData" :key="item.id">
            <BookCard :data="item" />
          </ion-card>
        </div>
        <div v-else class="error-search">
          <h4>There are no data for most searched for now.</h4>
        </div>
      </div>
    </div>

    <div v-if="optionTop === 'read'" :key="optionTop">
      <div class="book-loading" v-if="loadindMostRead">
        <ion-spinner name="lines-sharp"></ion-spinner>
      </div>
      <div v-else>
        <div class="book-cards" v-if="allMostRead.length !== 0">
          <ion-card v-for="item in allMostRead" :key="item.id">
            <BookCard :data="item" />
          </ion-card>
        </div>
        <div v-else class="error-search">
          <h4>There are no data for most read for now.</h4>
        </div>
      </div>
    </div>
  </div>
</template>
