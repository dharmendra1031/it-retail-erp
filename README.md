# IT Retail ERP

Computer hardware, software and IT retail management system for Kuwait.

## Backend stack

- Python 3.12+
- Django 5.2 LTS
- Django REST Framework
- Microsoft SQL Server 2019
- mssql-django + pyodbc

## Setup

```bash
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

API health check:

```text
GET /api/health/
```
