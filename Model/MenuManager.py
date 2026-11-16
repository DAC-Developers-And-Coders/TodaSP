import sys

from Database.MongoDB import MongoDB
from API.PiranotAPI import PiranotAPI
from API.GeoSampaWFS import GeoSampaWFS
from API.TransitlandAPI import TransitlandAPI
from API.TrilhosAgoraAPI import TrilhosAgoraAPI
from API.DadosAbertosAPI import DadosAbertosAPI
from Reader.ObservaSampaReader import ObservaSampaReader
from Utils.Utils import clear_terminal, colored_text, BOLD, RESET
from Scrapy.Scrapy.spiders.SubwayStationsSpider import SubwayStationsSpider

from scrapy import signals
from threading import Event
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

class MenuManager:
    def __init__(self):
        self.menuString = [f"======== Toda{colored_text('S', '#ff2828')}"
                           f"{BOLD}{colored_text('P', '#028a38')}{BOLD} ========",
                           "|[1] - Linhas de Metrô", "|[2] - Estações de Metrô","|[3] - Pontos de Ônibus",
                           "|[4] - Delegacias de polícia", "|[5] - Estabelecimentos de Saúde",
                           "|[6] - Ler dados de população e alagamentos de distritos e subprefeituras de São Paulo",
                           "|[0] - Sair\n"]

        self.mongo_db = MongoDB()
        self.piranot_api = PiranotAPI()
        self.transitland_api = TransitlandAPI(self.mongo_db)
        self.trilhos_agora_api = TrilhosAgoraAPI(self.mongo_db)
        self.dados_abertos_api = DadosAbertosAPI(self.mongo_db)
        self.observa_sampa_reader = ObservaSampaReader(self.mongo_db)
        self.geo_sampa_wfs = GeoSampaWFS(self.piranot_api, self.mongo_db)

        crawler_settings = get_project_settings()
        self.crawler_runner = CrawlerRunner(crawler_settings)

        reactor.addSystemEventTrigger('before', 'shutdown', self.mongo_db.client.close)

    def draw_menu(self):
        for line in self.menuString:
            print(f"{BOLD}{line}{RESET}")

    def start_menu(self):
        while True:
            clear_terminal()
            self.draw_menu()

            try:
                option = input()
            except (KeyboardInterrupt, EOFError):
                clear_terminal()
                print("Sistema encerrado.")
                return

            if not option.isnumeric():
                self.invalid_option()
                continue

            match int(option):
                case 1:
                    clear_terminal()
                    self.trilhos_agora_api.get_all_lines()
                case 2:
                    clear_terminal()
                    self.run_subway_stations_spider()
                case 3:
                    clear_terminal()
                    self.transitland_api.get_all_stops()
                case 4:
                    clear_terminal()
                    self.geo_sampa_wfs.get_all_police_stations()
                case 5:
                    clear_terminal()
                    self.dados_abertos_api.get_all_health_facilities()
                case 6:
                    clear_terminal()
                    self.observa_sampa_reader.read_all_data()
                case 0:
                    clear_terminal()
                    self.exit_system()
                    return
                case 10:
                    self.mongo_db.database['subway_stations'].delete_many({})
                case _:
                    self.invalid_option()
                    continue

    def run_subway_stations_spider(self):
        finished = Event()

        collected_subway_stations = 0

        def item_collected(item, response, spider):
            nonlocal collected_subway_stations

            collected_subway_stations += 1
            percentage = int((collected_subway_stations / 195) * 100)

            print(f"\rEstações coletadas ({percentage}%): {collected_subway_stations}", end="", flush=True)

        def crawl_finished(result):
            if result is None:
                print("\n\nColeta de estações finalizada.")
            else:
                print(f"\nErro durante a coleta das estações: {result}")

            print(f"Estações coletadas: {collected_subway_stations}")

            finished.set()
            return result

        def start_crawler():
            crawler = self.crawler_runner.create_crawler(SubwayStationsSpider)
            crawler.signals.connect(item_collected, signal=signals.item_scraped)

            crawl_run = self.crawler_runner.crawl(crawler, mongo_db=self.mongo_db)
            crawl_run.addBoth(crawl_finished)

        print("Coletando estações de metrô em São Paulo...\n")

        reactor.callFromThread(start_crawler)
        finished.wait()

        input("\nPressione ENTER para voltar ao menu.")

    @staticmethod
    def invalid_option():
        clear_terminal()
        print("Opção inválida, tente novamente.")
        input("Pressione ENTER para voltar ao menu.")
        clear_terminal()

    @staticmethod
    def exit_system():
        sys.stdout.flush()
        print("Sistema encerrado.")
        reactor.callFromThread(reactor.stop)