# Test Technique Hoortrade

## Cinema
Création d'une application Django nommée **Cinema**.

---

## Pré-requis techniques

- Python ≥ 3.12  
- Django ≥ 4.2  
- Django REST Framework ≥ 3.15.2  
- PostgreSQL  
- Docker + docker-compose  

---

## 🚀 Lancer le projet

### 1. Cloner le dépôt
```bash
git clone https://github.com/AlexianeBA/Cinema_Hoort/
cd Cinema
```

### 2. Configurer les variables d’environnement

Crée un fichier `.env` dans le dossier `cinema/` (exemple minimal) :
```
TMDB_API_KEY=your-secret-key
DJANGO_SECRET_KEY=your-secret-key
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=
```

### 3. Construire et démarrer le conteneurs Docker de la database

```bash
docker-compose up -d db
```

### 4. Appliquer les migrations Django

```bash
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

### 5. Importer les données via l'appel à l'API TMDB

```bash
docker-compose run web python manage.py import_tmdb
```

### 6. Créer un superutilisateur (optionnel, pour l’admin Django)

```bash
docker-compose run web python manage.py createsuperuser
```

### 7. Lancer le serveur web

```bash
docker-compose up web
```


### 8. Accéder à l’application

- **API** : [http://localhost:8000/](http://localhost:8000/)
- **Admin Django** : [http://localhost:8000/admin/](http://localhost:8000/admin/)


### 8. Arrêter les conteneurs

```bash
docker-compose down
```

---

## Authentification

L’API utilise JWT pour sécuriser les endpoints nécessitant une authentification.

- **Obtenir un token** :  
  `POST http://localhost:8000/api/token/`  
  Body : `{ "username": "...", "password": "..." }`

- **Rafraîchir un token** :  
  `POST http://localhost:8000/api/token/refresh/`  
  Body : `{ "refresh": "<refresh_token>" }`

  - **Déconnexion (JWT)**  
  `POST http://localhost:8000/api/logout/`  
  Body : `{ "refresh": "<refresh_token>" }`  
  > Cette opération blackliste le refresh token côté serveur.  
  > L’access token reste valide jusqu’à son expiration naturelle.

**À chaque requête protégée, ajoute le header :**
```
Authorization: Bearer <votre_token_jwt>
```

---

## Endpoints principaux

### 🎞️ Films

- **Liste des films**  
  `GET /api/movies/`
- **Filtrer par statut**  
  `GET /api/movies/by-status/?status=<statut>`
- **Détail d’un film**  
  `GET /api/movies/<id>/`
- **Mettre à jour un film**  
  `PUT/PATCH /api/movies/<id>/`
- **Archiver un film**  
  `PATCH /api/movies/<id>/archive/`

#### Filtres d’origine
- Films créés depuis l’admin :  
  `GET /api/movies/?source=manual`
- Films importés depuis TMDb :  
  `GET /api/movies/?source=tmdb`

---

### 👤 Auteurs

- **Liste des auteurs**  
  `GET /api/authors/`
- **Détail d’un auteur**  
  `GET /api/authors/<id>/`
- **Mettre à jour un auteur**  
  `PUT/PATCH /api/authors/<id>/`
- **Supprimer un auteur**  
  `DELETE /api/authors/<id>/`

#### Filtres d’origine
- Auteurs créés depuis l’admin :  
  `GET /api/authors/?source=manual`
- Auteurs importés depuis TMDb :  
  `GET /api/authors/?source=tmdb`

---

### ⭐ Favoris

- **Ajouter un film aux favoris**  
  `POST /api/favorites/<movie_id>/add/`
- **Retirer un film des favoris**  
  `DELETE /api/favorites/<movie_id>/remove/`
- **Lister mes films favoris**  
  `GET /api/favorites/my-favorites/`

---

### 📝 Notations

- **Noter un film**  
  `POST /api/rating/<movie_id>/add-to-movie/`
- **Noter un auteur**  
  `POST /api/rating/<author_id>/add-to-author/`

---

### 🔐 Authentification & Utilisateurs

- **Inscription**  
  `POST /api/users/register/`
- **Connexion (interface DRF)**  
  `POST /api-auth/login/`


---

## Notes

- Accès à l’admin Django : `http://localhost:8000/admin/`
- Pour toute action protégée, un token JWT valide est requis.

