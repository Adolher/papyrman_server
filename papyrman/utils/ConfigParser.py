import configparser
import logging


class ConfigParser:
    def __init__(self, file):
        self.logger = logging.getLogger('papyrman')
        self.logger.info(f"Read Data from {file}")
        self.configs = {}
        conf = configparser.ConfigParser()
        conf.read(file)
        sections = conf.sections()
        for section in sections:
            values = {}
            for value in conf[section]:
                values[value] = conf[section][value]
            self.configs[section] = values

    def show_config(self):
        for x in self.configs:
            print("\n[" + x + "]")
            for y in self.configs[x]:
                print(y + " = " + str(self.configs[x][y]))
