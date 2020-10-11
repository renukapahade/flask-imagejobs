"""
This module is used to make a connection to MySQL database
"""
import json
import sys
from sqlalchemy import create_engine


class SqlDbConnect():

    def __init__(self, config_object):
        """
        Connect to the MySQL database
        :param config_object: config object that have database parameters
        """
        self.error = None
        try:
            # mysql server connection
            engine = create_engine("mysql+pymysql://%s:%s@%s:3306"
                                   % (config_object.sql_username,config_object.sql_password,config_object.db_host), echo=False)
            self.sql_db = engine.connect()
        except Exception as e:
            print(e)
            sys.exit()
