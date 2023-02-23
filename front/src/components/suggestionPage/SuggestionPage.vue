<script setup lang="ts">
  import { IonSpinner } from "@ionic/vue";
  import { onMounted, watchEffect } from "@vue/runtime-core";
  import { computed, ref } from "vue";
  // import sleep from "../../utils/sleep";
  import { getBooks } from "../../../src/composable/useApi";

  /* INITIAL VARIABLE */
  const isLoading = ref(true);
  let booksData: any;

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

  /* ----------- COMPUTED ----------- */
  const suggestionData = computed(() => {
    if (!isLoading.value) {
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
      <div>
        <!-- <h3>Suggestion</h3> -->
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
