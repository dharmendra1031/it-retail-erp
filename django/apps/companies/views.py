from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CompanyForm
from .models import Company


class CompanyListView(ListView):
    model = Company
    context_object_name = "companies"


class CompanyDetailView(DetailView):
    model = Company


class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy("companies:list")


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy("companies:list")

    def form_valid(self, form):
        previous_name = self.object.logo.name if self.object.logo else ""
        storage = self.object.logo.storage if previous_name else None

        response = super().form_valid(form)

        current_name = self.object.logo.name if self.object.logo else ""
        if "logo" in form.changed_data and previous_name and previous_name != current_name:
            storage.delete(previous_name)

        return response


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("companies:list")

    def form_valid(self, form):
        logo_name = self.object.logo.name if self.object.logo else ""
        storage = self.object.logo.storage if logo_name else None

        response = super().form_valid(form)

        if logo_name:
            storage.delete(logo_name)

        return response
