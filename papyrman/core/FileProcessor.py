from os import path

"""
    incoming:   - profile in event.src_path
                - target in event.src_path
                - settings (in profile verschieben)

    incoming Data bei erster aktivität einlesen

    Client erstellt Ordnerstruktur upload/inbox/<prefix>/<profile>/<target>/<file.*>

"""


class FileProcessor:        # siehe class PageProcessor in postProcessing.py
    def __init__(self, event, profiles):
        self.src_path = path.abspath(event.src_path)
        if self.src_path.find("/") == -1:
            self.src_path = self.src_path.split("\\")
        else:
            self.src_path = self.src_path.split("/")
        self.profile_id = self.src_path[-3]
        if self.profile_id not in profiles.profiles:
            print(f"profil ID {self.profile_id} is not in profiles")
            # self.profile = profiles.get_profile(self.profile_name)
        self.target_name = self.src_path[-2]
        # self.target = self.profile['targets'][self.target_name]
        # self.settings = self.profile['settings']
        print("self.profile_name = " + str(self.profile_id))
        print("self.target_name = " + str(self.target_name))
        # print("self.profile_name = " + str(self.profile_name))
        print(event)
