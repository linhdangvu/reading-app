<script setup lang="ts">
  import { onMounted } from "@vue/runtime-core";
  import { useRouter } from "vue-router";

  const router = useRouter();

  onMounted(() => {
    router.push({ name: "home" });
  });
</script>

<template>
  <div></div>
</template>
