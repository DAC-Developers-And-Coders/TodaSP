# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SubwayStationItem(Item):
    name = Field()
    address = Field()
    operating_hours = Field()
    transfers = Field()
    lines = Field()
    info_date = Field()