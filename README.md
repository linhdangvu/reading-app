# Project Reading App

Sujet: https://www-apr.lip6.fr/~buixuan/files/mrecinsta2022/mrec_projet.pdf

### Partie Back

- Pour aller dans environement

  ```
  cd back/
  ```

- Pour aller dans environement ( for Mac )

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
  flask run --host=172.16.8.38 --port=5000
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

### Netcat connection (same wireless)

- For Mac

1. Go to Terminal and type: `ìfconfig` and find the line below:

   > inet **172.16.8.27** netmask 0xffffff00 broadcast 172.16.8.255

2. Share Back for everyone have the same wireless by using netcat

   - Host: **172.16.8.27**
   - Port: **5000**

   ```
   nc -v 172.16.8.27 5000
   ```

3. Share BFrontack for everyone have the same wireless by using netcat

   - Host: **172.16.8.27**
   - Port: **5173**

   ```
   nc -v 172.16.8.27 5173
   ```

   > ##### Remarque:
   >
   > - Back & Front can't use the same port
