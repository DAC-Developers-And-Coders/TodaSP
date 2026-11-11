import os
import requests
from tabulate import tabulate
from dotenv import load_dotenv

from Utils.Utils import clear_terminal, quicksort, colored_text, BOLD, RESET

class TrilhosAgoraAPI:
    def __init__(self):
        load_dotenv()

        self.key = os.getenv('TRILHOS_AGORA_KEY')
        self.URL = "https://api.trilhosagora.com.br/v1"
        self.headers = {"X-API-Key" : self.key}

    def get_all_lines(self):
        if not self.key:
            raise ValueError("Key da TrilhosAgora não encontrada.")

        try:
            response = requests.get(self.URL + '/status', headers=self.headers, timeout=15)
            response.raise_for_status()

            lines = response.json()["lines"]

            lines_dict = {}
            for line in lines:
                lines_dict[line['linha']] = [line['nome'], line['status'], line['cor']]

            keys = list(lines_dict.keys())
            quicksort(keys, 0, len(keys) - 1)

            table = []

            for key in keys:
                table.append([key, colored_text(lines_dict[key][0], lines_dict[key][2]), lines_dict[key][1]])

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
                    if line[0] == int(option):
                        self.get_stations(option, line[1])

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False

    def get_stations(self, line, line_name):
        if not self.key:
            raise ValueError("Key da TrilhosAgora não encontrada.")

        print(f'{BOLD}Checando as estações da linha {line_name}{RESET}\n')

        try:
            response = requests.get(self.URL + '/stations', params={'line': line}, headers=self.headers, timeout=15)
            response.raise_for_status()

            stations = response.json()["data"]

            table = []

            for index, station in enumerate(stations):
                table.append([index + 1, station["name"]])

            print(tabulate(table, headers=["Posição", "Nome"], tablefmt="heavy_grid", colalign=("left", "left", "left")))

            print()

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False