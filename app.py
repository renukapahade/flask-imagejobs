"""
    This module is the entry point to the flask server
"""

# import necessary libraries and functions
from flask import Flask, jsonify, request

# import database settings
from config import Config
from db_connection import SqlDbConnect

# import celery dependencies
from flask_celery import make_celery

# import custom image processing module
from image_processing import ImageProcessing


# connect to the database and send back the connection instance
def mysql_connect():
    config_obj = Config()
    sql_database_object = SqlDbConnect(config_obj, config_obj.sql_db_name)
    return sql_database_object


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
                conn.sql_db.execute(insert_query)

                # close the db connection
                conn.sql_db.invalidate()
                conn.engine.dispose()

                # run async image processing tasks
                processing.delay(job_id, request_data['visits'])

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
    except:
        response = jsonify({"error": "Something went wrong"})
        response.status_code = 400
        return response

# GET request function to get the status of a job
# on the terminal type: curl http://127.0.0.1:5000/api/status?jobid=123
# this returns the status of the job completed/ongoing etc


@app.route('/api/status', methods=['GET'], strict_slashes=False)
def get_job_status():
    job_id = request.args.get('jobid')
    if(job_id):
        try:
            conn = mysql_connect()
            select_query = "SELECT * from job where id='"+str(job_id)+"';"
            select_job_result = conn.sql_db.execute(select_query)
            status = select_job_result.first()[1]
            if status == 1:
                status_message = "completed"
            elif status == 2:
                status_message = "failed"
                select_failed_store_jobs = "SELECT store_id from store_job where job_id='" + \
                    str(job_id)+"' and status=2 group by store_id;"
                select_failed_store_jobs_result = conn.sql_db.execute(
                    select_failed_store_jobs)
                err_msg = "Image not found/processing error"
                failed_stores = [{"store_id": row.store_id, "error": err_msg}
                                 for row in select_failed_store_jobs_result]
                # status = "failed" if select_job_result
                return jsonify({
                    "status": status_message,
                    "job_id": job_id,
                    "error": failed_stores
                })
            else:
                status_message = "ongoing"

            # close the db connection
            conn.sql_db.invalidate()
            conn.engine.dispose()
            # status = "completed" if select_job_result
            return jsonify({
                "status": status_message,
                "job_id": job_id
            })
        except TypeError:
            # if jobid is not found
            response = jsonify({})
            response.status_code = 400
            return response
        except:
            response = jsonify({"error": "Something went wrong"})
            response.status_code = 400
            return response
    else:
        # if jobid is not found in the request
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
    areacode = request.args.get('area')
    store_id = request.args.get('storeid')
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')
    if(areacode):
        try:
            conn = mysql_connect()
            query = "SELECT store.id as store_id,store.areacode as area,store.name as store_name,store_perimeter.date as date,store_perimeter.perimeter as perimeter from store join store_perimeter on store.id = store_perimeter.store_id where store.areacode='" + \
                str(areacode) + "' "
            if(store_id):
                query = query + "and store.id='" + str(store_id)+"' "
            if(startdate):
                query = query + "and store_perimeter.date>='" + \
                    str(startdate)+"' "
            if(enddate):
                query = query + "and store_perimeter.date<='" + \
                    str(enddate)+"' "
            query = query + " group by store_id,date;"

            select_store_result = conn.sql_db.execute(query)
            store_details = [dict(row)
                             for row in select_store_result]

            # close the db connection
            conn.sql_db.invalidate()
            conn.engine.dispose()

            return jsonify({
                "results": store_details
            })
        except TypeError:
            # if store is not found
            response = jsonify({"error": "Store does not exist"})
            response.status_code = 400
            return response
        except:
            response = jsonify({"error": "Something went wrong"})
            response.status_code = 400
            return response
    else:
        # if areacode and storeid is not found in the request
        response = jsonify({
            "error": "Invalid request"
        })
        response.status_code = 400
        return response


# main driver function
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
