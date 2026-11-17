import requests, re

from tabulate import tabulate

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

    def get_all_police_stations(self, collect_from_api):
        if not collect_from_api:
            self.get_database_data()
            return

        print("Buscando delegacias de São Paulo...\n")

        try:
            self.piranot_api.get_police_station_ids()

            response = requests.get(self.URL, params=self.params, timeout=15).json()

            data = response["features"]

            if not data:
                raise ValueError("Nenhuma delegacia encontrada.")

            stations_counter = 0

            table = []

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

                    table.append([station.name, station.address, station.station_type])
                    stations_counter += 1

            print("========== DELEGACIAS DE SP ==========\n")
            print(tabulate(table, headers=["Delegacia", "Endereço", "Classe"], tablefmt="rounded_grid", colalign=("left", "left", "left")))

            print(f"\nTotal coletado: {stations_counter} delegacias.\nDados completos no banco de dados.")

            option = input("\nDigite o número da delegacia para verificar suas ocorrências criminais \nEXEMPLO - se 33°, digite 33: ")

            print()

            if option.isnumeric() and int(option) in self.piranot_api.dps_numbers_ids.values():
                reports = self.piranot_api.get_police_reports_by_station(int(option))

                if reports:
                    self.mongo_db.insert_police_station_reports(int(option), reports)
                    self.print_api_reports(reports)
            else:
                input("\nNenhuma delegacia encontrada, pressione ENTER para voltar ao menu.")
                clear_terminal()

            input("\nPressione ENTER para voltar ao menu.")
            clear_terminal()

        except Exception as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

    def get_database_data(self):
        data = self.mongo_db.get_all_data_from_collection('police_stations')

        table = []

        for station in data:
            police_station = PoliceStation(
                numero_dp=station.get("numero_dp"),
                nome=station.get("nome"),
                endereco=station.get("endereco"),
                classe=station.get("classe"),
                casos=station.get("casos")
            )

            table.append([police_station.name, police_station.address, police_station.station_type])

        print("========== DELEGACIAS DE SP ==========\n")
        print(tabulate(table, headers=["Delegacia", "Endereço", "Classe"], tablefmt="rounded_grid", colalign=("left", "left", "left")))

        print(f"\nDados completos no banco de dados.")

        option = input("\nDigite o número da delegacia para verificar suas ocorrências criminais \nEXEMPLO - se 33°, digite 33: ")

        print()

        dp_numbers = [station.get("numero_dp") for station in data]

        if option.isnumeric() and int(option) in dp_numbers:
            for dp in data:
                if int(option) == dp.get("numero_dp"):
                    reports = dp.get("casos")

                    if not reports:
                        self.piranot_api.get_police_station_ids(False)
                        reports = self.piranot_api.get_police_reports_by_station(int(option))

                        if reports:
                            self.mongo_db.insert_police_station_reports(int(option), reports)
                            self.print_api_reports(reports)
                        else:
                            print("\nReports está vazio")

                        input("\nPressione ENTER para voltar ao menu.")
                        clear_terminal()
                        return

                    table = []
                    ano = reports[0].get("ano")
                    for report in reports:
                        table.append([report.get("natureza"), report.get("quantidade_ultimo_mes"),
                                      report.get("quantidade_ultimo_ano")])

                    print(tabulate(table, headers=["Natureza", "Quantidade Último Mês ", f"Quantidade {ano}"],
                                   tablefmt="rounded_grid", colalign=("left", "left", "left")))

        input("\nPressione ENTER para voltar ao menu.")
        clear_terminal()

    @staticmethod
    def print_api_reports(reports):
        table = []
        ano = reports[0].year
        for report in reports:
            table.append([report.nature, report.last_month_reports, report.year_reports])

        print(tabulate(table, headers=["Natureza", "Quantidade Último Mês ", f"Quantidade {ano}"],
                       tablefmt="rounded_grid", colalign=("left", "left", "left")))

    @staticmethod
    def get_dp_number(dp_name):
        string_match = re.match(r"\d{1,3}", dp_name, re.IGNORECASE)

        if string_match:
            dp = int(string_match.group())
            return dp

        return None