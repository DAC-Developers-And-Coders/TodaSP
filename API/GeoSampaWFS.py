import requests, json

from Utils.Utils import clear_terminal

class GeoSampaWFS:
    def __init__(self):
        self.URL = "https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/geoportal/wfs"

        self.params = {
            "service": "WFS",
            "request": "GetFeature",
            "typeName": "geoportal:equipamento_policia_civil",
            "outputFormat": "application/json"
        }

    def get_all_police_offices(self):
        try:
            response = requests.get(self.URL, params=self.params, timeout=15).json()

            police_offices = response["features"]

            for po in police_offices:
                properties = po.get("properties")
                print(f"{properties.get('nm_equipamento')} - {properties.get('tx_endereco_equipamento')} - {properties.get('nm_classe_equipamento')}")

            with open("data/police_stations.json", "w", encoding="utf-8") as f:
                json.dump(response, f, ensure_ascii=False, indent=4)

            print()

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False