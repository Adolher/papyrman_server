import threading
import logging
import sys

from core import DirObserver, FileProcessor
from DB_Interface import Profiles, DataBase
from UI import CLUI
from utils import ConfigParser


class Dispatcher:
    def __init__(self):
        self.logger = logging.getLogger('papyrman')
        self.logger.info("")
        self.ini = None
        self.db = None
        self.clui = None
        self.observer = None

    def sini(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        self.ini = ConfigParser('papyrman.ini')
        ui_thread = threading.Thread(target=self.ini.show_config())
        ui_thread.start()

    def cp(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.create_profile())
        ui_thread.start()

    def sps(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.show_profiles())
        ui_thread.start()

    def sp(self, *args):
        self.logger.info(f"{args}")
        self.init_clui()

        self.logger.info(f"ID={args}")
        ui_thread = threading.Thread(target=self.clui.show_profile(column='profile_id', value=args['id']))
        ui_thread.start()

    def dp(self, *args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.delete_profile(column='profile_id', value=args.id))
        ui_thread.start()

    def ep(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        pass

    def att(self, args):
        self.logger.info(f"{sys.argv[1:]}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.create_target(profile_id=args.id))
        ui_thread.start()

    def et(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        pass

    def dt(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.delete_target(column='target_id', value=args.id))
        ui_thread.start()

    def crdb(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.create_db())
        ui_thread.start()

    def codb(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.connect_db())
        ui_thread.start()

    def ddb(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.drop_db())
        ui_thread.start()

    def run(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        if self.ini is None:
            self.ini = ConfigParser('papyrman.ini')
        if self.db is None:
            self.db = DataBase(self.ini)
        self.observer = DirObserver(ini=self.ini, profiles=Profiles(self.ini, self.db), o_create_func=FileProcessor)

        try:
            while self.observer.observer.is_alive():
                self.observer.observer.join(1)
        except KeyboardInterrupt:
            self.observer.observer.stop()
            self.observer.observer.join()

    def stop(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        pass

    def init_clui(self):
        self.logger.info(f"{sys.argv[1:]}")
        if self.clui is None:
            if self.ini is None:
                self.ini = ConfigParser('papyrman.ini')
            if self.db is None:
                self.db = DataBase(self.ini)
            self.clui = CLUI(self.ini, self.db)

    def version(self, *args):
        self.logger.info(f"{sys.argv[1:]}")
        print("version nummer sonstwas")    # ToDo: version aus ini lesen; mit argparse-version realisieren
