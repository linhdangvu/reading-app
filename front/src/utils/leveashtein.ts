export const levenshteinDistance = (word1 = "", word2 = "") => {
  const sizeN = word1.length;
  const sizeM = word2.length;

  //créer un tableau vide
  // initialisation des indices lignes et colonnes de taille sizeN, sizeM
  const matrice = Array(sizeM + 1)
    .fill(null)
    .map(() => Array(sizeN + 1).fill(null));

  // remplissage de la première ligne du tableau (1,2,3,...,n)
  for (let i = 0; i <= sizeN; i += 1) {
    matrice[0][i] = i;
  }

  // remplissage de la première colonne du tableau (1,2,3,...,m)
  for (let j = 0; j <= sizeM; j += 1) {
    matrice[j][0] = j;
  }

  // Doing some transition
  for (let j = 1; j <= sizeM; j += 1) {
    for (let i = 1; i <= sizeN; i += 1) {
      // si les lettres sont les mêmes on rajoute 1 à l'algo
      const indicator = word1[i - 1] === word2[j - 1] ? 0 : 1;
      matrice[j][i] = Math.min(
        matrice[j][i - 1] + 1, // deletion
        matrice[j - 1][i] + 1, // insertion
        matrice[j - 1][i - 1] + indicator // substitution
      );
    }
  }
  return matrice[sizeM][sizeN];
};
