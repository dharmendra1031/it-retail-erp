# Django backend

Django API implementation of IT Retail ERP.

## Stack

- Python 3.12+
- Django 5.2 LTS
- Django REST Framework
- Microsoft SQL Server 2019
- mssql-django
- pyodbc

## Setup

1. Create a virtual environment.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Run `python manage.py migrate`.
5. Create the first user with `python manage.py createsuperuser`.
6. Run `python manage.py runserver`.

The React frontend communicates through the `/api` contract.


## Required configuration

Copy `.env.example` to `.env`, set a strong unique `SECRET_KEY`, real `DB_NAME`, credentials and installed ODBC driver. When `DEBUG=False`, missing `SECRET_KEY` stops Django startup. Missing `DB_NAME` stops the production SQL Server configuration before startup. Never commit `.env`.

## Local checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test apps.core apps.accounts apps.companies
```

Unit tests in GitHub Actions use `config.settings_test` and a disposable SQLite database; CI separately runs these test modules and SQL Server migrations/integration/concurrency tests against an ephemeral SQL Server 2022 container. Never run destructive test DB commands against production.
