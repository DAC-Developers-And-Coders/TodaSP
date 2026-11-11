import requests, json

from Utils.Utils import clear_terminal

class GeoSampaWFS:
    def __init__(self, piranot_api):
        self.piranot_api = piranot_api
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

            chosen_pf = input("Digite o número da delegacia para verificar suas ocorrências criminais \nEXEMPLO - se 33°, digite 33: ")

            if chosen_pf.isnumeric() and chosen_pf in self.piranot_api.dps_numbers_ids.values():
                try:
                     if not self.piranot_api.get_police_reports_by_number(chosen_pf):
                         raise Exception
                except Exception as ex:
                    input("\nFalha ao encontrar registro, pressione ENTER para voltar ao menu.")
                    clear_terminal()
            else:
                input("\nNenhuma delegacia encontrada, pressione ENTER para voltar ao menu.")
                clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False