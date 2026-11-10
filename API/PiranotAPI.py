import os, re, json, requests
from dotenv import load_dotenv

from Utils.Utils import clear_terminal

class PiranotAPI:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('PIRANOT_KEY')

        self.URL = "https://www.piranot.com.br/datax/api/v1/seguranca/ssp-sp/dp"
        self.headers = {"X-Api-Key": self.key}

        os.makedirs("data", exist_ok=True)

    def get_police_reports(self):
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
                self.get_dp_number(dp["nome"])

            with open("data/police_reports.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print()

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na busca: {error}")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False

    def get_dp_number(self, dp_name):
        string_match = re.match(r"^\d{3}\s*DP\s*-\s*", dp_name, re.IGNORECASE)

        if string_match:
            dp = string_match.group(0).partition(" DP -")[0]
            return dp

        return None