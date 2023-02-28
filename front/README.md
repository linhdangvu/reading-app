### This is the Front of the reading app

- **Framework + Langage**: Vue + Vite + Ionic + Typescript

Dans cette application **READING APP**, on prends des livres depuis le **Back**

- Pour la partie **Home**:
  > On récupéré tous les livres de **Back**
  > On peut cliquer sur les livres pour lire
- Pour la partie **Top 10** ( le classement ):
  > On récupére top 10 livres qui ont le plus cherché par mots clés (cosine simalirity)
  > On récupére aussi top 10 livres qui ont le plus lu par le nombre de cliqué.
- Pour la partie **Suggestion**:
  > On envoie la dernière mot-clé au Back et revoie la list de suggestion par la closeness centrality (on prends juste 2 livres à côté)
- Pour la partie **Search**:
  > On utilise **RegEx** et l'algorithme **Levenshtein** pour faire le filtre de l'auto-completeion
  > On sauvegarde la dernière mot-clé dans **localStorage**.
