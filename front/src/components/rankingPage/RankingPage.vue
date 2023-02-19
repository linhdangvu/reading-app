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
        <h4>There a no ranking for now.</h4>
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
</style>
