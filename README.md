# QuerySafe

A Django REST API demonstrating MongoDB's Queryable Encryption using `django-mongodb-backend`.

## Tech Stack

- Python 3.12 / Django 6.x
- MongoDB 8.0 
- Django REST Framework
- drf-spectacular (Swagger)

## Setup

```bash
git clone
cd querysafe
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --database encrypted
python manage.py seed_data --target encrypted
python manage.py runserver
```

Visit `http://127.0.0.1:8000/api/docs/`

## API

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/assessments/` | List all assessments |
| POST | `/api/assessments/` | Create an assessment |

## Encryption

| Encrypted 🔒 | Plain (queryable) |
|---------------|-------------------|
| Titles, descriptions | Likelihood, impact |
| Names, emails, roles | Score, dates |

Data is encrypted at rest in MongoDB. 
Django auto-decrypts on read.

## Tests

```bash
python manage.py test riskapp
```

## References
- [Queryable Encryption](https://www.mongodb.com/docs/languages/python/django-mongodb/current/queryable-encryption/)
