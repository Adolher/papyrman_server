import argparse
import logging

from dispatcher import Dispatcher
from utils import Logger


'''für jeden Client Inbox/<prefix>/<profile_id>/<target_id>/ Ordner erstellen
   Scanprofile anhand des Ordners auslesen'''


# Here just argument-parsing
# and calling dispatcher


class Papyrman:
    def __init__(self):
        self.dispatcher = Dispatcher()

        self.parser = argparse.ArgumentParser(prog='papyrman')
        self.subparsers = self.parser.add_subparsers()
        self.args = self.add_pars_args()

        self.logger = self.start_logger(self.args.ll, self.args.lf, self.args.lt)

        self.args = vars(self.args)

        self.logger.logger.debug(f"{self.args}")
        self.logger.logger.info("Initialized Papyrman Server")

        if 'fun' in self.args.keys():
            self.args['fun'](self.args)

    def add_pars_args(self):
        help_msg = "Specifies the Log(-File)-Level. Default is 'WARNING'"
        self.parser.add_argument('-lf', '--logfile-level', choices=['debug', 'info', 'warning', 'error', 'critical'],
                                 default='info', type=str, help=help_msg, dest='lf')

        help_msg = "Specifies the Terminal-output. Default is 'INFO'"
        self.parser.add_argument('-lt', '--terminal-output', choices=['silent', 'debug', 'info', 'warning', 'error', 'critical'],
                                 default='warning', type=str, help=help_msg, dest='lt')

        help_msg = "Specifies the Log(-File)-Level and Terminal-Output."
        self.parser.add_argument('-ll', '--log-level', choices=['silent', 'debug', 'info', 'warning', 'error', 'critical'],
                                 default=None, type=str, help=help_msg, dest='ll')

        help_msg = "shows the version of Papyrman-Server"
        parser_version = self.subparsers.add_parser('version', help=help_msg)
        parser_version.set_defaults(fun=self.dispatcher.version)

        help_msg = "Shows your ini-file.ini"
        parser_sini = self.subparsers.add_parser('ini', help=help_msg)
        parser_sini.set_defaults(fun=self.dispatcher.sini)

        help_msg = "Creates a User-Profile and save it to the DataBase"
        parser_cp = self.subparsers.add_parser('create-profile', help=help_msg)
        parser_cp.set_defaults(fun=self.dispatcher.cp)

        help_msg = "Shows a list of all Profiles"
        parser_sps = self.subparsers.add_parser('show-profiles', help=help_msg)
        parser_sps.set_defaults(fun=self.dispatcher.sps)

        help_msg = "'papyrman.py show-profile -id <profile_id>' -> shows the specified profile"
        parser_sp = self.subparsers.add_parser('show-profile', help=help_msg)
        parser_sp.add_argument('-id', type=int, dest='id', required=True)
        parser_sp.set_defaults(fun=self.dispatcher.sp)

        help_msg = "'papyrman.py delete-profile -id <profile_id>' -> delete the specified profile"
        parser_dp = self.subparsers.add_parser('delete-profile', help=help_msg)
        parser_dp.add_argument('-id', type=int, required=True)
        parser_dp.set_defaults(fun=self.dispatcher.dp)

        help_msg = "'papyrman.py edit-profile -id <profile_id>' -> edit the specified profile"
        parser_ep = self.subparsers.add_parser('edit-profile', help=help_msg)
        parser_ep.add_argument('-id', type=int, required=True)
        parser_ep.set_defaults(fun=self.dispatcher.ep)

        help_msg = "'papyrman.py add-target-to -id <profile_id>' -> add a target to the specified profile"
        parser_att = self.subparsers.add_parser('add-target-to', help=help_msg)
        parser_att.add_argument('-id', type=int, required=True)
        parser_att.set_defaults(fun=self.dispatcher.att)

        help_msg = "'papyrman.py edit-target -id <target_id>' -> edit the specified target"
        parser_et = self.subparsers.add_parser('edit-target', help=help_msg)
        parser_et.add_argument('-id', type=int, required=True)
        parser_et.set_defaults(fun=self.dispatcher.et)

        help_msg = "'papyrman.py delete-target -id <target_id>' -> delete the specified target"
        parser_dt = self.subparsers.add_parser('delete-target', help=help_msg)
        parser_dt.add_argument('-id', type=int, required=True)
        parser_dt.set_defaults(fun=self.dispatcher.dt)

        help_msg = "create a Database accordance your settings in papyrman.ini"
        parser_crdb = self.subparsers.add_parser('create-db', help=help_msg)
        parser_crdb.set_defaults(fun=self.dispatcher.crdb)

        help_msg = "connect to the Database"
        parser_codb = self.subparsers.add_parser('connect-db', help=help_msg)
        parser_codb.set_defaults(fun=self.dispatcher.codb)

        help_msg = "delete the Database"
        parser_ddb = self.subparsers.add_parser('drop-db', help=help_msg)
        parser_ddb.set_defaults(fun=self.dispatcher.ddb)

        help_msg = "run the Observer"
        parser_r = self.subparsers.add_parser('run', help=help_msg)
        parser_r.set_defaults(fun=self.dispatcher.run)

        help_msg = "stops the Observer"
        parser_s = self.subparsers.add_parser('stop', help=help_msg)
        parser_s.set_defaults(fun=self.dispatcher.stop)

        return self.parser.parse_args()

    @staticmethod
    def start_logger(ll, lf, lt):
        def translate(x):
            if x.lower() == "silent":
                return 60
            elif x.lower() == "critical":
                return logging.CRITICAL
            elif x.lower() == "error":
                return logging.ERROR
            elif x.lower() == "warning":
                return logging.WARNING
            elif x.lower() == "info":
                return logging.INFO
            elif x.lower() == "debug":
                return logging.DEBUG
        if ll is not None:
            if ll == "silent":
                return Logger(translate(lf), translate(ll))
            else:
                return Logger(translate(ll), translate(ll))
        else:
            return Logger(translate(lf), translate(lt))


start = Papyrman()
