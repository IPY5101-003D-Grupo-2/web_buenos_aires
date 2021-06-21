from django.urls import path

from web_buenos_aires.ventas.views import (
    producto_lista_view,
    finalizar_compra_view,
    comprobar_medio_de_pago_view
)

app_name = "ventas"
urlpatterns = [
    path("productos/", view=producto_lista_view, name="producto-lista"),
    path("finalizar-compra/", view=finalizar_compra_view, name="finalizar-compra"),
    path("comprobar-medio-de-pago/", view=comprobar_medio_de_pago_view, name="comprar-medio-de-pago"),


]
