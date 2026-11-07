import os
import sys

from API.OlhoVivoAPI import OlhoVivoAPI
from API.TrilhosAgoraAPI import TrilhosAgoraAPI
from Utils.Utils import clear_terminal, colored_text, BOLD, RESET

class MenuManager:
    def __init__(self):
        self.menuString = [f"======== Toda{colored_text('S', '#ff2828')}"
                           f"{BOLD}{colored_text('P', '#028a38')}{BOLD} ========",
                           "|[1] - Linhas de Metrô", "|[0] - Sair\n"]

        self.olhoVivoAPI = OlhoVivoAPI()
        self.trilhosAgoraAPI = TrilhosAgoraAPI()
        self.start_menu()

    def draw_menu(self):
        for line in self.menuString:
            print(f"{BOLD}{line}{RESET}")

    def start_menu(self):
        while True:
            clear_terminal()
            self.draw_menu()
            option = input()

            if not option.isnumeric():
                self.invalid_option()
                continue

            match int(option):
                case 10:
                    clear_terminal()
                    self.olhoVivoAPI.authenticate()
                case 1:
                    clear_terminal()
                    self.trilhosAgoraAPI.get_all_lines()
                case 0:
                    clear_terminal()
                    print("Sistema encerrado.")
                    sys.stdout.flush()
                    self.exit_system()
                case _:
                    self.invalid_option()
                    continue

    def invalid_option(self):
        clear_terminal()
        print("Opção inválida, tente novamente.")
        input("Pressione ENTER para voltar ao menu.")
        clear_terminal()

    @staticmethod
    def exit_system():
        os._exit(0)