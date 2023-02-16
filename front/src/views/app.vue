<script setup lang="ts">
  import axios from "axios";

  const getData = async () => {
    try {
      const data = await axios.get("https://gutendex.com/books/1513/");
      console.log(data);
    } catch (e: any) {
      console.log(e);
    }
  };

  const getDataFlask = async () => {
    try {
      const data = await axios.get("http://localhost:5000/ping");
      console.log(data);
    } catch (e: any) {
      console.log(e);
    }
  };

  console.log("get flask");
  getDataFlask();
</script>

<template><div>We are in the app</div></template>
