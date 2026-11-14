import requests, json, re

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

        self.police_stations = {}

    def get_police_station(self, dp_number):
        if dp_number not in self.police_stations:
            self.police_stations[dp_number] = {
                "Dados": {}
            }

        return self.police_stations[dp_number]

    def get_all_police_stations(self):
        try:
            self.piranot_api.get_police_station_ids()

            response = requests.get(self.URL, params=self.params, timeout=15).json()

            data = response["features"]

            for d in data:
                properties = d.get("properties")
                dp_number = self.get_dp_number(properties.get("nm_equipamento"))

                if dp_number and dp_number in self.piranot_api.dps_numbers_ids.values():
                    station_record = self.get_police_station(int(dp_number))

                    station_record["Dados"]["Nome"] = properties.get("nm_equipamento")
                    station_record["Dados"]["Endereco"] = properties.get("tx_endereco_equipamento")
                    station_record["Dados"]["Classe"] = properties.get("nm_classe_equipamento")

            for station in self.police_stations.values():
                print(f"{station["Dados"]["Nome"]} - {station["Dados"]["Endereco"]} - {station["Dados"]["Classe"]}")

            print(f"\nTotal coletado: {len(self.police_stations)} delegacias.")

            option = input("\nDigite o número da delegacia para verificar suas ocorrências criminais \nEXEMPLO - se 33°, digite 33: ")

            print()

            if option.isnumeric() and int(option) in self.piranot_api.dps_numbers_ids.values():
                reports = self.piranot_api.get_police_reports_by_station(int(option))

                if reports:
                    self.get_police_station(int(option))["Casos"] = reports

                    for report in reports.values():
                        print(f"Natureza: {report["Nome"]}, Quantidade Último Mês: {report["QuantidadeMes"]}, "
                                f"Quantidade {report["Ano"]}: {report["QuantidadeAno"]}")
            else:
                input("\nNenhuma delegacia encontrada, pressione ENTER para voltar ao menu.")
                clear_terminal()

            with open("data/police_stations.json", "w", encoding="utf-8") as f:
                json.dump(self.police_stations, f, ensure_ascii=False, indent=4)

            input("\nPressione ENTER para voltar ao menu.")
            clear_terminal()

        except Exception as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False

    def get_dp_number(self, dp_name):
        string_match = re.match(r"\d{1,3}", dp_name, re.IGNORECASE)

        if string_match:
            dp = int(string_match.group())
            return dp

        return None