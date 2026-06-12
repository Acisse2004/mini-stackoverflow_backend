# Mini Stack Overflow — Backend Django

## Installation

```bash
# 1. Cloner et entrer dans le projet
cd mini_stackoverflow

# 2. Créer un environnement virtuel
python -m venv env
source env/bin/activate        # Linux/Mac
env\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Modifier .env avec vos identifiants PostgreSQL

# 5. Créer la base de données PostgreSQL
createdb mini_stackoverflow

# 6. Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# 7. Créer un superuser
python manage.py createsuperuser

# 8. Lancer le serveur
python manage.py runserver
```

---

## Routes API

### Authentification — `users/`
| Méthode | URL | Description | US |
|---------|-----|-------------|-----|
| POST | `/api/auth/register/` | Inscription | US001 |
| POST | `/api/auth/login/` | Connexion → JWT | US002 |
| POST | `/api/auth/logout/` | Déconnexion | US002 |
| POST | `/api/auth/refresh/` | Rafraîchir le token | — |
| GET  | `/api/auth/me/` | Profil connecté | US003 |
| GET  | `/api/auth/users/<id>/` | Profil public | US003, US014 |
| PUT  | `/api/auth/users/<id>/` | Modifier profil | US003 |

### Questions — `questions/`
| Méthode | URL | Description | US |
|---------|-----|-------------|-----|
| GET  | `/api/questions/` | Liste + filtre + recherche | US005, US006, US012 |
| POST | `/api/questions/` | Créer une question | US004 |
| GET  | `/api/questions/<id>/` | Détail d'une question | US007 |
| PUT  | `/api/questions/<id>/` | Modifier (auteur) | US004 |
| DELETE | `/api/questions/<id>/` | Supprimer (auteur) | — |
| POST | `/api/questions/<id>/vote/` | Voter | US009 |
| GET  | `/api/questions/tags/` | Liste des tags | US013 |
| GET  | `/api/questions/tags/<name>/questions/` | Questions par tag | US013 |

### Réponses & Commentaires — `answers/`
| Méthode | URL | Description | US |
|---------|-----|-------------|-----|
| GET  | `/api/questions/<id>/answers/` | Réponses d'une question | US007 |
| POST | `/api/questions/<id>/answers/` | Ajouter une réponse | US008 |
| PUT  | `/api/answers/<id>/` | Modifier (auteur) | — |
| DELETE | `/api/answers/<id>/` | Supprimer (auteur) | — |
| POST | `/api/answers/<id>/vote/` | Voter | US009 |
| POST | `/api/answers/<id>/best/` | Marquer meilleure réponse | US011 |
| GET  | `/api/answers/<id>/comments/` | Commentaires | US010 |
| POST | `/api/answers/<id>/comments/` | Ajouter commentaire | US010 |
| DELETE | `/api/comments/<id>/` | Supprimer commentaire | — |

---

## Paramètres de filtre (GET /api/questions/)

| Paramètre | Exemple | Description |
|-----------|---------|-------------|
| `search` | `?search=django` | Recherche mot-clé (US012) |
| `tag` | `?tag=python` | Filtrer par tag (US013) |
| `unresolved` | `?unresolved=true` | Sans réponse acceptée (US006) |
| `ordering` | `?ordering=-vote_count` | Tri par votes (US006) |
| `ordering` | `?ordering=-created_at` | Tri par date (US006) |

---

## Headers pour les requêtes authentifiées

```
Authorization: Bearer <access_token>
Content-Type: application/json
```
