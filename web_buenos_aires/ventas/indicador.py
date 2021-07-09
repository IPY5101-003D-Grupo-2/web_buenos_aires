import json
import requests


class Mindicador:

    def __init__(self, indicador):
        self.indicador = indicador

    def valor_actual(self):
        url = f'https://mindicador.cl/api/{self.indicador}'
        response = requests.get(url)
        data = json.loads(response.text.encode("utf-8"))
        valor = data['serie'][0]['valor']
        return float(valor)
