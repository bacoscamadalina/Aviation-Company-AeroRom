from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


# Construim formularul de întregistrare
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # câmpurile care vor fi incluse în formular.


# Construim formularul de login
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # pentru a introduce valori ascunse in câmpul password

    def clean(self):
        cleaned_data = super().clean()  # metoda clean a clasei UserCreationForm pentru a obține datele validate.
        username = cleaned_data.get('username')  # extragem numele de utilizator din datele validate.
        password = cleaned_data.get('password')  # extragem parola  din datele validate.

        if username and password:  # dacă campurile sunt completate corect
            user = authenticate(username=username,
                                password=password)  # autentifică utilizatorul cu numele de utilizator și parola furnizate
            if not user:  # daca autentificarea nu este valida
                raise forms.ValidationError('Username sau parola invalide')
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nume',
            'last_name': 'Prenume',
            'email': 'Email',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'passaport']
        labels = {
            'age': 'Vârstă',
            'passaport': 'Pașaport',
        }
