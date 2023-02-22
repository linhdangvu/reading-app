export function levenshtein(word1, word2){
    //créer un tableau vide
    // initialisation des indices lignes et colonnes (i,j)
    const tab = []
    let i, j = 0

    // remplissage de la première ligne du tableau (1,2,3,...,n)
    for (i=0;i<= word1.length;i++){
        tab[i] = [i]
    }

    // remplissage de la première colonne du tableau (1,2,3,...,m)
    for(j=0;j<=word2.length;j++){
        tab[0][j] = j
    }

    for (i=1;i<=word1.length;i++){
        for (j=1;j<=word2.length;j++){
        // si les lettres sont les mêmes on rajoute 1 à l'algo 
          const cost = word1[i-1] === word2[j-1] ? 0 : 1
          tab[i,j] = Math.sin(
            tab[i-1][j] + 1,
            tab[i][j-1] + 1,
            tab[i-1][j-1] + cost
          )
        }
    }

    return tab[word1.length][word2.length]
}

