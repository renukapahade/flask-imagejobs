# Project description

A service implemented in Flask framework to process thousands of images collected from different stores.

The service is implemented using the Flask framework, the REST API server is built using Flask and MySQL is used for storing the data.


## How it works

```
1. The Create Job Info API receives the jobs with image urls and store id. (There can be multiple jobs with thousands of images each at a given time, a job can take few minutes to an hour to complete.)
2. To process a job, the service downloads the images and calculates the perimeter 2*[Height+Width]of each image. After calculating the perimeter of image -> random sleep time of 0.1 to 0.4 secs will be there (this is to imitate GPU processing). After this the results are stored at the image level.
3. Once the job is created, it's status can be checked by Get Job Info API.
4. Show Visit Info is used by the dashboard to access the insights using relevant filters.
```


## Installation

Go to project directory:
```
$ cd flask-imagejobs
```

Create a virtual environment:
```
$ virtualenv flask-imagejobs
$ source flask-imagejobs/bin/activate
```

Now install the required modules:
```
$ pip3 install -r requirements.txt
```

## Database setup

Setup MySQL on the system.
To play with the app right away, you can use a local database. Edit config.py by commenting out the AWS URL and uncomment this line:
```
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
```
Next run:
```
$ python3 db_create.py
```

## Launch app server

Once the databse tables are created. You can now launch the app:

```
$ python3 application.py
```


## Run tests

```
#Run the test command
```

## By default

```
server   :     http://localhost:5000
database :     http://localhost:3306
```

## File structure

```
app.py               - Launch flask app 
requirements.txt     - Install the required modules to run the app
```

## API endpoints

```

POST  /api/submit/                             - Create a job to process the images collected from stores.
GET   /api/status?jobid=123                    - Get Job Info
GET   /api/visits?area=abc&storeid=S00339218   - Get the engagement rate (average time in seconds) by session
      &startdate=stdate&enddate=endate        

```


