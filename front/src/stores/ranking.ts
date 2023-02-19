import { ref } from "vue";

export const useRanking = () => {
  const loadingRank = ref(false);

  const setLoadingRank = (val: boolean) => {
    loadingRank.value = val;
  };

  return {
    loadingRank,
    setLoadingRank,
  };
};
