import os, requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

from Utils.Utils import clear_terminal
from Model.PublicTransportData.BusStation import BusStation

class TransitlandAPI:
    def __init__(self, mongo_db):
        load_dotenv()
        self.geolocator = Nominatim(user_agent="TodaSP")

        self.key = os.getenv('TRANSITLAND_KEY')
        self.URL = "https://transit.land/api/v2/rest"
        self.headers = {"apikey": self.key}
        self.feed_id = "f-6gy-sptrans"

        self.mongo_db = mongo_db

    def get_all_stops(self):
        if not self.key:
            raise ValueError("Key da Transitland não encontrada.")

        print(f'Checando os pontos de SÃO PAULO (NÃO É POSSÍVEL INTERROMPER O PROCESSAMENTO)\n')

        parameters = {
            'feed_onestop_id': self.feed_id,
            'include_routes': 'true',
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

                print(f"Pontos coletados: {len(stops)}")

                if not after:
                    break

                parameters['after'] = after

            for stop in stops:
                lines = []

                for route_stop in stop.get('route_stops', []):
                    route = route_stop['route']

                    lines.append({
                        "id_linha": route['route_id'],
                        "nome_completo": route['route_long_name'],
                        "nome_curto": route['route_short_name']
                    })

                coordinates = stop.get('geometry', {}).get('coordinates', [])

                self.mongo_db.insert_bus_station(BusStation(
                    id_ponto=stop['stop_id'],
                    nome=stop['stop_name'],
                    latitude=coordinates[1],
                    longitude=coordinates[0],
                    linhas=lines
                ))

            print(f"\nPontos coletados e armazenados no banco de dados. ({len(stops)} registros)\n")

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False