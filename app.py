# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, Response

# creating a Flask app
app = Flask(__name__)


# on the terminal type: curl http://127.0.0.1:5000/
# returns hello message when we use GET/POST.
@app.route('/', methods=['GET', 'POST'])
def home():
    data = "Hello from image API service"
    return jsonify({'data': data})


# POST request function to submit an image processing job
# on the terminal type: curl http://127.0.0.1:5000/api/submit
# Sample request payload:
# {
#    "count":2,
#    "visits":[
#       {
#          "store_id":"S00339218",
#          "image_url":[
#             "https://www.gstatic.com/webp/gallery/2.jpg",
#             "https://www.gstatic.com/webp/gallery/3.jpg"
#          ],
#          "visit_time": "time of store visit"
#       },
#       {
#          "store_id":"S01408764",
#          "image_url":[
#             "https://www.gstatic.com/webp/gallery/3.jpg"
#          ],
#          "visit_time": "time of store visit"
#       }
#    ]
# }
# this returns the job id of the process
@app.route('/api/submit', methods=['POST'], strict_slashes=False)
def create_job():

    return jsonify({
        "job_id": 123
    })


# GET request function to get the status of a job
# on the terminal type: curl http://127.0.0.1:5000/api/status?jobid=123
# this returns the status of the job completed/ongoing etc
@app.route('/api/status', methods=['GET'])
def get_job_status():
    job_id = request.args.get('jobid')
    if(job_id):
        return jsonify({
            "status": "completed",
            "job_id": ""
        })
    else:
        # if jobid is not in the request
        return Response(
            "{}",
            status=400,
        )


# GET request function to get the store visiting info
# on the terminal type: curl http://127.0.0.1:5000/api/visits?area=abc&storeid=S00339218&startdate=stdate&enddate=endate
# this returns the store visiting info store details, date of visit, total perimeter of the images submited
@app.route('/api/visits', methods=['GET'])
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


# driver function
if __name__ == '__main__':

    app.run(host='127.0.0.1',port=5000,debug=True)
