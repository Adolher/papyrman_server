# ToDo: Better User-input check ( names not only alpha-num)
# ToDo: if show_profiles has no results -> say that it has no results

import logging
import sys


class CLUI:
    def __init__(self, ini, db):
        self.logger = logging.getLogger('papyrman')
        self.logger.debug(f"ini = {vars(ini)}, db = {vars(db)}")
        self.ini = ini
        self.db = db

    #####################
    # Profile functions #
    #####################

    def create_profile(self):   # eingabe Profile + Target + auswahl der Settings
        if self.db.connection[0]:   # [Database, Server, result]
            profile = {}
            table_name = "DB_profiles"
            table = self.ini.configs[table_name]

            for key in table:
                if "_id" not in key:
                    user_input = input(key + ": ")
                    if user_input.isalnum():
                        profile[key] = user_input
                    else:
                        profile[key] = None

            if self.db.insert_entety(table_name.replace("DB_", ""), profile):
                entety = self._select_profile('profile_name', profile['profile_name'])
                profile_id = entety[0]

                while True:
                    self.create_target(profile_id)
                    if input("Add further target? y/N ").lower() != "y":
                        break
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def show_profiles(self):
        if self.db.connection[0]:   # [Database, Server, result]
            result = self.db.select_entety("profiles")
            if result:
                for entety in result.mappings():
                    print(entety)
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def show_profile(self, column, value):
        self.logger.debug(f"column = {column}, value = {value}")
        if self.db.connection[0]:   # [Database, Server, result]
            profile = self._select_profile(column, value)
            print()
            if profile:
                for key in profile.keys():
                    print(str(key) + " : " + str(profile[key]))
                self._show_targets(column, value)
            else:
                self.logger.error(f"No Profile with ID {value}")
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def update_profile(self):
        if self.db.connection[0]:   # [Database, Server, result]
            pass
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def delete_profile(self, column, value):
        self.logger.debug(f"column = {column}, value = {value}")
        if self.db.connection[0]:   # [Database, Server, result]
            targets = self.db.select_entety("targets", column, value)
            for target in targets:
                self.delete_target("target_id", target[0])
            self.db.delete_entety("profiles", column, value)
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def _select_profile(self, column, value):
        self.logger.debug(f"column = {column}, value = {value}")
        result = self.db.select_entety("profiles", column, value).fetchone()
        return result

    #####################
    #  Target functions #
    #####################

    def create_target(self, profile_id):
        self.logger.debug(f"profile_id = {profile_id}")
        if self.db.connection[0]:   # [Database, Server, result]
            if self._select_profile('profile_id', profile_id):
                target = {}
                table_name = "DB_targets"
                table = self.ini.configs[table_name]
                for key in table:
                    if key == "profile_id":
                        target[key] = profile_id
                        print(profile_id)
                    elif "_id" not in key:
                        user_input = input(key + ": ")
                        if user_input.isalnum():
                            target[key] = user_input
                        else:
                            target[key] = None
                self.db.insert_entety(table_name.replace("DB_", ""), target)
            else:
                self.logger.error(f"No Profile with ID {profile_id}")
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def _show_targets(self, column, value):
        self.logger.debug(f"column = {column}, value = {value}")
        targets = self.db.select_entety("targets", column, value)
        for target in targets.mappings():
            for key in targets.keys():
                if key != column:
                    print("\t" + str(key) + " : " + str(target[key]))
            print()

    def update_target(self):
        if self.db.connection[0]:   # [Database, Server, result]
            pass
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def delete_target(self, column, value):
        self.logger.debug(f"column = {column}, value = {value}")
        if self.db.connection[0]:   # [Database, Server, result]
            if self._select_target(column, value):
                self.db.delete_entety("targets", column, value)
            else:
                self.logger.error(f"No Target with ID {value}")
        else:
            self.logger.error(f"Database {self.db.db_name} does not exist. Use 'create-db to create your Database!")

    def _select_target(self, column, value):
        self.logger.debug(f"column = {column}, value = {value}")
        result = self.db.select_entety("targets", column, value).fetchone()
        return result

    def create_db(self):
        self.logger.info("Database will be created...")
        if self.db.connection[1]:   # [Database, Server, result]
            self.db.create_db()
        else:
            self.logger.critical(f"Connection to DB-Server == {self.db.connection[1]}. Please make sure that your Server is running")

    def connect_db(self):
        self.logger.info(f"Connection to {self.ini.configs['DB']['db_name']} is being established")
        self.db.connect_with_engine(self.ini.configs['DB']['db_name'])

    def drop_db(self):
        self.logger.debug("")
        if self.db.connection[1]:   # [Database, Server, result]
            self.db.drop_db()
        else:
            self.logger.critical(f"Connection to DB-Server == {self.db.connection[1]}. Please make sure that your Server is running")
