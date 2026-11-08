import os
import requests
from dotenv import load_dotenv

from Utils.Utils import clear_terminal

class OlhoVivoAPI:
    def __init__(self):
        load_dotenv()

        self.key = os.getenv('OLHO_VIVO_API_TOKEN')
        self.URL = "https://api.olhovivo.sptrans.com.br/v2.1"

        self.session = requests.Session()
        self.authenticated = False

    def authenticate(self):
        if not self.key:
            raise ValueError("Token da SPTrans não encontrado.")

        try:
            auth_response = self.session.post(self.URL + f'/Login/Autenticar?token={self.key}', json={}, data={}, timeout=15)
            auth_response.raise_for_status()

            print(f"Status Code: {auth_response.status_code}\n{auth_response.json()}\n")

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()

        except requests.RequestException as error:
            print(f"Erro na autenticação: {error}")
            self.authenticated = False

            input("Pressione ENTER para voltar ao menu.")
            clear_terminal()
            return False