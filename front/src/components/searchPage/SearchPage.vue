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
  import { onMounted, watchEffect } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  import sleep from "../../utils/sleep";
  import { getBooks, sendSearchData } from "../../composable/useApi";
  import axios from "axios";
  import { useRanking } from "../../stores/ranking";

  /* INITIAL VARIABLE */
  const isLoading = ref(true);
  const loadingTableIndex = ref(false);
  const showSuggestion = ref(false);
  const search = ref("");
  const inputSearch = ref("");
  let booksData: any[] | string = [];
  const keyword = ref("");
  let tableIndexList: string[] = [];
  const rank = useRanking();

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

  onMounted(async () => {
    loadingTableIndex.value = true;
    try {
      tableIndexList = await getBooks("http://127.0.0.1:5000/tableindex");
      // console.log(tableIndexList);
      loadingTableIndex.value = false;
    } catch (e: any) {
      console.log(e);
    }
  });

  /* FUNCTIONS */
  const checkTextLong = (text: string) => {
    if (text.split("").length >= 50) {
      return text.slice(0, 51) + "...";
    }
    return text;
  };

  const searchByWords = async (words: string) => {
    isLoading.value = true;
    try {
      await sleep(10);
      booksData = await getBooks("http://127.0.0.1:5000/searchbook/" + words);
      // console.log(booksData);
      if (booksData !== "NOT_FOUND") {
        await sendSearchData("http://127.0.0.1:5000/searchdata", words);
        rank.setLoadingRank(true);
      }
      await sleep(10);
      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  };

  // Doing search with query
  const handleEnterSearch = async (event: any) => {
    const query = event.target.value.toLowerCase();
    search.value = "";
    searchByWords(query);
  };

  const handleClickSearch = async (words: string) => {
    inputSearch.value = words;
    search.value = "";
    searchByWords(words);
  };

  // Chercher dans table intex
  const handleInputSearch = (event: any) => {
    const query = event.target.value.toLowerCase();
    search.value = query;
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

  const allTableIndexData = computed(() => {
    if (!loadingTableIndex.value && tableIndexList.length !== 0) {
      return tableIndexList;
    }
    return [];
  });

  const searchData = computed(() => {
    if (allTableIndexData.value.length !== 0) {
      if (!search.value) {
        return [];
      } else {
        const filteredData = allTableIndexData.value.filter((item: string) => {
          return item.match(new RegExp(search.value, "i"));
        });
        return filteredData.length > 5
          ? filteredData.slice(0, 5)
          : filteredData;
      }
    }
    return [];
  });

  watchEffect(() => {
    console.log("watch from search", rank.loadingRank.value);
  });
</script>

<template>
  <div>
    <div v-if="!loadingTableIndex">
      <!-- debounce to to wait 1000 to search       -->
      <ion-searchbar
        @ionInput="handleInputSearch($event)"
        @keyup.enter="handleEnterSearch($event)"
        :value="inputSearch"
      ></ion-searchbar>
      <ion-list v-if="searchData.length !== 0">
        <ion-item
          v-for="item in searchData"
          :key="item"
          @click="handleClickSearch(item)"
        >
          <ion-label>{{ item }}</ion-label>
        </ion-item>
      </ion-list>
    </div>
    <div v-else>
      <ion-skeleton-text
        :animated="true"
        style="padding: 16px; width: 93%; margin: 0 auto"
      ></ion-skeleton-text>
    </div>

    <div class="book-loading" v-if="isLoading">
      <ion-spinner name="lines-sharp"></ion-spinner>
    </div>
    <div v-else>
      <div v-if="allBooksData.length !== 0" class="book-cards">
        <ion-card v-for="item in allBooksData" :key="item.id" class="book-card">
          <img :alt="item.title" :src="item.formats['image/jpeg']" />
          <ion-card-header>
            <ion-card-title>{{ checkTextLong(item.title) }}</ion-card-title>
            <ion-card-subtitle>{{
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
</style>
