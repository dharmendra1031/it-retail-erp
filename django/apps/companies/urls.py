from django.urls import path

from .views import (
    CompanyCreateView,
    CompanyDeleteView,
    CompanyDetailView,
    CompanyListView,
    CompanyUpdateView,
)

app_name = "companies"

urlpatterns = [
    path("companies/", CompanyListView.as_view(), name="list"),
    path("companies/add/", CompanyCreateView.as_view(), name="create"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="detail"),
    path("companies/<int:pk>/edit/", CompanyUpdateView.as_view(), name="edit"),
    path("companies/<int:pk>/delete/", CompanyDeleteView.as_view(), name="delete"),
]
