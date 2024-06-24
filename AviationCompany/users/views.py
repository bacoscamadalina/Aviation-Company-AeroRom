from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic import FormView
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileForm
from .models import UserProfile
from tickets.models import Cart


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm  # formularul utilizat din forms.py
    redirect_authenticated_user = True  # daca utilizatorul este deja autentificat, redirectionam catre succes_url
    success_url = reverse_lazy('aerorom:home')

    def form_valid(self, form):
        user = form.save()  # salvam datele formularului si cream un nou utilizator
        if user:  # daca utilizatorul a fost inregistrat cu succes
            login(self.request, user)  # se poate conecta folosind functia 'login'
            messages.success(self.request, 'Te-ai înregistrat cu succes.')
        return super().form_valid(form)  # ne returneaza Reg cu formul valid si salveaza si userul

    def form_invalid(self, form):  # pentru un formular invalid
        messages.error(self.request, 'Te rog corectează erorile care apar.')
        return super().form_invalid(form)


# Construium pagina de login
class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('aerorom:home')  # daca logarea este reușită facem redirectionare automata la home

    def form_valid(self, form):  # pentru un formular valid
        username = form.cleaned_data['username']  # extragem username-ul din datele formularului
        password = form.cleaned_data['password']  # extragem parola din datele formularului
        user = authenticate(username=username,
                            password=password)  # realizam autentificarea folosind username si password
        login(self.request, user)  # ne conectam folosind funcția login
        return super().form_valid(form)

    def form_invalid(self, form):  # Pentru un formular invalid
        messages.error(self.request, 'Username sau parolă invalidă!')
        return render(self.request, self.template_name, self.get_context_data(form=form))


# In momentul cand apasam pe butonul de deconectare
def logout_view(request):
    logout(request)  # utilizatorul se deconectează
    return redirect('users:login') # redirecționăm utilizatorul spre pagina de login


@login_required  # accesibil doar pentru utilizatorii logați
def contul_meu(request):
    user = request.user  # obtinem utilizatorul
    try:
        profile = user.userprofile  # obtinem profilul utilizatorului
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)  # daca nu exista, cream unul

    user_form = UserForm(instance=user)  # cream formular cu datele utilizatorului (nume, prenume, email)
    profile_form = UserProfileForm(instance=profile)  # _"_ cu datele profilului (varsta, document de identitate)
    current_order = Cart.get_current_order(user)  # obtinem comenzile nefinalizate
    orders = Cart.objects.filter(user=user, ordered=True)  # obtinem comenzile finalizate

    if request.method == 'POST':  # adaugam datele in formular
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():   # daca detaliile sunt valide
            # salvam datele utilizatorului
            user_form.save()
            profile_form.save()
            messages.success(request, 'Detaliile au fost actualizate cu succes.')
            return redirect('users:contul_meu')
        else:
            messages.error(request, 'A apărut o eroare. Te rugăm să încerci din nou.')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'current_order': current_order,
        'orders': orders,
    }
    return render(request, 'registration/contul_meu.html', context)
