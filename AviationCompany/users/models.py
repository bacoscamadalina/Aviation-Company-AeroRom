from django.contrib.auth.models import User
from django.db import models


# Cream baza de date pentru profilul utilizatorului
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # detaliile utilizatorului
    age = models.IntegerField(blank=True, null=True)  # varsta
    passaport = models.ImageField(upload_to='passaports/', null=True, blank=True) #actul de identitate

    def __str__(self):
        return self.user.username
