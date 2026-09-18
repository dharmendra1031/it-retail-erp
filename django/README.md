# Django implementation

Python Django implementation of IT Retail ERP.

## Stack

- Python 3.12+
- Django 5.2 LTS
- Microsoft SQL Server 2019
- mssql-django
- pyodbc

## Setup

```bash
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

On Windows, use `copy .env.example .env` instead of `cp`.
