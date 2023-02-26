<script setup lang="ts">
  import checkTextLong from "../../utils/useText";
  import { Book } from "../../../src/interfaces/books.interface";
  import {
    IonCard,
    IonCardHeader,
    IonCardContent,
    IonCardSubtitle,
    IonCardTitle,
    IonModal,
    IonToolbar,
    IonHeader,
    IonButton,
    IonButtons,
    IonTitle,
    IonContent,
    IonItem,
    IonSpinner,
    createAnimation,
  } from "@ionic/vue";
  import { reactive, ref } from "vue";
  import axios from "axios";
  import { sendData } from "../../composable/useApi";
  import sleep from "../../utils/sleep";
  import { CFA_STUDENTS_HOST } from "../../../src/stores/host";

  const props = defineProps<{
    data: Book;
  }>();

  const openReading = ref(false);
  const loadingBook = ref(false);
  const book = reactive<any>({
    id: 0,
    name: "",
    author: "",
    content: "",
    link: "",
  });

  const setOpenReading = (status: boolean) => {
    openReading.value = status;
  };

  const enterAnimation = (baseEl: HTMLElement | any) => {
    const root = baseEl.shadowRoot;

    if (root !== null) {
      const backdropAnimation = createAnimation()
        .addElement(root.querySelector("ion-backdrop"))
        .fromTo("opacity", "0.01", "var(--backdrop-opacity)");

      const wrapperAnimation = createAnimation()
        .addElement(root.querySelector(".modal-wrapper"))
        .keyframes([
          { offset: 0, opacity: "0", transform: "scale(0)" },
          { offset: 1, opacity: "0.99", transform: "scale(1)" },
        ]);

      return createAnimation()
        .addElement(baseEl)
        .easing("ease-out")
        .duration(120)
        .addAnimation([backdropAnimation, wrapperAnimation]);
    }
  };

  const leaveAnimation = (baseEl: any) => {
    return enterAnimation(baseEl)?.direction("reverse");
  };

  const getAuthors = (authors: any) => {
    const authorsData: any = [];
    if (authors) {
      authors.forEach((item: any) => {
        if (item.name) {
          authorsData.push(item.name);
        }
      });
      if (authorsData.length === 0) {
        return "No author";
      }
      return authorsData.join(" & ");
    }
    return "No author";
  };

  const readBook = async () => {
    book.id = props.data.id;
    book.name = props.data.title;
    book.author = getAuthors(props.data.authors);

    try {
      loadingBook.value = true;
      await sendData(CFA_STUDENTS_HOST + "/clickedbooks", {
        bookId: props.data.id,
      });
      await sleep(10);
      const data = await sendData(CFA_STUDENTS_HOST + "/readbookcontent", {
        bookId: props.data.id,
      });
      // console.log(data);
      book.content = data.textHtml;
      book.link = data.link;
      loadingBook.value = false;
    } catch (e: any) {
      console.log(e);
    }
    // }
  };
</script>
<template>
  <div
    class="book-card"
    @click="
      readBook();
      setOpenReading(true);
    "
  >
    <img
      v-if="props.data.formats"
      :alt="props.data.title"
      :src="props.data.formats['image/jpeg']"
    />
    <ion-card-header>
      <ion-card-title v-if="props.data.title">{{
        checkTextLong(props.data.title)
      }}</ion-card-title>
      <ion-card-subtitle v-if="props.data.authors">{{
        getAuthors(props.data.authors)
      }}</ion-card-subtitle>
    </ion-card-header>
    <!-- <ion-button expand="block" @click="setOpenReading(true)">Open</ion-button> -->
    <div style="width: 100%">
      <ion-modal
        class="my-modal"
        :is-open="openReading"
        :enter-animation="enterAnimation"
        :leave-animation="leaveAnimation"
      >
        <ion-header>
          <ion-toolbar>
            <ion-title>{{ book.name }}</ion-title>
            <ion-buttons slot="end">
              <ion-button @click="setOpenReading(false)">Close</ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>
        <ion-content class="ion-padding">
          <div class="init-book">
            <p>
              <span>Title:</span> <span>{{ props.data.title }}</span>
            </p>
            <p>
              <span>Author:</span>
              <span> {{ getAuthors(props.data.authors) }}</span>
            </p>
            <p>
              <span>ID:</span> <span>{{ props.data.id }}</span>
            </p>
            <p>
              <span>Link:</span>
              <span>
                <div v-if="!loadingBook">
                  <a :href="book.link" target="_blank">Go to link</a>
                </div>
                <ion-spinner v-else name="lines-sharp"></ion-spinner>
              </span>
            </p>
          </div>
          <div class="book-loading" v-if="loadingBook">
            <ion-spinner name="lines-sharp"></ion-spinner>
          </div>
          <div v-else class="book-content" v-html="book.content"></div>

          <div style="width: 100%; height: 50px"></div>
        </ion-content>
      </ion-modal>
    </div>
  </div>
</template>

<style lang="scss">
  .my-modal {
    &::part(content) {
      width: 100%;
      height: 100vh;
    }
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

    .book-card:hover {
      cursor: pointer;
    }
  }

  .init-book {
    border: solid 1px black;
    padding: 10px;
    margin: 5px auto;

    p {
      // text-align: center;
      margin: 5px;
      justify-content: space-between;
      display: flex;
      flex-wrap: wrap;

      span:first-child {
        font-weight: 800;
      }
    }
  }

  .book-content {
    width: 90%;
    // margin: 10px;
  }

  .ion-padding {
    height: 90vh;
  }
</style>
