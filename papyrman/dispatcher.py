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

    # show papyrman.ini
    def sini(self, args):
        self.logger.info(f"{args}")
        self.ini = ConfigParser('papyrman.ini')
        ui_thread = threading.Thread(target=self.ini.show_config())
        ui_thread.start()

    # create profile
    def cp(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.create_profile())
        ui_thread.start()

    # show profiles
    def sps(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.show_profiles())
        ui_thread.start()

    # show profile -id <profile_id>
    def sp(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.show_profile(column='profile_id', value=args['id']))
        ui_thread.start()

    # delete profile -id <profile_id>
    def dp(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.delete_profile(column='profile_id', value=args['id']))
        ui_thread.start()

    # edit profile -id <profile_id>
    def ep(self, args):
        self.logger.info(f"{args}")
        pass

    # add target to -id <profile_id>
    def att(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.create_target(profile_id=args['id']))
        ui_thread.start()

    # edit target -id <target_id>
    def et(self, args):
        self.logger.info(f"{args}")
        pass

    # delete target -id <target_id>
    def dt(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.delete_target(column='target_id', value=args['id']))
        ui_thread.start()

    # create database (accordance .ini file)
    def crdb(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.create_db())
        ui_thread.start()

    # connect to database
    def codb(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.connect_db())
        ui_thread.start()

    # delete database
    def ddb(self, args):
        self.logger.info(f"{args}")
        self.init_clui()
        ui_thread = threading.Thread(target=self.clui.drop_db())
        ui_thread.start()

    # run observer
    def run(self, args):
        self.logger.info(f"{args}")
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

    # stop observer
    def stop(self, *args):
        self.logger.info(f"{args}")
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
        self.logger.info(f"{args}")
        print("version nummer sonstwas")    # ToDo: version aus ini lesen; mit argparse-version realisieren
