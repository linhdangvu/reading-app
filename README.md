# Project Reading App

Sujet: https://www-apr.lip6.fr/~buixuan/files/mrecinsta2022/mrec_projet.pdf

### Partie Back

- Pour aller dans environement

  ```
  cd back/
  ```

- Pour aller dans environement

  ```
  source .env/bin/activate
  ```

- Pour installer des libraries

  ```
  pip install -r requirements.txt
  ```

- Pour executer l'application

  ```
  export FLASK_APP=app
  export FLASK_ENV=development
  flask run
  ```

### Partie Front

- Pour aller dans environement

  ```
  cd front/
  ```

- Pour installer des libraries

  ```
  npm install
  ```

  ou

  ```
  yarn install
  ```

- Pour executer l'application

  ```
  npm run dev
  ```

  ou

  ```
  yarn dev
  ```

<!-- ##### Ne concerne pas

Installing env Python
`virtualenv .env` -->

awk -F "[]"

Une fonctionnalite implicite de classement : ´ Classement des reponses des deux fonctionnalit ´ es de recherche ´ prec´ edentes. A la suite d’une r ´ eponse ´ a la fonctionnalit `e recherche, l’application retourne la liste des documents ´ triee par un certain crit ´ ere de pertinence : par nombre d’occurrences du mot-clef dans le document; par indice de` centralite d ´ ecroissant dans le graphe de Jaccard, et cetera. Le crit ´ ere de centralit `e est laiss ´ e libre ´ a chaque groupe`
d’interpreter. Cependant, il est obligatoire d’utiliser au moins un crit ´ ere parmi les trois indices vu en cours, `a savoir` closeness, betweenness, ou pagerank. Concernant l’indice de centralite utilis ´ e, il est ´ egalement important de bien ´ le decrire dans le rapport. On veillera en particulier ´ a expliciter la d ` efinition, le calcul, ainsi que le r ´ esultat de cet ´ indice sur des extraits pertinents de quelques livres parmi les > 1664 livres presents dans la base de donn ´ ees.
