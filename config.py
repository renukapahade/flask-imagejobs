"""
This module gets all the environment variables (retrieve it from the .env file in production)
"""

class Config():
    """
    This class loads the settings for the database and constants
    """
    db_host = None
    sql_db_name = None
    sql_username = None
    sql_password = None

    def __init__(self):
        # Load expected variables into different variables
        self.db_host = "localhost"
        self.sql_db_name = "retail_store"
        self.sql_username = "root"
        self.sql_password = "password"
