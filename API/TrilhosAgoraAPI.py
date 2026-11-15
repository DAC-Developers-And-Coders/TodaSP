import os
import requests
from tabulate import tabulate
from dotenv import load_dotenv

from Model.PublicTransportData.SubwayLine import SubwayLine
from Utils.Utils import clear_terminal, quicksort, colored_text, BOLD, RESET

class TrilhosAgoraAPI:
    def __init__(self, mongo_db):
        load_dotenv()

        self.key = os.getenv('TRILHOS_AGORA_KEY')
        self.URL = "https://api.trilhosagora.com.br/v1"
        self.headers = {"X-API-Key" : self.key}

        self.mongo_db = mongo_db

    def get_all_lines(self):
        if not self.key:
            raise ValueError("Key da TrilhosAgora não encontrada.")

        try:
            response = requests.get(self.URL + '/status', headers=self.headers, timeout=15)
            response.raise_for_status()

            lines_data = response.json()["lines"]

            lines = []

            for line in lines_data:
                lines.append(SubwayLine(
                    numero_linha=line['linha'],
                    nome=line['nome'],
                    rotulo=line['rotulo'],
                    cor=line['cor'],
                    status=line['status'],
                    operadora=line['operadora'],
                    data_atualizacao=line['atualizado_em']
                ))

            keys = [line.line_number for line in lines]
            quicksort(keys, 0, len(keys) - 1)

            table = []

            for i, key in enumerate(keys):
                line = lines[i]
                self.mongo_db.insert_subway_line(line)
                table.append([key, colored_text(line.name, line.color), line.status])

            print(tabulate(table, headers=["Linha", "Nome", "Status"], tablefmt="rounded_grid", colalign=("left", "left", "left")))

            option = input("\nDigite o número da linha que deseja checar as estações, ou digite 0 para voltar ao menu: ")

            if option == "0":
                clear_terminal()
            elif not option.isnumeric() and int(option) not in keys:
                print("\nOpção inválida.")
                input("Pressione ENTER para voltar ao menu.")
                clear_terminal()
            else:
                clear_terminal()

                for line in table:
                    numero_linha = int(line[0])

                    if numero_linha == int(option):
                        self.get_stations(numero_linha, line[1])

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False

    def get_stations(self, line_number, line_name):
        if not self.key:
            raise ValueError("Key da TrilhosAgora não encontrada.")

        print(f'{BOLD}Checando as estações da linha {line_name}{RESET}\n')

        try:
            response = requests.get(self.URL + '/stations', params={'line': line_number}, headers=self.headers, timeout=15)
            response.raise_for_status()

            stations_data = response.json()["data"]

            stations = []
            table = []

            for index, station in enumerate(stations_data):
                stations.append({
                    "posicao": index + 1,
                    "nome": station["name"]
                })

                table.append([index + 1, station["name"]])

            self.mongo_db.insert_subway_line_route(line_number, stations)

            print(tabulate(table, headers=["Posição", "Nome"], tablefmt="heavy_grid", colalign=("left", "left", "left")))

            print()

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False