# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django-based Uzbek-language news portal. Runs on Django 6.0 with SQLite. A single app (`newsapp`) handles all content: articles, categories, regions, and tags.

## Commands

```bash
python manage.py runserver       # start dev server
python manage.py migrate         # apply migrations
python manage.py makemigrations  # generate migrations after model changes
python manage.py createsuperuser # create admin user
python manage.py shell           # interactive Django shell
```

## Architecture

**Single-app structure:** `newsapp/` contains all models, views, URLs, admin config, templates, and context processors.

**Models (`newsapp/models.py`):**
- `News` — core article with `title`, `slug`, `content`, `image`, `count_views`, FK to `Category` and `Region`, M2M to `Tag`
- `Category`, `Region`, `Tag` — each has `name` + unique `slug`

**URL patterns (`newsapp/urls.py`):**
- `/` → `home` — all news, ordered by `created_at`
- `/category/<slug>` → `category_news`
- `/region/<slug>` → `region_news`
- `/tag/<slug>` → `tag_news`
- `/read_more/<slug>` → `read_more` — single article view, increments `count_views`

**Templates (`newsapp/templates/newsapp/`):**
- `base.html` extended by page templates: `home.html`, `read_more.html`, `category_news.html`, `region_news.html`, `tag_news.html`
- `inc/` holds partials: `_nav1.html`, `_nav2.html`, `_latestNews.html`, `_most_viewed.html`

**Context processors (`newsapp/context_processors.py`):** Inject `categories`, `regions`, and `latest_news` into every template automatically.

## Known Issues

- `CategoryAdmin` in `admin.py` has a typo: `prepopulated_fie` should be `prepopulated_fields`
- `SECRET_KEY` is hardcoded in `settings.py`
- `read_more` view increments `count_views` non-atomically (race condition under concurrent load)
- Views use `.get()` without `try/except` — missing slugs raise unhandled 500 errors instead of 404s
- No tests exist (`tests.py` is empty)
