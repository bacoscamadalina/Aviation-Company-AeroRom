from django.urls import path
from .views import TicketsOrderView, add_to_cart, CartDetailView, RemoveFromCartView, PlaceOrderView, OrderSuccessView
from . import views

app_name = 'tickets'  # numele aplicatiei
# Lista de rute URL
urlpatterns = [
    path('', views.TicketsOrderView.as_view(), name='tickets_list'),  # Pagina principala de rezervari
    path('add_to_cart/<int:price_id>/', views.add_to_cart, name='add_to_cart'), # <int:price_id> - specifica id-ul pretului biletului
    path('cart/', CartDetailView.as_view(), name='cart'),
    path('remove_from_cart/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('order_success/', OrderSuccessView.as_view(), name='order_success'),
]
