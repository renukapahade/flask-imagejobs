"""
This module is used to make a connection to MySQL database
"""
import json
import sys
from sqlalchemy import create_engine


class SqlDbConnect():

    def __init__(self, config_object, db_name=None):
        """
        Connect to the MySQL database
        :param config_object: config object that have database parameters
        """
        self.error = None

        # mysql server connection
        try:
            if db_name:
                engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s"
                                    % (config_object.sql_username,config_object.sql_password,config_object.sql_db_host,config_object.sql_db_port,db_name), echo=False)
            else:
                engine = create_engine("mysql+pymysql://%s:%s@%s:%s"
                                    % (config_object.sql_username,config_object.sql_password,config_object.sql_db_host,config_object.sql_db_port), echo=False)
            self.engine = engine
            self.sql_db = engine.connect()
        except Exception as e:
            print(e)
            sys.exit()
