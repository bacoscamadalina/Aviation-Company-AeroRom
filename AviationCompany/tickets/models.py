from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Definim un model in baza de date pentru destinatii
class Destinations(models.Model):
    name = models.CharField(max_length=100)  # numele destinatiei

    def __str__(self):
        return self.name  # returnam in siruri de caractere numele destinatiilor

# Definim un model in baza de date pentru pretul rezervarilor
class Price(models.Model):
    destinations = models.ForeignKey(Destinations, related_name='prices',
                                     on_delete=models.CASCADE)  # accesam obiectele 'Price' prin intermediul atributului 'prices',
    # models.CASCADE - daca o instanță 'Destinations' se sterge, toate obiectele 'Price' se sterg
    arrival = models.ForeignKey(Destinations, related_name='arrival_prices', on_delete=models.CASCADE, default=1) # destinatia de sosire
    flight_type = models.CharField(max_length=20) # tipul zborului (dus/ dus-intors)
    price = models.DecimalField(max_digits=10, decimal_places=2) # pretul zborului
    start_date = models.DateField(default='2023-12-31')  # stocam date de tip data ( iceputul perioadei de valabilitate a pertului)
    end_date = models.DateField(default='2023-12-31') # sfarsitul perioadei de valabilitate a pretului

    def __str__(self):  # returnam o reprezentare a obiectului in admin
        return f"{self.destinations.name} - {self.arrival.name} - {self.flight_type}: €{self.price}"

# Definim un model in baza de date pentru reduceri
class Discount(models.Model):
    destinations = models.ForeignKey(Destinations, related_name='discounts', on_delete=models.CASCADE)  # destinatia de sosire
    arrival = models.ForeignKey(Destinations, related_name='arrival_discount', on_delete=models.CASCADE, default=1) # destinatia de intorcere
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2) # procentul de reducere
    start_date = models.DateField() # inceputul perioadei
    end_date = models.DateField() # sfarsitul perioadei

    def __str__(self):
        return f"{self.destinations.name} - {self.arrival.name} - Discount: {self.discount_percentage}%"

# Definim un model in baza de date pentru cosul de cumparaturi
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # setam default=1 ca fiind un user valid
    ordered = models.BooleanField(default=False)  # default=False - comanda nu a fost inca plasata
    created_at = models.DateTimeField(default=datetime.now)  # stocam data si ora la care se crează comanda

    @staticmethod  # cream o metoda statica get_current_order() (nu avem acces la instanta obiectului si la clasa )
    def get_current_order(user):
        qs = Cart.objects.filter(user=user,
                                 ordered=False)  # cream un queryset care filtreaza obiectele 'Cart' pentru a gasi comenzile nefinalizate
        if qs.exists():  # daca gasim o comanda nefinalizata
            return qs.first()  # returnam primul cos din queryset
        return Cart.objects.create(user=user)  # daca nu exista, se creaza un nou cos pentru utilizator

    def total_price(self):  # functie care calculeaza si returneaza pretul total al articolelor din cos
        return sum(item.price.price * item.quantity for item in self.items.all())

# Definim un model in baza de date pentru elementele din cosul de cumparaturi
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #daca utilizatorul este sters, toate obiectele vor fi sterse, default 1 = user valid
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE) # daca comanda este stearsa, se sterg toate obiectele CartItem
    price = models.ForeignKey(Price, on_delete=models.CASCADE) # cheie straina catre obiectul 'Price', daca pretul este sters, se sterg obiectele asociate acestui pret
    quantity = models.PositiveIntegerField(default=0) # cantitatea de articole din cos
    depart_date = models.DateField(null=True, blank=True) # data de plecare
    return_date = models.DateField(null=True, blank=True) # data de intoarcere

    def get_total_price(self):
        return self.price.price * self.quantity # returnam pretul unui articol din cos

    class Meta:
        unique_together = ('cart', 'price', 'depart_date', 'return_date') # combinatii unice in baza de date
