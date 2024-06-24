from django.contrib import admin
from .models import Price, Destinations, Discount, Cart, CartItem

# Oferim acces in pagian de administrator pentru a modifica, adauga și șterge elemente
admin.site.register(Destinations)
admin.site.register(Price)
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(CartItem)
