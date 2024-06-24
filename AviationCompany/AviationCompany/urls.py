"""
URL configuration for AviationCompany project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# lista de rute URL specifice fiecarei pagini, utilizand aplicatiile create
urlpatterns = [
    # Redirecționare către pagina home (permanent= False - redirectionarea nu este permanenta, daca era True, browserul memora redirectionarea)
    path('', RedirectView.as_view(url='/aerorom/home/', permanent=False)),
    path('aerorom/', include('aerorom.urls', namespace='aerorom')),  # Include toate URL-urile din aplicația aerorom
    path('tickets/', include('tickets.urls')),  # Include toate URL-urile din aplicatie tickets
    # includem toate rutarile din aplicatia de autentificare Django
    path('users/', include('users.urls',namespace='users')),  # include toate URL-urile din aplicatia urls
    path('admin/', admin.site.urls),  # ruta pentru interfata de administrare
]

'''
Verificăm dacă setarea DEBUG este activată în fișierul de setări Django. Dacă este activată, se adaugă rute
URL specifice media la lista de rute
'''
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)