import os, json, requests
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

    def display_lines(self, lines, from_database=False):
        keys = [line.line_number for line in lines]
        quicksort(keys, 0, len(keys) - 1)

        lines_by_number = {line.line_number: line for line in lines}

        table = []

        for key in keys:
            line = lines_by_number[key]
            table.append([key, colored_text(line.name, line.color), line.status])

        print(tabulate(table, headers=["Linha", "Nome", "Status"], tablefmt="rounded_grid", colalign=("left", "left", "left")))

        option = input("\nDigite o número da linha que deseja checar as estações, ou digite 0 para voltar ao menu: ")

        if option == "0":
            clear_terminal()
            return

        if not option.isnumeric() or int(option) not in keys:
            print("\nOpção inválida.")
            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

            return

        clear_terminal()

        numero_linha = int(option)

        for line in table:
            if int(line[0]) == numero_linha:
                self.get_stations(numero_linha, line[1], from_database)
                break

    def get_database_data(self):
        full_subway_lines_data = self.mongo_db.get_all_data_from_collection('subway_lines')

        lines = []

        for line in full_subway_lines_data:
            lines.append(SubwayLine(
                numero_linha=line['numero_linha'],
                nome=line['nome'],
                rotulo=line['rotulo'],
                cor=line['cor'],
                status=line['status'],
                operadora=line['operadora'],
                data_atualizacao=line['data_atualizacao'],
                rota=line.get('rota', [])
            ))

        self.display_lines(lines, True)

    def get_all_lines(self, option: str):
        if option == "n":
            self.get_database_data()
            return

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

            for line in lines:
                self.mongo_db.insert_subway_line(line)

            self.display_lines(lines)

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

    def get_stations(self, line_number, line_name, from_database=False):
        print(f'{BOLD}Checando as estações da linha {line_name}{RESET}\n')

        if from_database:
            full_subway_line_route_data = self.mongo_db.database['subway_lines'].find_one(
                {"numero_linha": line_number},
                {"_id": 0, "rota": 1}
            )

            stations = full_subway_line_route_data.get("rota") if full_subway_line_route_data else None

            if stations:
                table = [[station["posicao"], station["nome"]] for station in stations]

                print(tabulate(table, headers=["Posição", "Nome"], tablefmt="heavy_grid", colalign=("left", "left")))

                input("\nPressione ENTER para voltar ao menu.")
                clear_terminal()
                return

        if not self.key:
            raise ValueError("Key da TrilhosAgora não encontrada.")

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

    def save_data(self):
        full_subway_lines_data = self.mongo_db.get_all_data_from_collection('subway_lines')

        with open('data/subway_lines', 'w', encoding='utf-8') as file:
            json.dump(full_subway_lines_data, file, ensure_ascii=False, indent=4)