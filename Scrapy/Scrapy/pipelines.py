# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem
from Scrapy.Scrapy.items import SubwayStationItem
from Model.PublicTransportData.SubwayStation import SubwayStation

class ValidationPipeline:
    def process_item(self, item):
        if isinstance(item, SubwayStationItem):
            fields_to_search = ['name', 'address', 'info_date']
        else:
            raise DropItem("Item não é uma estação")

        fields_missing = self.get_missing_fields(item, fields_to_search)

        if fields_missing:
            raise DropItem(f"Item não possui campos obrigatórios: {fields_missing}")

        return item

    @staticmethod
    def get_missing_fields(item, fields):
        return [field for field in fields if not item.get(field)]

class DuplicatesPipeline:
    def __init__(self):
        self.seen_items = set()

    def process_item(self, item):
        adapter = ItemAdapter(item)

        key = (adapter['name'], adapter['address'], tuple(adapter.get('lines') or []))

        if key in self.seen_items:
            raise DropItem(f"Item já foi coletado: {key}")
        else:
            self.seen_items.add(key)
            return item

class MongoPipeline:
    def __init__(self):
        self.crawler = None
        self.mongo_db = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self):
        self.mongo_db = self.crawler.spider.mongo_db

    def process_item(self, item):
        adapter = ItemAdapter(item)
        item_dict = adapter.asdict()

        station = SubwayStation(
            nome=item_dict["name"],
            endereco=item_dict["address"],
            horario_funcionamento=item_dict["operating_hours"],
            integracoes=item_dict["transfers"],
            data_informacoes=item_dict["info_date"],
            linhas=item_dict["lines"]
        )

        self.mongo_db.insert_subway_station(station)

        return item