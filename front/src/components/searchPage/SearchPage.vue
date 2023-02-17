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
  } from "@ionic/vue";
  import { onMounted, watchEffect } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  import sleep from "../../utils/sleep";

  /* INITIAL VARIABLE */
  let booksData: any[] | string = [];
  const isLoading = ref(true);
  const isSearching = ref(false);
  const search = ref("");

  /* MOUNTED */
  onMounted(async () => {
    isLoading.value = true;
    try {
      booksData = await getBooks("http://127.0.0.1:5000/getbooks");
      isLoading.value = false;
    } catch (e: any) {
      console.log(e);
    }
  });

  /* FUNCTIONS */
  const getBooks = async (url: string) => {
    try {
      const data = await axios.get(url);
      // console.log(data.data);
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

  const handleSearch = async (event: any) => {
    const query = event.target.value.toLowerCase();
    console.log(query);
    isLoading.value = true;
    try {
      await sleep(10);
      booksData = await getBooks("http://127.0.0.1:5000/searchbook/" + query);
      await sleep(10);
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

  watchEffect(() => {
    console.log(allBooksData);
  });
</script>

<template>
  <div>
    <div>
      <ion-textarea
        class="search-textarea"
        placeholder="Paste some text to find"
        :auto-grow="false"
        :height="200"
      >
      </ion-textarea>
    </div>

    <!-- <div class="book-loading" v-if="isLoading">
      <ion-spinner name="lines-sharp"></ion-spinner>
    </div>
    <div v-else>
      <h4>Here is some book have this text:</h4>
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
    </div> -->
  </div>
</template>

<style lang="scss">
  .search-textarea {
    border: solid 1px black;

    .native-textarea {
      height: 200px;
    }
  }

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
