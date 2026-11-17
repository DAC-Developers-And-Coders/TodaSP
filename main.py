import os
from threading import Thread
from scrapy.utils.reactor import install_reactor

from Utils.Utils import clear_terminal

install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

from twisted.internet import reactor
from Model.MenuManager import MenuManager

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'Scrapy.Scrapy.settings')

menu = MenuManager()

reactor_thread = Thread(target=reactor.run, kwargs={"installSignalHandlers": False}, name="TwistedReactor")

reactor_thread.start()

try:
    menu.start_menu()
except (KeyboardInterrupt, EOFError):
    clear_terminal()
    print("Sistema encerrado.")
finally:
    if reactor.running:
        reactor.callFromThread(reactor.stop)

    reactor_thread.join()