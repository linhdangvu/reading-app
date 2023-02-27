<script setup lang="ts">
  import {
    IonSearchbar,
    IonSkeletonText,
    IonItem,
    IonList,
    IonLabel,
    IonSpinner,
    IonCard,
  } from "@ionic/vue";
  import { onMounted } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  import sleep from "../../utils/sleep";
  import { getBooks, sendData } from "../../composable/useApi";
  import { useRanking } from "../../stores/ranking";
  import { levenshteinDistance } from "../../utils/leveashtein";
  import { CFA_STUDENTS_HOST } from "../../stores/host";

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
      tableIndexList = await getBooks(CFA_STUDENTS_HOST + "/tableindex");
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
      // Search books with cosine
      booksData = await getBooks(CFA_STUDENTS_HOST + "/searchbook/" + words);
      // console.log(booksData);

      // send history search
      if (booksData !== "NOT_FOUND") {
        await sendData(CFA_STUDENTS_HOST + "/searchdata", {
          word: words,
        });
        rank.setLoadingRank(true);

        // save to local storage
        localStorage.setItem("last_search", words);
      }

      await sleep(10);
      isLoading.value = false;
      await getSearchData();
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
      const lastSearch = localStorage.getItem("last_search");
      console.log(lastSearch);
      if (lastSearch) {
        lastSearchList = await getBooks(
          CFA_STUDENTS_HOST + "/searchbook/" + lastSearch
        );
      }
      console.log(lastSearchList);
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

  const autoCompleteData = computed(() => {
    if (search.value && searchData.value.length === 0) {
      // do auto comptele
      const filterDistance = allTableIndexData.value.map((item: string) => {
        return {
          word: item,
          distance: levenshteinDistance(search.value, item),
        };
      });

      filterDistance.sort((a: any, b: any) => a.distance - b.distance);

      // console.log("Check", filterDistance);
      return filterDistance.length > 5
        ? filterDistance.slice(0, 5)
        : filterDistance;
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

      <div v-else-if="autoCompleteData.length !== 0 && searchData.length === 0">
        <h5 class="search-title">Do you mean this word ?</h5>
        <ion-list>
          <ion-item
            button
            v-for="(item, id) in autoCompleteData"
            :key="id"
            @click="handleClickSearch(item.word)"
          >
            <ion-label>{{ item.word }}</ion-label>
          </ion-item>
        </ion-list>
      </div>
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
      <div class="book-cards" v-if="allBooksData.length !== 0">
        <ion-card v-for="item in allBooksData" :key="item.id">
          <BookCard :data="item" />
        </ion-card>
      </div>
      <div v-else class="error-search">
        <h4>{{ errorSearch }}</h4>
      </div>
    </div>

    <h3 class="search-title">Your last search</h3>
    <div v-if="!loadingLastSearch">
      <div
        class="book-cards"
        v-if="lastSearchList && lastSearchData.length !== 0"
      >
        <ion-card v-for="item in lastSearchData" :key="item.id">
          <BookCard :data="item" />
        </ion-card>
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

<style scoped>
  .search-title {
    font-weight: 800;
    text-align: center;
  }
</style>
