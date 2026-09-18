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
