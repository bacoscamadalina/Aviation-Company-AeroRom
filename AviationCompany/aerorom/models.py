import os
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

# Modelul pentru pagina Despre noi
class CompanyInfo(models.Model):
    description = models.TextField()  # descrierea
    angajat = models.CharField(
        max_length=100)  # numele angajatului, stocam siruri de caractere cu lungimea maxima de 100 caractere
    post = models.CharField(max_length=100)  # postul pe care il ocupa
    experienta = models.TextField()  # experienta de munca,stocam un text fara o limita de caractere
    email = models.EmailField()  # adresa de contact

    def get_description_fragments(
            self):  # dorim ca în momentul când punem '/' in pagina admin să mutăm textul cu un rând mai jos
        return self.description.split('/')


# Model pentru pagina de afișare a destinațiilor
'''
Vrem ca pozele pe care le adaugam in admin sa fie salvate in: 'aerorom/static/destinations',așadar construim o funcție 
destination_image_path() care să redirecționeze imaginile din admin într-un folder:
'''


def destination_image_path(instance, filename):  # functie care genereaza calea unde vor fi salvate imaginile
    return os.path.join('aerorom/static/destinations', filename)


class Destination(models.Model):  # models.Model permite crearea de tabele si manipularea datelor
    location = models.CharField(max_length=100)  # destinatia
    description = models.TextField()  # descrierea destinatiei
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # stocam valori cu zecimale pentru pret
    image = models.ImageField(upload_to=destination_image_path)  # stocam imagini pentru imaginea destinatiilor


# Model pentru pagina de contact
class Contact(models.Model):
    name = models.CharField(max_length=100)  # nume
    phone_number = models.CharField(max_length=20)  # numarul de telefon
    email = models.EmailField()  # stocam adrese de email
    message = models.TextField()  # mesajul dorit


# Model pentru pagina de cariere
class Job(models.Model):
    job_name = models.CharField(max_length=100)  # numele postului
    description = models.TextField()  # descrierea postului

    def get_description_fragments(self):
        return self.description.split('/')


# Model pentru pagina de adaugare recenzii
class Reviews(models.Model):
    nume = models.CharField(max_length=100, default='Nedeterminat')  # numele celui care doreste sa lase o recenzie
    content = models.TextField()  # continutul
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(
        5)])  # Stocam nr. intregi cu valoare min si max acceptata
    post_date = models.DateTimeField(auto_now_add=True)  # data postarii
