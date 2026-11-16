import os
from scrapy.utils.reactor import install_reactor

install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

from twisted.internet import reactor
from Model.MenuManager import MenuManager

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'Scrapy.Scrapy.settings')

menu = MenuManager()

reactor.callWhenRunning(reactor.callInThread, menu.start_menu)
reactor.run()