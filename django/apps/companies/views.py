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
        previous_logo = self.object.logo
        response = super().form_valid(form)

        if "logo" in form.changed_data and previous_logo:
            current_name = self.object.logo.name if self.object.logo else ""
            if previous_logo.name != current_name:
                previous_logo.storage.delete(previous_logo.name)

        return response


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("companies:list")

    def form_valid(self, form):
        logo = self.object.logo
        response = super().form_valid(form)

        if logo:
            logo.storage.delete(logo.name)

        return response
