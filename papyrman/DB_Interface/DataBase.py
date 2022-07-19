from sqlalchemy.exc import OperationalError, IntegrityError, ProgrammingError

import logging
import re
import sqlalchemy
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, Interval, Numeric, PickleType, SmallInteger, String, Text, Time, Unicode, UnicodeText
from sqlalchemy import ForeignKey


class DataBase:
    def __init__(self, ini):
        self.logger = logging.getLogger('papyrman')
        self.logger.info("")
        self.ini = ini
        self.dialect = self.ini.configs['DB']['dialect']
        self.db_user = self.ini.configs['DB']['db_user']
        self.db_password = self.ini.configs['DB']['db_password']
        self.db_host = self.ini.configs['DB']['db_host']
        self.db_port = self.ini.configs['DB']['db_port']
        self.db_name = self.ini.configs['DB']['db_name']

        self.varchar_length = int(self.ini.configs['DB_defaults']['varchar_length'])

        self.connection = None
        self.engine = None
        self.meta = None

        self.connect_with_engine(self.db_name)
        self.logger.info("")

    #####################
    #  Data Definition  #
    #####################

    def insert_entety(self, table, *values):
        self.logger.info("")
        table_obj = self.get_table_obj(table)
        if table_obj is not None:
            stmt = table_obj.insert().values(values)
        else:
            stmt = None
        return self.execute_statement(stmt)

    def select_entety(self, table, column=None, value=None):    # SELECT * FROM table WHERE column = value
        self.logger.info("")
        table_obj = self.get_table_obj(table)
        if column is not None:
            column_obj = sqlalchemy.Column(column, self.meta)
            stmt = sqlalchemy.select(table_obj).where(column_obj == value)
        else:
            stmt = sqlalchemy.select(table_obj)
        return self.execute_statement(stmt)

    # ToDo: update_entety()
    def update_entety(self):
        self.logger.info("")
        pass

    def delete_entety(self, table, column, value):
        self.logger.info("")
        table_obj = self.get_table_obj(table)
        column_obj = sqlalchemy.Column(column, self.meta)
        stmt = sqlalchemy.delete(table_obj).where(column_obj == value)
        self.execute_statement(stmt)

    def get_table_obj(self, table_name):
        self.logger.info("")
        if table_name.startswith("DB_"):
            table_name = table_name.replace("DB_", "")
        try:
            table_obj = sqlalchemy.Table(table_name, self.meta, autoload_with=self.engine)
        except OperationalError as e:
            self.logger.critical(f"{e.orig}")
            table_obj = None
        return table_obj

    def execute_statement(self, statement):
        self.logger.info("")
        try:
            result = self.connection[2].execute(statement)
            return result
        except OperationalError as e:
            self.logger.critical(f"{e.orig}")
            return None
        except ProgrammingError as e:
            self.logger.critical(f"{e.orig}")
            return None
        except AttributeError as e:
            self.logger.critical(f"{e.orig}")
            return None

    #####################
    # Schema Definition #
    #####################

    def create_db(self):
        self.logger.info("")
        self.connect_with_engine()
        try:
            self.engine.execute("CREATE DATABASE " + self.db_name)
            self.engine.execute("USE " + self.db_name)
            self.connect_with_engine(self.db_name)

            for table in self.ini.configs:
                if "DB_" in table and "DB_defaults" not in table:
                    self.create_table(table)
        except ProgrammingError as e:
            if e.orig.args[0] == 1007:
                self.logger.critical(f"{e.orig}")
        except OperationalError as e:
            self.logger.critical(f"{e.orig}")

    def drop_db(self):
        self.logger.info("")
        self.connect_with_engine()
        if self.connection[0] and self.connection[1]:
            try:
                self.engine.execute("DROP DATABASE " + self.db_name)
            except OperationalError as e:
                self.logger.critical(f"{e.orig}")
            except ProgrammingError as e:
                self.logger.critical(f"{e.orig}")
        else:
            print(self.connection[2])

    def create_table(self, table_name):
        self.logger.info("")
        raw_table_name = table_name.replace("DB_", "")
        table = sqlalchemy.Table(raw_table_name, self.meta)
        for c in self.ini.configs[table_name]:
            foreign_key = None
            pk = False
            unique = False
            nullable = True
            arg_list = self.ini.configs[table_name][c].split(", ")

            value_type = str(arg_list[0])
            if "integer" in value_type.lower():
                if "big" in value_type.lower():
                    value_type = BigInteger
                elif "small" in value_type.lower():
                    value_type = SmallInteger
                else:
                    value_type = Integer
            elif "string" in value_type.lower():
                if value_type.isalpha():
                    varchar_length = self.varchar_length
                else:
                    varchar_length = int(re.split('\(|\)', value_type)[-2])
                value_type = String(varchar_length)
            elif "boolean" in value_type.lower():
                value_type = Boolean
            elif "date" in value_type.lower() or "time" in value_type.lower():
                if "date" in value_type.lower():
                    value_type = Date
                elif "datetime" in value_type.lower():
                    value_type = DateTime
                else:
                    value_type = Time
            elif "float" in value_type.lower():
                value_type = Float
            elif "interval" in value_type.lower():
                value_type = Interval
            elif "numeric" in value_type.lower():
                value_type = Numeric
            elif "pickletype" in value_type.lower():
                value_type = PickleType
            elif "text" in value_type.lower():
                value_type = Text
            elif "unicode" in value_type.lower():
                if "text" in value_type.lower():
                    value_type = UnicodeText
                else:
                    if value_type.isalpha():
                        varchar_length = 50
                    else:
                        varchar_length = int(re.split('\(|\)', value_type)[-2])
                    value_type = Unicode(varchar_length)

            arg_list = arg_list[1:]
            for arg in arg_list:
                if "primary" in arg.lower():
                    pk = True
                    nullable = False
                if "foreign" in arg.lower():
                    fk_to = re.split('"', arg)[-2].lower()
                    fk_to = fk_to.replace("db_", "")
                    foreign_key = ForeignKey(fk_to)
                if "unique" in arg.lower():
                    unique = True
                if "nullable" in arg.lower():
                    nullable = False
            args = (foreign_key, )
            column = sqlalchemy.Column(c, type_=value_type, primary_key=pk, unique=unique, nullable=nullable, *args)
            table.append_column(column)
        try:
            table.create(bind=self.engine, checkfirst=True)
        except OperationalError as e:
            self.logger.critical(f"{e.orig}")

    def drop_table(self, table):
        self.logger.info("")
        table_obj = self.get_table_obj(table)
        try:
            table_obj.drop(bind=self.engine)
        except IntegrityError as e:
            self.logger.critical(f"{e.orig}")
        except OperationalError as e:
            self.logger.critical(f"{e.orig}")

    #################
    # DB Connection #
    #################

    def connect_with_engine(self, db_name=None):
        self.logger.info("")
        self.engine = self.create_engine(db_name)
        self.meta = sqlalchemy.MetaData(self.engine)
        self.connection = self.connect_db()
        if self.connection[0] and db_name:
            try:
                self.meta.reflect(bind=self.engine)
            except OperationalError as e:
                self.logger.critical(f"{e.orig}")

    def create_engine(self, db_name=None):
        self.logger.info("")
        conn = self.dialect + '://' + self.db_user + ':' + self.db_password + '@' + self.db_host + ':' + self.db_port
        if db_name:
            conn += '/' + db_name
        return sqlalchemy.create_engine(conn)

    def connect_db(self):
        self.logger.info("")
        # [Database, Server, result]
        try:
            connection = [True, True, self.engine.connect()]
        except OperationalError as e:
            if e.orig.args[0] == 1049:  # (1049, "Unknown database 'papyrman_profiles'")
                self.logger.critical(f"{e.orig}")
                connection = [False, True, e.orig]
            elif e.orig.args[0] == 2002:  # (2002, "Can't connect to server on 'localhost' (10061)")
                self.logger.critical(f"{e.orig}")
                connection = [False, False, e.orig]  # Maybe create a Backup (sqlight)
            else:
                self.logger.critical(f"{e.orig}")
                connection = [False, False, e.orig]
        return connection
