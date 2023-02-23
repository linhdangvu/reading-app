<script setup lang="ts">
  import { IonSpinner, IonCard } from "@ionic/vue";
  import { onMounted } from "@vue/runtime-core";
  import { all } from "axios";
  import { computed, ref } from "vue";
  // import sleep from "../../utils/sleep";
  import { getBooks } from "../../../src/composable/useApi";

  /* INITIAL VARIABLE */
  const isLoading = ref(true);
  let booksData: any[] | string = [];

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
      if (booksData === "NOT_FOUND") {
        return [];
      }
      return booksData;
    }
    return [];
  });
</script>

<template>
  <div>
    <div class="book-loading" v-if="isLoading">
      <ion-spinner name="lines-sharp"></ion-spinner>
    </div>
    <div v-else>
      <h3>Here is the list of {{ allBooksData.length }} books:</h3>
      <div class="book-cards" v-if="allBooksData.length !== 0">
        <ion-card v-for="item in allBooksData" :key="item.id">
          <BookCard :data="item" />
        </ion-card>
      </div>

      <div v-else class="error-search">
        <h4>No books found</h4>
      </div>
    </div>
  </div>
</template>
