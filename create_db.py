import csv

# import database settings
from config import *
from db_connection import *

"""Create database retail_store if not exists"""
def create_db():
    try:
        query = "CREATE DATABASE IF NOT EXISTS retail_store;"
        sql_database_object.sql_db.execute(query)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
        pass

"""Create table store if not exists"""
def create_store_db_table():
    try:
        query = """CREATE TABLE retail_store.store (
                id VARCHAR(200) NOT NULL PRIMARY KEY,
                areacode VARCHAR(200) NOT NULL,
                name VARCHAR(500) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );"""
        sql_database_object.sql_db.execute(query)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
        pass

"""Insert values into table store if not exists"""
def insert_data():
    try:
        openFile = open('StoreMasterAssignment.csv', 'r')
        csvFile = csv.reader(openFile)
        header = next(csvFile)
        headers = map((lambda x: '`'+x+'`'), header)
        insert_query = 'INSERT IGNORE INTO retail_store.store (areacode,name,id) VALUES '
        for row in csvFile:
            values = map((lambda x: '"'+x+'"'), row)
            insert_query = insert_query +"("+ ", ".join(values) +"),"
        openFile.close()
        insert_query = insert_query[:-1]+";"   # To remove , from the EOL and add ; to complete the SQL syntax
        sql_database_object.sql_db.execute(insert_query)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        pass

"""Create table job if not exists"""
def create_job_db_table():
    try:
        query = """CREATE TABLE retail_store.job (
                id INT NOT NULL AUTO_INCREMENT,
                status TINYINT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                );"""
        sql_database_object.sql_db.execute(query)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
        pass


"""Create table store_job if not exists"""
def create_store_job_db_table():
    try:
        query = """CREATE TABLE retail_store.store_job (
                id INT NOT NULL AUTO_INCREMENT,
                job_id INT NOT NULL,
                store_id VARCHAR(200) NOT NULL,
                image_url VARCHAR(200) NOT NULL,
                visit_time DATETIME NOT NULL,
                status TINYINT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                );"""
        sql_database_object.sql_db.execute(query)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
        pass

"""Create table store_perimeter if not exists"""
def create_store_perimeter_db_table():
    try:
        query = """CREATE TABLE retail_store.store_perimeter (
                id INT NOT NULL AUTO_INCREMENT,
                store_id VARCHAR(200) NOT NULL,
                perimeter INT NULL,
                date DATETIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                );"""
        sql_database_object.sql_db.execute(query)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
        pass


# create database and insert values
if __name__ == '__main__':

    config_obj = Config()
    sql_database_object = SqlDbConnect(config_obj)

    create_db()
    create_store_db_table()
    create_job_db_table()
    create_store_job_db_table()
    create_store_perimeter_db_table()
    insert_data()


