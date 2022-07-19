

"""
{
   "anonymous":{
        "name":"anonymous",
        "description":"scans to /data/t_test_public_scans",
        "raw_path":null,
        "targets":{
            "test":{
                "name":"apocalyptica",
                "description":"/nobackup/apocalyptica2/scans-test",
                "type":"filesystem",
                "target":"/nobackup/apocalyptica2/scans-test"
            },
        },
        "settings":[
            "source",
            "format",
            "resolution",
            "mode",
            "rotate",
            "combine",
            "ocr",
            "empty_page"
        ],
    },
}
"""


class Profiles:
    def __init__(self, ini, db):
        self.ini = ini
        self.db = db
        self.profiles = {}

    def get_profile(self, db, profile_name):
        # Zeitstempel der letzten Nutzung hinzufügen um Daten nach bestimmter Zeit aus Dict zu entfernen

        if profile_name not in self.profiles.keys():
            self.profiles[profile_name] = db.read()
            # lese Profildaten aus Datenbank
            # profiles['profile_name']['time_stamp'] = timestamp
            # return profile
            pass
        else:
            # profiles['profile_name']['time_stamp'] = timestamp
            return self.profiles[profile_name]
