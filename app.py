"""
    This file is the entry point to the server
    Using flask to make an API server
"""

# import necessary libraries and functions
from flask import Flask, jsonify, request

# import database settings
from config import *
from db_connection import *
from flask_celery import *
from image_processing import *

# connect to the database and send back the connection instance


def mysql_connect():
    config_obj = Config()
    sql_database_object = SqlDbConnect(config_obj, config_obj.sql_db_name)
    return sql_database_object


# creating a Celery instance
# celery = Celery(broker='redis://localhost:6379/0')

# creating a Flask app
app = Flask(__name__)

# add celery to the application
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


# create the async image processing task with celery
@celery.task(name='image.processing')
def processing(job_id, visits):
    image_processing_obj = ImageProcessing(job_id, visits)
    image_processing_obj.process()


# on the terminal type: curl http://127.0.0.1:5000/
# returns hello message
@app.route('/', methods=['GET', 'POST'])
def home():
    data = "Hello from image API service"
    return jsonify({'data': data})


# POST request function to submit an image processing job
# on the terminal type: curl http://127.0.0.1:5000/api/submit
# this returns the job id of the process
@app.route('/api/submit', methods=['POST'], strict_slashes=False)
def create_job():

    request_data = request.json
    try:
        if request_data and request_data['count'] and request_data['visits']:
            if(request_data['count'] != len(request_data['visits'])):
                response = jsonify({
                    "error": "Invalid fields in the request"
                })
                response.status_code = 400
                return response
            else:
                # insert a new job record in database
                sqlQuery = "INSERT INTO job (status) VALUES (0);"
                conn = mysql_connect()
                job_result = conn.sql_db.execute(sqlQuery)
                job_id = job_result.lastrowid

                # insert the new store jobs record in database
                insert_query = 'INSERT IGNORE INTO retail_store.store_job (job_id,store_id,image_url,visit_time) VALUES '
                for store in request_data['visits']:
                    for image in store['image_url']:
                        insert_query = insert_query + \
                            "('"+str(job_id)+"','" + \
                            store['store_id']+"','"+image + \
                            "','"+store['visit_time']+"'),"
                # To remove , from the EOL and add ; to complete the SQL syntax
                insert_query = insert_query[:-1]+";"
                store_job_result = conn.sql_db.execute(insert_query)

                # close the db connection
                conn.sql_db.invalidate()
                conn.engine.dispose()

                # run async image processing tasks
                # async_obj = AsyncJob(job_id,request_data['visits'])
                # async_obj.process()
                async_result = processing.delay(job_id, request_data['visits'])
                # async_result.wait()

                # return the response
                response = jsonify({
                    "job_id": job_id
                })
                response.status_code = 201
                return response
    except KeyError:
        # missing values and incorrect request
        response = jsonify({
            "error": "Invalid request"
        })
        response.status_code = 400
        return response


# GET request function to get the status of a job
# on the terminal type: curl http://127.0.0.1:5000/api/status?jobid=123
# this returns the status of the job completed/ongoing etc
@app.route('/api/status', methods=['GET'], strict_slashes=False)
def get_job_status():
    job_id = request.args.get('jobid')
    if(job_id):
        return jsonify({
            "status": "completed",
            "job_id": ""
        })
    else:
        # if jobid is not in the request
        response = jsonify({
            "error": "JobID not sent in the request"
        })
        response.status_code = 400
        return response


# GET request function to get the store visiting info
# on the terminal type: curl http://127.0.0.1:5000/api/visits?area=abc&storeid=S00339218&startdate=stdate&enddate=endate
# this returns the store visiting info store details, date of visit, total perimeter of the images submited
@app.route('/api/visits', methods=['GET'], strict_slashes=False)
def get_visit_info():

    return jsonify({
        "results": [
            {
                "store_id": "S00339218",
                "area": "",
                "store_name": "",
                "data": [
                    {
                        "date": "",
                        "perimeter": ""
                    },
                    {
                        "date": "",
                        "perimeter": ""
                    }
                ]
            },
            {
                "store_id": "S01408764",
                "area": "",
                "store_name": "",
                "data": [
                    {
                        "date": "",
                        "perimeter": ""
                    },
                    {
                        "date": "",
                        "perimeter": ""
                    }
                ]
            }
        ]
    })


# main driver function
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
