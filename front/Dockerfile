FROM node:lts-alpine
WORKDIR /front

# copie 'package.json' et 'package-lock.json' (si disponible)
COPY package*.json ./

# installe les dépendances du projet
RUN npm install


# RUN npm run dev
# copie les fichiers et dossiers du projet dans le dossier de travail (par exemple : le dossier 'app')
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev"]