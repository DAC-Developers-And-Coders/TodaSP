import requests, re

from Utils.Utils import clear_terminal
from Model.PoliceData.PoliceStation import PoliceStation

class GeoSampaWFS:
    def __init__(self, piranot_api, mongo_db):
        self.piranot_api = piranot_api
        self.URL = "https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/geoportal/wfs"

        self.params = {
            "service": "WFS",
            "request": "GetFeature",
            "typeName": "geoportal:equipamento_policia_civil",
            "outputFormat": "application/json"
        }

        self.mongo_db = mongo_db

    def get_all_police_stations(self):
        print("Buscando delegacias de São Paulo...\n")

        try:
            self.piranot_api.get_police_station_ids()

            response = requests.get(self.URL, params=self.params, timeout=15).json()

            data = response["features"]

            if not data:
                raise ValueError("Nenhuma delegacia encontrada.")

            stations_counter = 0

            for d in data:
                properties = d.get("properties")
                dp_number = self.get_dp_number(properties.get("nm_equipamento"))

                if dp_number and dp_number in self.piranot_api.dps_numbers_ids.values():

                    station = PoliceStation(
                        numero_dp=int(dp_number),
                        nome=properties.get("nm_equipamento"),
                        endereco=properties.get("tx_endereco_equipamento"),
                        classe=properties.get("nm_classe_equipamento")
                    )

                    self.mongo_db.insert_police_station(station)

                    print(f"{station.name} - {station.address} - {station.station_type}")
                    stations_counter += 1

            print(f"\nTotal coletado: {stations_counter} delegacias.")

            option = input("\nDigite o número da delegacia para verificar suas ocorrências criminais \nEXEMPLO - se 33°, digite 33: ")

            print()

            if option.isnumeric() and int(option) in self.piranot_api.dps_numbers_ids.values():
                reports = self.piranot_api.get_police_reports_by_station(int(option))

                if reports:
                    self.mongo_db.insert_police_station_reports(int(option), reports)

                    for report in reports:
                        print(f"Natureza: {report.nature}, Quantidade Último Mês: {report.last_month_reports}, "
                                f"Quantidade {report.year}: {report.year_reports}")
            else:
                input("\nNenhuma delegacia encontrada, pressione ENTER para voltar ao menu.")
                clear_terminal()

            input("\nPressione ENTER para voltar ao menu.")
            clear_terminal()

        except Exception as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

    @staticmethod
    def get_dp_number(dp_name):
        string_match = re.match(r"\d{1,3}", dp_name, re.IGNORECASE)

        if string_match:
            dp = int(string_match.group())
            return dp

        return None