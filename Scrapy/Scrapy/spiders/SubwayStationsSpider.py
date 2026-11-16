from scrapy import Spider
from datetime import datetime
from curl_cffi import requests
from scrapy.http import HtmlResponse
from curl_cffi.requests.exceptions import RequestException

from Utils.Utils import remove_accents
from Scrapy.Scrapy.items import SubwayStationItem

class SubwayStationsSpider(Spider):
    name = "subway_stations"
    allowed_domains = ["trilhosagora.com.br"]
    start_url = "https://trilhosagora.com.br/saopaulo/estacoes"

    needed_info = [
        'Horário de funcionamento',
        'Integrações disponíveis',
        'Endereço da Estação'
    ]

    def __init__(self, mongo_db=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mongo_db = mongo_db
        self.default_station_url = "https://trilhosagora.com.br/saopaulo/estacao/"

        self.station_names = []
        self.processed_stations = set()

    async def start(self):
        try:
            response = requests.get(self.start_url, impersonate="chrome", timeout=60)
            response.raise_for_status()

            scrapy_response = HtmlResponse(url=self.start_url, body=response.content, encoding="utf-8")

            self.parse_stations_names(scrapy_response)

            for item in self.parse_stations():
                yield item
        except RequestException as e:
            print(f"Erro ao acessar primeira página: {e}")

    def parse_stations_names(self, response):
        stations = response.xpath('//div[@class="station-directory"]//a[contains(@href, "/saopaulo/estacao/")]')

        for station in stations:
            station_name = remove_accents(
                station.css("::text").get().strip().lower().replace(" (", "-")
                .replace(")", "").replace(" ", "-").replace("/", "-")
            )

            if station_name not in self.station_names:
                self.station_names.append(station_name)

    def parse_stations(self):
        for station_name in self.station_names:
            if station_name in self.processed_stations:
                continue

            yield from self.process_stations(station_name)

    def process_stations(self, station_name):
        if station_name in self.processed_stations:
            return

        self.processed_stations.add(station_name)

        try:
            response = requests.get(self.default_station_url + station_name, impersonate="chrome", timeout=30)
            response.raise_for_status()

            scrapy_response = HtmlResponse(url=self.default_station_url + station_name, body=response.content, encoding="utf-8")

            yield from self.parse_station_data(scrapy_response)
        except Exception as e:
            print(f"Erro ao acessar página da estação {station_name}: {e}")

    def parse_station_data(self, response):
        station_data = response.xpath('//div[@class="page-aside"]//div[@class="station-info-grid"]'
                                      '//article[contains(@class, "station-info-card")]')

        data = {}

        for info_block in station_data:
            info_title = info_block.xpath('normalize-space(.//h3)').get(default="").strip()
            info_description = info_block.xpath('normalize-space(.//p)').get(default="").strip()

            for i, ni in enumerate(self.needed_info):
                if ni in info_title:
                    if i == 0:
                        data["operating_hours"] = info_description
                    elif i == 1:
                        data["transfers"] = info_description
                    elif i == 2:
                        data["address"] = info_description

        main_data = response.xpath('//section[@class="station-hero"]//h1')
        data["name"] = main_data.xpath('normalize-space(.)').get().strip()

        lines = []

        lines_info = response.xpath('//div[@class="station-status-grid"]'
                                    '//div[contains(@class, "station-line-card__heading")]'
                                    '//a[contains(@href, "/saopaulo/linha/")]')

        for line in lines_info:
            line_name = line.css("::text").get().strip()

            if line_name not in lines:
                lines.append(line_name)

        data["lines"] = lines
        data["info_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield SubwayStationItem(**data)