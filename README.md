# Loose Papers
Work in progress

## Loose Papers - Local Setup

### 1. Start PostgreSQL & Redis
```bash
  docker-compose up -d
```
### 2. Install dependencies
```bash
  poetry install
```
### 3. Run migrations
```bash
  poetry run python manage.py migrate
```
### 4. Start Django server
```bash
  poetry run python manage.py migrate
```