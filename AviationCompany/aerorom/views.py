from django.shortcuts import render, redirect
from .models import Job, Destination, Reviews, CompanyInfo, Contact
from django.views.generic import TemplateView, ListView, CreateView
from .forms import ContactForm
from django.urls import reverse_lazy, reverse


# Create your views here.

# Clasa pentru pagina principala: Acasa care mosteneste din TemplateView
class HomePage(TemplateView):  # TemplateView - vedere utilizata pentru un sablon simplu
    template_name = 'aerorom/home.html'  # sablon "home.html" din folderul "aerorom", pentru a genera raspunsul


# Clasa pentru pagina: Despre noi care mosteneste din ListView
class CompanyInfoView(ListView):
    model = CompanyInfo  # Accesam si manipulam datele din baza de date CompanyInfo
    context_object_name = 'info'  # Accesam în șabloane obiectele "CompanyInfo" sub numele "info" (in caz de dorim sa iterăm)
    template_name = 'aerorom/company_info.html'


# Clasa pentru pagina: Destinatii
class DestinationsView(ListView):
    model = Destination
    context_object_name = 'destinations'
    template_name = 'aerorom/destinations.html'


# Clasa pentru pagina: Contact are mosteneste din CreateView
class ContactView(CreateView):  # vedere pentru a crea noi obiecte in baza de date
    model = Contact  # modelul de referinta din baza de date
    context_object_name = 'contact'  # Accesam în șabloane obiectele "Contact" sub numele "contact”
    template_name = 'aerorom/contact.html'
    form_class = ContactForm  # din forms.py (colectam date de la utilizatori)
    success_url = '/aerorom/contact/'  # dupa ce trimitem formularul, redirectionam tot catre Contact

    # Functii pentru a manipula si a afisa datele in sablon
    def get_context_data(self, **kwargs):  # obtinem si returnam datele de context care vor fi transmise șablonului
        context = super().get_context_data(**kwargs)  # apelam metoda get_context_data() a clasei parinte
        context['form'] = self.get_form()  # adaugam la datele de context obiectul formularului
        return context  # returnam datele pentru a le folosi in sablon

    def form_valid(self, form):  # metoda care va fi apelata dupa ce utilizatorul trimite datele
        form.save()  # salvam datele din formular
        return super().form_valid(form)  # apelam metoda form_valid .


# Clasa pentru pagina: Cariere
class JobInfoView(ListView):
    model = Job  # modelul de referinta din baza de date
    context_object_name = 'jobs'  # Accesam în șabloane obiectele "Job" sub numele "jobs"
    template_name = 'aerorom/job_info.html'  # numele șablonului html


# Clasa pentru pagina: Adauga recenzii
class AddReviewView(CreateView):
    model = Reviews
    fields = ['nume', 'content', 'rating']  # campurile afisate si editabile din formular
    template_name = 'aerorom/add_review.html'  # numele șablonului html
    success_url = reverse_lazy('aerorom:reviews')  # dupa ce trimitem formularul redirectionam catre reviews


# Clasa pentru pagina: Recenzii
class ReviewsView(TemplateView):
    template_name = 'aerorom/reviews.html'  # numele șablonului html

    def get_context_data(self, **kwargs):  # permitem trecerea argumentelor suplimentare
        context = super().get_context_data(**kwargs)  # apelam metoda get_context_data() a clasei parinte
        context['reviews'] = Reviews.objects.all()  # adaugam toate obiectele din 'Rewiews'
        return context  # returnam datele pentru a le folosi in sablon


# Clasa pentru pagina : Politici si Reguli
class RulesView(TemplateView):
    template_name = 'aerorom/rules.html'  # numele șablonului html
