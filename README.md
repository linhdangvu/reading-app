# Project Reading App

Sujet: https://www-apr.lip6.fr/~buixuan/files/mrecinsta2022/mrec_projet.pdf

### Partie Back

- Pour aller dans environement

  ```
  cd back/
  ```

- Pour aller dans environement

  ```
  virtualenv .env
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
  flask run --host=0.0.0.0 --port=5000
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
  npm run dev --host 172.16.8.27
  ```

  ou

  ```
  yarn dev
  ```

<!-- ##### Ne concerne pas

Installing env Python
`virtualenv .env` -->
