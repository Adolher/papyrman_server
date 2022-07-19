# ToDo: Better User-input check
# ToDo: if show_profiles has no results -> say that it has no results

import logging, sys


class CLUI:
    def __init__(self, ini, db):
        self.logger = logging.getLogger('papyrman')
        self.logger.info(f"{sys.argv[1:]}")
        self.ini = ini
        self.db = db
        # self.profile_menu()

        # menu als argparse
        # -> papyrman edit -profile -> show_profiles() -> enter ID -> edit_profile()
        # -> papyrman create -> create_profile
        # -> papyrman delete -> show_profiles -> enter ID -> delete:profile()

    def profile_menu(self):
        self.logger.info("")
        menu = "1 - Create Profile\n" \
               "2 - Show Profiles\n" \
               "3 - Show Profile\n" \
               "4 - Delete Profile\n" \
               "5 - Add Target to\n" \
               "6 - Edit Profile\n" \
               "7 - Delete Target\n" \
               "8 - Create DB\n" \
               "9 - Connect to DB\n" \
               "0 - Drop DB\n" \
               "10- Edit Target"
        user_input = input(menu)

        if user_input == "1":
            self.create_profile()
            self.profile_menu()
        elif user_input == "2":
            self.show_profiles()
            self.profile_menu()
        elif user_input == "3":
            self.show_profile('profile_id', input("Enter Profile ID: "))
            self.profile_menu()
        elif user_input == "4":
            self.delete_profile('profile_id', int(input("Enter Profil_ID: ")))
            self.profile_menu()
        elif user_input == "5":
            self.create_target(int(input("Enter Profile_ID: ")))
            self.profile_menu()
        elif user_input == "6":
            self.update_profile()
            self.profile_menu()
        elif user_input == "7":
            self.delete_target('target_ID', int(input("Enter Target_ID: ")))
            self.profile_menu()
        elif user_input == "8":
            self.create_db()
            self.profile_menu()
        elif user_input == "9":
            self.connect_db()
            self.profile_menu()
        elif user_input == "0":
            self.drop_db()
            self.profile_menu()
        else:
            self.wrong_choice()

    #####################
    # Profile functions #
    #####################

    def create_profile(self):   # eingabe Profile + Target + auswahl der Settings
        self.logger.info(f"{sys.argv[1:]}")
        if self.db.connection[0]:
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
            self.logger.info("")

    def show_profiles(self):
        self.logger.info(f"{sys.argv[1:]}")
        if self.db.connection[0]:
            result = self.db.select_entety("profiles")
            if result:
                for entety in result.mappings():
                    print(entety)
        else:
            self.logger.info("")

    def show_profile(self, column, value):
        self.logger.info("")
        if self.db.connection[0]:
            profile = self._select_profile(column, value)
            print()
            if profile:
                for key in profile.keys():
                    print(str(key) + " : " + str(profile[key]))
                self._show_targets(column, value)
            else:
                print(f"No Profile with ID {value}")
        else:
            self.logger.info("")

    def update_profile(self):
        self.logger.info("")
        if self.db.connection[0]:
            pass
        else:
            self.logger.info("")

    def delete_profile(self, column, value):
        self.logger.info("")
        if self.db.connection[0]:
            targets = self.db.select_entety("targets", column, value)
            for target in targets:
                self.delete_target("target_id", target[0])
            self.db.delete_entety("profiles", column, value)
        else:
            self.logger.info("")

    def _select_profile(self, column, value):
        self.logger.info("")
        result = self.db.select_entety("profiles", column, value).fetchone()
        return result

    #####################
    #  Target functions #
    #####################

    def create_target(self, profile_id):
        self.logger.info("")
        if self.db.connection[0]:
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
                print(f"No Profile with ID {profile_id}")
        else:
            self.logger.info("")

    def _show_targets(self, column, value):
        self.logger.info("")
        targets = self.db.select_entety("targets", column, value)
        for target in targets.mappings():
            for key in targets.keys():
                if key != column:
                    print("\t" + str(key) + " : " + str(target[key]))
            print()

    def update_target(self):
        self.logger.info("")
        if self.db.connection[0]:
            pass
        else:
            self.logger.info("")

    def delete_target(self, column, value):
        self.logger.info("")
        if self.db.connection[0]:
            if self._select_target(column, value):
                self.db.delete_entety("targets", column, value)
            else:
                print(f"No Target with ID {value}")
        else:
            self.logger.info("")

    def _select_target(self, column, value):
        self.logger.info("")
        result = self.db.select_entety("targets", column, value).fetchone()
        return result

    def create_db(self):
        self.logger.info("")
        if self.db.connection[1]:
            self.db.create_db()
        else:
            self.logger.info("")

    def connect_db(self):
        self.logger.info("")
        self.db.connect_with_engine(self.ini.configs['DB']['db_name'])

    def drop_db(self):
        self.logger.info("")
        if self.db.connection[1]:
            self.db.drop_db()
        else:
            self.logger.info("")

    def wrong_choice(self):
        self.logger.info("")
        print("Wrong")
        self.profile_menu()
