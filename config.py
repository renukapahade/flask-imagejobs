"""
This module gets all the environment variables (retrieve it from the .env file if running in production)
"""


class Config():
    """
    This class loads the settings for the database and constants
    """
    sql_db_host = None
    sql_db_name = None
    sql_username = None
    sql_password = None
    sql_db_port = None

    def __init__(self):
        # Load expected variables into different variables
        self.sql_db_host = "localhost"
        self.sql_db_name = "retail_store"
        self.sql_username = "root"
        self.sql_password = "password"
        self.sql_db_port = "3306"
