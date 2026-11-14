import os, re, json, requests
from dotenv import load_dotenv

from Utils.Utils import clear_terminal

class PiranotAPI:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('PIRANOT_KEY')

        self.URL = "https://www.piranot.com.br/datax/api/v1/seguranca/ssp-sp/dp"
        self.headers = {"X-Api-Key": self.key}
        self.dps_numbers_ids = {}

        os.makedirs("data", exist_ok=True)

    def get_police_station_ids(self):
        if not self.key:
            raise ValueError("Key da Piranot não encontrada.")

        params = {
            "municipio": "São Paulo"
        }

        try:
            response = requests.get(self.URL, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            for dp in data.get("dps", []):
                dp_number = self.get_dp_number(dp["nome"])

                if dp_number and dp_number not in self.dps_numbers_ids:
                    #dp_regular_number = dp_number.lstrip("0")
                    self.dps_numbers_ids[dp["id"]] = dp_number

            clear_terminal()

        except Exception:
            clear_terminal()

    def get_police_reports_by_station(self, number):
        if not self.key:
            raise ValueError("Key da Piranot não encontrada.")

        if (len(self.dps_numbers_ids) <= 0) or (number not in self.dps_numbers_ids.values()):
            return None

        dp_id = self.get_dp_id(number)

        if not dp_id:
            return None

        params = {
            "municipio": "São Paulo",
            "dp": dp_id
        }

        with open("data/ids.txt", "a", encoding="utf-8") as f:
            f.write(f"DP ID: {dp_id}\n")

        try:
            response = requests.get(self.URL, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            natures = {}

            for n in data.get('naturezas', []):
                nature_id = int(n.get('id'))

                if nature_id not in natures:
                    natures[nature_id] = {
                        "Nome": n.get('nome'),
                        "Ano": n.get('acumulado').get('ano'),
                        "QuantidadeAno": n.get('acumulado').get('atual'),
                        "QuantidadeMes": n.get('ultimo_mes').get('valor')
                    }

            return natures

        except Exception as error:
            print(f"Erro na busca: {error}")
            clear_terminal()
            return None

    def get_dp_id(self, number):
        for dp_id, dp_number in self.dps_numbers_ids.items():
            if dp_number == number:
                return dp_id

        return None

    def get_dp_number(self, dp_name):
        string_match = re.match(r"^\d{3}\s*DP\s*-\s*", dp_name, re.IGNORECASE)

        if string_match:
            dp = string_match.group(0).partition(" DP -")[0]
            return int(dp)

        return None