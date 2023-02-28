### Le Back de reading app

- **Framework + Langage**: Flask + Python

Dans le **Back** de **READING APP**:

- On prends 182 livres en utilise des identité de books de 0 à 199 + 2 livres qu'on apprend dans le cours (49345, 56667) depuis [Gutendex](https://gutendex.com/)
- On construit la **table d'indexage** depuis des contents des livres en utilisant la **RegEx**
- On trie le **nombre de cliqués** des livres pour le **classement** (Top 10 most read)
- On calcule et trie la **Cosine Simalirity** pour le **classement** (Top 10 most search)
- On calcule la **Closeness Centrality** pour la **suggestion**
