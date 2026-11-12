import json
import requests

from Utils.Utils import clear_terminal, BOLD, RESET, LEGAL_NATURE, FACILITIES_CODES

class DadosAbertosAPI:
    def __init__(self):
        self.URL = "https://apidadosabertos.saude.gov.br/cnes"
        self.headers = {"accept": "application/json"}
        self.facilities_codes_set = {code for codes in FACILITIES_CODES.values() for code in codes}

    def get_all_health_facilities(self):
        print(f'{BOLD}Checando os estabelecimentos de saúde na cidade de  SÃO PAULO{RESET}\n')

        parameters = {
            'codigo_uf': 35,
            'codigo_municipio': 355030,
            'status': 1,
            'limit': 20,
            'offset': 0
        }

        facilities = []
        seen_ids = set()

        try:
            while True:
                response = requests.get(self.URL + '/estabelecimentos', headers=self.headers, params=parameters, timeout=30)
                response.raise_for_status()

                data = response.json().get("estabelecimentos", [])

                if not data:
                    break

                current_facilities = []

                for facility in data:
                    facility_id = facility["codigo_cnes"]

                    if facility_id in seen_ids:
                        continue

                    seen_ids.add(facility_id)

                    if facility["codigo_tipo_unidade"] in self.facilities_codes_set:
                        current_facilities.append(facility)

                facilities.extend(current_facilities)

                print(
                    f"Página {parameters['offset'] + 1}: "
                    f"{len(current_facilities)} estabelecimentos coletados "
                    f"| Total: {len(facilities)}"
                )

                if len(data) < parameters["limit"]:
                    break

                parameters["offset"] += 1

            with open("data/health_facilities.json", "w", encoding="utf-8") as f:
                json.dump(facilities, f, ensure_ascii=False, indent=4)

            print(f"\nTotal coletado: {len(facilities)} estabelecimentos.")

            print()

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False