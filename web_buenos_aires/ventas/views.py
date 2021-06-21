from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
import zeep
import requests


class ProductoListaView(TemplateView):
    template_name = "ventas/producto-lista.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get('https://ws-buenos-aires.herokuapp.com/inventario/')
        productos = response.json()
        context['productos'] = productos
        return context


class FinalizarCompraView(TemplateView):
    template_name = "ventas/finalizar-compra.html"


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


producto_lista_view = ProductoListaView.as_view()
finalizar_compra_view = FinalizarCompraView.as_view()
comprobar_medio_de_pago_view = ComprobarMedioDePagoView.as_view()
