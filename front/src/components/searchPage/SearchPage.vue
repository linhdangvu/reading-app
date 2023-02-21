<script setup lang="ts">
  import {
    IonSearchbar,
    IonSkeletonText,
    IonItem,
    IonList,
    IonLabel,
    IonSpinner,
  } from "@ionic/vue";
  import { onMounted } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  import sleep from "../../utils/sleep";
  import { getBooks, sendSearchData } from "../../composable/useApi";
  import { useRanking } from "../../stores/ranking";

  /* INITIAL VARIABLE */
  const isLoading = ref(true);
  const loadingLastSearch = ref(true);
  const loadingTableIndex = ref(false);
  const search = ref("");
  const inputSearch = ref("");
  let booksData: any[] | string = [];
  let tableIndexList: string[] = [];
  const rank = useRanking();
  const errorSearch = ref("Welcome, let search some books");
  let lastSearchList: any[] = [];

  /* ----------- MOUNTED ---------- */
  onMounted(async () => {
    isLoading.value = true;
    try {
      // booksData = await getBooks("http://127.0.0.1:5000/getbooks");
      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  });

  onMounted(async () => {
    await getSearchData();
  });

  onMounted(async () => {
    loadingTableIndex.value = true;
    try {
      tableIndexList = await getBooks("http://127.0.0.1:5000/tableindex");
      loadingTableIndex.value = false;
    } catch (e: any) {
      console.log(e);
    }
  });

  /* ---------- FUNCTIONS ---------- */
  const searchByWords = async (words: string) => {
    search.value = "";
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
      await getSearchData();
      await sleep(10);
      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  };

  // Doing search with query
  const handleEnterSearch = async (event: any) => {
    const query = event.target.value.toLowerCase();
    if (query === "") {
      errorSearch.value = "Please write something to search";
    } else {
      searchByWords(query);
    }
  };

  const handleClickSearch = async (words: string) => {
    inputSearch.value = words;
    searchByWords(words);
  };

  // Chercher dans table intex
  const handleInputSearch = (event: any) => {
    const query = event.target.value.toLowerCase();
    search.value = query;
  };

  const getSearchData = async () => {
    loadingLastSearch.value = true;
    try {
      const data = await getBooks("http://127.0.0.1:5000/suggestion");
      lastSearchList = data["lastSearch"];
      loadingLastSearch.value = false;
    } catch (e: any) {
      console.log(e);
    }
  };

  /* ---------- COMPUTED ---------- */
  const allBooksData = computed(() => {
    if (!isLoading.value) {
      if (booksData === "NOT_FOUND") {
        errorSearch.value = "NO BOOK FOUND";
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
          return item.match(new RegExp("^" + search.value, "i"));
        });
        return filteredData.length > 5
          ? filteredData.slice(0, 5)
          : filteredData;
      }
    }
    return [];
  });

  const lastSearchData = computed(() => {
    if (!loadingLastSearch.value) {
      return lastSearchList;
    }
    return [];
  });
</script>

<template>
  <div>
    <div v-if="!loadingTableIndex">
      <!-- debounce to to wait 1000 to search -->
      <ion-searchbar
        @ionInput="handleInputSearch($event)"
        @keyup.enter="handleEnterSearch($event)"
        :value="inputSearch"
      ></ion-searchbar>
      <ion-list v-if="searchData.length !== 0">
        <ion-item
          button
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

    <!-- BOOKS LIST -->
    <div class="book-loading" v-if="isLoading">
      <ion-spinner name="lines-sharp"></ion-spinner>
    </div>
    <div v-else>
      <div v-if="allBooksData.length !== 0">
        <BookCard :data="allBooksData" />
      </div>
      <div v-else class="error-search">
        <h4>{{ errorSearch }}</h4>
      </div>
    </div>

    <h3>Your last search</h3>
    <div v-if="!loadingLastSearch">
      <div v-if="lastSearchList && lastSearchData.length !== 0">
        <BookCard :data="lastSearchData" />
      </div>
      <div v-else class="error-search">
        <h4>You haven't search anything yet.</h4>
      </div>
    </div>
    <div v-else class="book-loading">
      <ion-spinner name="lines-sharp"></ion-spinner>
    </div>
  </div>
</template>
