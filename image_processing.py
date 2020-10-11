"""
This module run the image processing job asynchronously
"""
# import necessary libraries and functions
import time
import urllib.request
import os
from PIL import Image

# import database settings
from config import *
from db_connection import *


class ImageProcessing():
    """
    This class loads the settings for the database and constants
    """

    def __init__(self, jobid, visits):
        # Load expected variables into different variables
        self.job_id = jobid
        self.visits = visits

    def process(self):
        # connect to database
        config_obj = Config()
        sql_database_object = SqlDbConnect(config_obj, config_obj.sql_db_name)

        # insert the new store jobs record in database
        for store in self.visits:
            storeProcessFailed = False
            total_store_perimeter = 0
            filedir = 'downloads/' + \
                str(self.job_id) + '/' + \
                store['store_id'] + '/' + \
                store['visit_time']
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            for image_url in store['image_url']:
                try:
                    urllib.request.urlretrieve(
                        image_url, filedir + '/'+image_url.split("/")[-1])
                    current_image = Image.open(
                        filedir + '/'+image_url.split("/")[-1])
                    width, height = current_image.size
                    total_store_perimeter = total_store_perimeter + \
                        2*(width + height)
                except urllib.error.URLError:
                    storeProcessFailed = True
                    update_query = "UPDATE retail_store.store_job SET status=2 where job_id='" + \
                        str(self.job_id)+"' and store_id='" + \
                        store['store_id']+"';"
                    sql_database_object.sql_db.execute(update_query)
                    print(
                        "Image exception: stop the processing for current store and continue with the next store")
                    break
            if not storeProcessFailed:
                print("Store:"+store['store_id'] +
                      " Perimeter:"+str(total_store_perimeter))
                update_store_job_query = "UPDATE retail_store.store_job SET status=1 where job_id='" + \
                    str(self.job_id)+"' and store_id='"+store['store_id']+"';"
                sql_database_object.sql_db.execute(update_store_job_query)

                insert_store_perimeter_query = "INSERT into retail_store.store_perimeter (store_id,perimeter,date) values ('" + \
                    store['store_id'] + "' , '" + \
                    str(total_store_perimeter) + "' , '" + \
                    store['visit_time'] + "' );"
                sql_database_object.sql_db.execute(
                    insert_store_perimeter_query)
        # update job table set status=1 completed
        update_job_query = "UPDATE retail_store.job SET status=1 where id='" + \
            str(self.job_id)+"';"
        sql_database_object.sql_db.execute(update_job_query)

        # close the db connection
        sql_database_object.sql_db.invalidate()
        sql_database_object.engine.dispose()
