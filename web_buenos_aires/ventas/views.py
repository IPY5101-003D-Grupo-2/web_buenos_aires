from django.views.decorators.csrf import csrf_exempt
from web_buenos_aires.ventas.indicador import Mindicador
from .models import CarritoDeCompra
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
import zeep
import requests
from datetime import datetime
from django.urls import reverse
from transbank.webpay.webpay_plus.transaction import Transaction
import random


class ProductoListaView(TemplateView):
    template_name = "ventas/producto-lista.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get('https://ws-buenos-aires.herokuapp.com/inventario/')
        productos = response.json()
        context['valor_dolar'] = Mindicador('dolar').valor_actual()
        for producto_a in productos:
            producto_a['PRECIO_EN_DOLARES'] = round(producto_a['PRECIO'] / context['valor_dolar'], 2)
        context['productos'] = productos
        productos_en_carrito = self.request.user.carritos.all()
        skus_a_buscar = []
        for producto in productos_en_carrito:
            skus_a_buscar.append(producto.sku)
        lista = list(filter(lambda producto: producto.get("SKU") in skus_a_buscar, productos))
        total_carrito = 0
        for product in lista:
            product["CANTIDADCARRITO"] = productos_en_carrito.get(sku=product.get("SKU")).cantidad
            product["PRECIOCARRITO"] = product.get("PRECIO") * productos_en_carrito.get(sku=product.get("SKU")).cantidad
            total_carrito += product["PRECIOCARRITO"]
        context['total_carrito'] = total_carrito
        context['carrito'] = lista
        print("skus", skus_a_buscar)
        print("carrito", context['carrito'])

        return context


class FinalizarCompraView(TemplateView):
    template_name = "ventas/finalizar-compra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get('https://ws-buenos-aires.herokuapp.com/inventario/')
        productos = response.json()
        context['productos'] = productos

        productos_en_carrito = self.request.user.carritos.all()
        skus_a_buscar = []
        for producto in productos_en_carrito:
            skus_a_buscar.append(producto.sku)
        lista = list(filter(lambda producto: producto.get("SKU") in skus_a_buscar, productos))
        total_carrito = 0
        for product in lista:
            product["CANTIDADCARRITO"] = productos_en_carrito.get(sku=product.get("SKU")).cantidad
            product["PRECIOCARRITO"] = product.get("PRECIO") * productos_en_carrito.get(sku=product.get("SKU")).cantidad
            total_carrito += product["PRECIOCARRITO"]

        context['carrito'] = lista
        context['total_carrito'] = total_carrito

        print("skus", skus_a_buscar)
        print("carrito", context['carrito'])

        amount = total_carrito
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(self.request.user.id)
        return_url = 'http://127.0.0.1:8000'+reverse('ventas:transaccion-exitosa')

        response = Transaction.create(buy_order, session_id, amount, return_url)
        context['url_transbank'] = response.url
        context['token'] = response.token

        return context


class ComprobarMedioDePagoView(APIView):
    def post(self, request, format=None):
        full_name = request.data.get("full_name")
        card_number = int(request.data.get("card_number"))
        cvv_number = int(request.data.get("cvv_number"))
        card_type = request.data.get("type")
        expiration_month = int(request.data.get("expiration_month"))
        expiration_year = int(request.data.get("expiration_year"))
        wsdl = "https://ws-soap-pagos.herokuapp.com/?wsdl"
        client = zeep.Client(wsdl=wsdl)
        soap_response = client.service.check_payment(
            full_name, card_number, cvv_number, card_type, expiration_month, expiration_year)
        if soap_response is True:
            return Response({"confirmacion": True}, status=200)
        else:
            return Response({"confirmacion": False}, status=404)


class AgregarACarritoView(APIView):
    def post(self, request, format=None):
        sku = request.data.get("sku")
        cantidad = int(request.data.get("cantidad"))
        existe = CarritoDeCompra.objects.filter(sku=sku)
        if existe.count() > 0:
            cantidad_antigua = existe[0].cantidad
            carro_encontrado = CarritoDeCompra.objects.get(sku=sku)
            carro_encontrado.cantidad = cantidad_antigua+cantidad
            carro_encontrado.save()
        else:
            CarritoDeCompra.objects.create(sku=sku, cantidad=cantidad, usuario=request.user)
        return Response({}, status=200)


class CrearTransaccion(TemplateView):
    def post(self, request):
        print(request.data)

        # return render(request, "ventas/aa.html", context)


@csrf_exempt
def TransaccionExitosa(request):
    template_name = "ventas/transaccion-exitosa.html"
    if request.method == 'POST':
        token = request.POST.get("token_ws")
        response = Transaction.commit(token=token)
        context = {
            "buy_order": response.buy_order,
            "session_id": response.session_id,
            "amount": response.amount,
            "response": response,
            "token_ws": token,
            "status": response.status,
            "fecha_transaccion": response.transaction_date
        }
    # else:
    #     context = {
    #         "buy_order": "123",
    #         "session_id": "1",
    #         "amount": "1231123",
    #         "response": "response",
    #         "token_ws": "token",
    #         "status": "response.status",
    #         "fecha_transaccion": "response.transaction_date"
    #     }

    # VISA              4051885600446623
    #                   CVV 123
    return render(request, template_name, context)


producto_lista_view = ProductoListaView.as_view()
finalizar_compra_view = FinalizarCompraView.as_view()
comprobar_medio_de_pago_view = ComprobarMedioDePagoView.as_view()
agregar_a_carrito_view = AgregarACarritoView.as_view()
crear_transaccion_view = CrearTransaccion.as_view()
transaccion_exitosa_view = TransaccionExitosa
