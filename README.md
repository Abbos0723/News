# News Portal

Uzbek-language news portal built with Django 6.0.

## Features

- News articles with categories, regions, and tags
- View count tracking per article
- Django admin for content management

## Setup

```bash
# Install dependencies
pip install django python-dotenv

# Create a .env file
cp .env.example .env
# Add your SECRET_KEY to .env

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
