from django import forms
from .models import Contact, Reviews


# Construim clasele pentru formularul de contact si formularul de recenzii
class ContactForm(forms.ModelForm):
    class Meta:  # configuram optiunile specifice modelului pentru formular
        model = Contact  # modelul de referinta din baza de date
        fields = ['name', 'email', 'message']  # campurile din model


class Review(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['nume', 'content', 'rating']
