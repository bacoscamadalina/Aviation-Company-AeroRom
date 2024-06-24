from django.contrib import admin

from django.contrib import admin
from .models import CompanyInfo,Contact,Job,Reviews,Destination

# Oferim acces pe pagina de admin pentru a putea adauga/modifica/sterge informatii
admin.site.register(CompanyInfo)
admin.site.register(Contact)
admin.site.register(Job)
admin.site.register(Reviews)
admin.site.register(Destination)