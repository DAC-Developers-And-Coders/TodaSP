import os
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

from Utils.Utils import clear_terminal

class TransitlandAPI:
    def __init__(self):
        load_dotenv()
        self.geolocator = Nominatim(user_agent="TodaSP")

        self.key = os.getenv('TRANSITLAND_KEY')
        self.URL = "https://transit.land/api/v2/rest"
        self.headers = {"apikey": self.key}
        self.feed_id = "f-6gy-sptrans"

    def get_all_stops(self):
        if not self.key:
            raise ValueError("Key da Transitland não encontrada.")

        print(f'Checando os pontos de SÃO PAULO\n')

        parameters = {
            'feed_onestop_id': self.feed_id,
            'limit': 1000
        }

        stops = []

        try:
            while True:
                response = requests.get(self.URL + '/stops', params=parameters, headers=self.headers, timeout=30)
                response.raise_for_status()

                data = response.json()
                stops.extend(data.get('stops', []))

                after = data.get('meta', {}).get('after')

                if not after:
                    break

                parameters['after'] = after

            for stop in stops:
                #coordinates = stop.get('geometry', {}).get('coordinates', [])
                #location = self.geolocator.reverse(f"{coordinates[1]}, {coordinates[0]}", language='pt', timeout=30)
                print(f"{stop['stop_id']} - {stop['stop_name']}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False