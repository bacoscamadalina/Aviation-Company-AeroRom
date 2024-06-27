from decimal import Decimal
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator

from .models import Destinations, Price, Discount, Cart, CartItem
from django.views import View
from django.http import HttpResponse


@method_decorator(login_required,
                  name='dispatch')  # Putem efectua o rezervare doar daca suntem conectați, daca nu, suntem redierctionati catre pagina de login
class TicketsOrderView(View):
    def get(self, request):  # tratam cererile GET
        departure_destinations = Destinations.objects.all()  # obtinem destinatiile din modelul cu clasa Destinations
        arrival_destinations = Destinations.objects.all()
        return render(request, 'tickets/tickets_list.html', {'departure_destinations': departure_destinations,
                                                             'arrival_destinations': arrival_destinations})  # returnam sablonul cu contextul care contine toate destinatiile

    def post(self, request):  # tratam cererile POST (trimise prin formular)
        departure_id = request.POST.get('departure')  # id-ul destinatiei de plecare
        arrival_id = request.POST.get('arrival')  # id-ul destinatiei de sosire
        depart_date = request.POST.get('depart-date')  # data de plecare
        return_date = request.POST.get('return-date')  # data intoarcerii
        passengers_str = request.POST.get('passengers')  # numarul de pasageri
        flight_type = request.POST.get('flight-type')  # tipul de zbor

        if not passengers_str:
            return HttpResponse('Nu ați introdus numărul de pasageri')

        passengers = int(passengers_str)

        if arrival_id == departure_id:   # daca orasul de plecare = destinatia
            return HttpResponse('Nu există zbor pentru această rută. Introduceți o rută validă')

        try:
            if flight_type == 'one_way':  # daca tipul de zbor este doar dus
                price = Price.objects.get(destinations_id=departure_id, arrival_id=arrival_id, flight_type='one_way',
                                          start_date__lte=depart_date,
                                          end_date__gte=depart_date)  # cautam in baza de date pretul
                total_price = price.price * passengers  # calculam pretul total
                initial_price = total_price  # setam pretul initial
                depart_date2 = depart_date  # setam data de plecare
                return_date2 = None  # setam None deoarece nu avem intoarcere intr-un zbor doar dus
            elif flight_type == 'round_trip':  # daca tipul de zbor este dus-intors
                price = Price.objects.get(destinations_id=departure_id, arrival_id=arrival_id, flight_type='round_trip',
                                          start_date__lte=depart_date,
                                          end_date__gte=return_date)  # cautam pretul in baza de date
                total_price = price.price * passengers
                initial_price = total_price
                depart_date2 = depart_date
                return_date2 = return_date
            else:
                return HttpResponse("Tipul de zbor selectat este invalid.")  # daca tipul de zbor este invalid
        except Price.DoesNotExist:  # daca nu există un preț pentru zborul selectat
            return HttpResponse("Nu există un preț disponibil pentru tipul de zbor selectat.")

        # Aplicarea discountului, dacă acesta există
        discount_percentage = 0  # variabila care tine procentul discount-ului aplicat
        discount = Discount.objects.filter(
            destinations_id=departure_id,
            arrival_id=arrival_id,
            start_date__lte=depart_date,
            end_date__gte=depart_date).first()

        if discount:
            initial_price = price.price * passengers  # pretul initial, fara o reducere
            discount_percentage = discount.discount_percentage  # setam la valoarea procentului de discount din obiect
            total_price = initial_price * (1 - discount_percentage / 100)  # aplicam reducerea de pret

        discount_rate = Decimal('0.85')  # convertim deoarece in models avem DecimalField
        depart_date_obj = datetime.strptime(depart_date, '%Y-%m-%d')  # Convertim din string in data
        if passengers >= 5 and depart_date_obj.month == 8:  # aplicam reducerea in cazul in care avem in cos mai mult de 5 bilete in luna august
            initial_price = price.price * passengers
            group_discount_percentage = 15  # reducerea de 15%
            # Având în vedere că avem și alte reduceri aplicate, alegem reducerea cea mai mare
            if group_discount_percentage > discount_percentage:
                discount_percentage = group_discount_percentage
                total_price = initial_price * discount_rate
            else:
                total_price = initial_price * (1 - discount_percentage / 100)

        # Adăugare în coșul de cumpărături
        cart = Cart.get_current_order(request.user)  # obtinem cosul curent de cumparaturi al utilizatorului

        # GESTIONAM DUPLICATELE
        cart_items = CartItem.objects.filter(
            cart=cart, price=price, user=request.user,
            depart_date=depart_date2, return_date=return_date2
        )  # filtram elementele din coșul utilizatorului

        if cart_items.exists():  # daca există un bilet
            cart_item = cart_items.first()  # obtinem primul element duplicat
            cart_item.quantity += passengers  # actualizam cantitatea
            cart_item.save()  # salvam modificarile
            cart_items.exclude(
                id=cart_item.id).delete()  # stergem celelalte elemente duplicate, păstrând cel actualizat
        else:
            CartItem.objects.create(
                cart=cart, price=price, user=request.user,
                quantity=passengers, depart_date=depart_date2, return_date=return_date2
            )  # Dacă nu există duplicate, creăm un nou element în coș

        context = {
            'departure_destinations': Destinations.objects.all(),
            'arrival_destinations': Destinations.objects.all(),
            'initial_price': initial_price,
            'total_price': total_price,
            'price': price,
            'discount_percentage': discount_percentage if discount_percentage > 0 else None,
            'passengers': passengers
        }  # contextul pentru șablonul HTML
        return render(request, 'tickets/tickets_list.html', context)  # returnam un raspuns HTTP


@login_required  # ne asiguram ca doar utilizatorii logați pot accesa funcția
def add_to_cart(request, price_id):
    price = get_object_or_404(Price, id=price_id)  # daca nu gasim pretul, ridicam eroarea 404 (pagian nu a fost gasita)
    cart = Cart.get_current_order(request.user)  # obtinem cosul de cumparaturi al utilizatorului

    # Verificam dacă există deja un CartItem pentru cart și price
    cart_item = CartItem.objects.filter(cart=cart, price=price, user=request.user).first()

    if cart_item:
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, price=price, user=request.user)

    return redirect('tickets:cart')  # redirectionam catre cosul de cumparaturi


@method_decorator(login_required,
                  name='dispatch')  # inainte de a procesa orice cerere, Django verifica daca utilizatorul este autentificat
class CartDetailView(View):
    template_name = 'tickets/cart.html'

    def get(self, request):
        current_order = Cart.get_current_order(request.user)  # obtinem cosul de cumparaturi
        # Initializam variabilele: 
        total_price = 0
        discount_amount = 0

        items = []

        if current_order:  # daca exista un cos de cumparaturi curent
            for item in current_order.items.all():  # iteram prin elementele cosului
                item_total_price = item.get_total_price()  # calculam pretul total folosind metoda get_total_price()
                total_price += item_total_price  # adaugam pretul total al elementului la "total_price"

                # Verificăm dacă datele sunt valide înainte de a face interogarea pentru discount
                if item.depart_date and item.price.start_date and item.price.end_date:
                    discount = Discount.objects.filter(
                        destinations_id=item.price.destinations_id,
                        arrival_id=item.price.arrival_id,
                        start_date__lte=item.depart_date,
                        end_date__gte=item.depart_date
                    ).first()  # daca ni se returneaza mai multe rezultate, luam primul
                    if discount:  # daca exista o reducere, calculam suma de reducere
                        discount_amount += (item.price.price * item.quantity) * (discount.discount_percentage / 100)

                # Aplicăm reducerea de grup (15%) pentru luna august și 5 sau mai mulți pasageri
                if item.depart_date:
                    depart_date_obj = datetime.strptime(str(item.depart_date),
                                                        '%Y-%m-%d')  # Convertim din string in data
                    if item.quantity >= 5 and depart_date_obj.month == 8:
                        group_discount_percentage = 15
                        group_discount = (Decimal(item.price.price) * item.quantity) * (
                                Decimal(group_discount_percentage) / 100)
                        discount_amount = max(discount_amount,
                                              group_discount)  # returneaza valoarea cea mai mare a reducerii

                items.append({
                    'item': item,
                    'total_price': item_total_price,
                })  # adaugam elementele in lista pentru a le utiliza in template

        # Calculam pretul dupa discount
        total_price_after_discount = total_price - discount_amount

        context = {
            'order': current_order,
            'items': items,
            'total_price': total_price,
            'discount_amount': discount_amount,
            'total_price_after_discount': total_price_after_discount,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request, item_id):  # item_id = elementul care urmeaza a fi eliminat din cosul de cumparaturi
        cart_item = get_object_or_404(CartItem, id=item_id,
                                      cart__user=request.user)  # daca elementul nu este gasit, primim eroarea 404
        cart_item.delete()
        return redirect('tickets:cart')


class PlaceOrderView(View):
    def post(self, request):
        current_order = Cart.get_current_order(request.user)
        if current_order:
            # Marcam comanda ca fiind plasată
            current_order.ordered = True
            current_order.save()

            # Dupa finalizarea comenzii redirectionam utilizatorul la pagina de succes
            messages.success(request, 'Comanda a fost efectuată cu succes!')
            return redirect(reverse('tickets:order_success'))
        return redirect('tickets:cart')


@method_decorator(login_required, name='dispatch')
class OrderSuccessView(View):
    template_name = 'tickets/order_success.html'

    def get(self, request):
        return render(request, self.template_name)
