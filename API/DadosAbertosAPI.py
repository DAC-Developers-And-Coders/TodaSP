import json, requests

from Model.HealthFacility import HealthFacility
from Utils.Utils import clear_terminal, BOLD, RESET, LEGAL_NATURE, FACILITIES_CODES

class DadosAbertosAPI:
    def __init__(self, mongo_db):
        self.URL = "https://apidadosabertos.saude.gov.br/cnes"
        self.headers = {"accept": "application/json"}
        self.facilities_codes_set = {code for codes in FACILITIES_CODES.values() for code in codes}

        self.mongo_db = mongo_db

    @staticmethod
    def get_legal_nature(code):
        return next((k for k, v in LEGAL_NATURE.items() if code in v), None)

    @staticmethod
    def get_facility_type(code):
        return next((k for k, v in FACILITIES_CODES.items() if code in v), None)

    def get_all_health_facilities(self):
        print(f'{BOLD}Checando os estabelecimentos de saúde na cidade de  SÃO PAULO{RESET}\n')

        parameters = {
            'codigo_uf': 35,
            'codigo_municipio': 355030,
            'status': 1,
            'limit': 20,
            'offset': 0
        }

        facility_counter = 0

        try:
            while True:
                response = requests.get(self.URL + '/estabelecimentos', headers=self.headers, params=parameters, timeout=30)
                response.raise_for_status()

                data = response.json().get("estabelecimentos", [])

                if not data:
                    break

                for facility in data:
                    facility_id = facility["codigo_cnes"]
                    facility_type_code = facility["codigo_tipo_unidade"]

                    if facility_type_code not in self.facilities_codes_set:
                        continue

                    legal_nature_code = facility["descricao_natureza_juridica_estabelecimento"]

                    if facility["bairro_estabelecimento"] == "SAO PAULO":
                        bairro = None
                    else:
                        bairro = facility["bairro_estabelecimento"]

                    health_facility = HealthFacility(
                        cnes_id=facility_id,
                        razao_social=facility["nome_razao_social"],
                        nome_fantasia=facility["nome_fantasia"],
                        esfera_administrativa=facility["descricao_esfera_administrativa"],
                        codigo_tipo=facility_type_code,
                        tipo=self.get_facility_type(facility_type_code),
                        cep=facility["codigo_cep_estabelecimento"],
                        endereco=facility["endereco_estabelecimento"],
                        numero=facility["numero_estabelecimento"],
                        bairro=bairro,
                        latitude=facility["latitude_estabelecimento_decimo_grau"],
                        longitude=facility["longitude_estabelecimento_decimo_grau"],
                        codigo_natureza_juridica=legal_nature_code,
                        natureza_juridica=self.get_legal_nature(legal_nature_code),
                        data_informacoes=facility["data_atualizacao"]
                    )

                    self.mongo_db.insert_health_facility(health_facility)

                    facility_counter += 1

                print(
                    f"Página {parameters['offset'] + 1}: "
                    f"| Total: {facility_counter}"
                )

                if len(data) < parameters["limit"]:
                    break

                parameters["offset"] += 1

            print(f"\nTotal coletado: {facility_counter} estabelecimentos.")

            input("\nPressione ENTER para voltar ao menu.")
            clear_terminal()

        except Exception as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False