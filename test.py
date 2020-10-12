"""
Test API endpoints
"""

import io
import os
import json
import unittest
from app import *

__author__ = 'Renuka Pahade'


class TestDataObjects(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        "set up test fixtures"
        print('### Setting up flask server ###')
        self.app = app.test_client()

    @ classmethod
    def tearDownClass(self):
        "tear down test fixtures"
        print('### Tearing down the flask server ###')

    def test_01_get_server_verify(self):
        """ Test that the flask server is running and reachable"""
        r = self.app.get('http://localhost:5000/')
        self.assertEqual(r.status_code, 200)

    def test_02_post_job_data(self):
        """ Test successful job submit: POST """
        payload = json.dumps({
            "count": 2,
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/2.jpg",
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:53"
                },
                {
                    "store_id": "S01408764",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:56"
                }
            ]
        })
        r = self.app.post('http://localhost:5000/api/submit',
                          headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(int, type(r.json['job_id']))  # Should return a job id
        self.assertEqual(r.status_code, 201)  # Should return status 201

    def test_03_post_job_data(self):
        """ Test successful job submit with incorrect image link: POST """
        payload = json.dumps({
            "count": 2,
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                                "https://www.gstatic.com/webp/galleryy/2.jpg",  # incorrect link
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:53"
                },
                {
                    "store_id": "S01408764",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:56"
                }
            ]
        })
        r = self.app.post('http://localhost:5000/api/submit',
                          headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(int, type(r.json['job_id']))  # Should return a job id
        self.assertEqual(r.status_code, 201)  # Should return status 201

    def test_04_post_job_data_fail(self):
        """ Test incorrect job submit, count is not equal to visits array length: POST """
        payload = json.dumps({
            "count": 5,
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/2.jpg",
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:53"
                },
                {
                    "store_id": "S01408764",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:56"
                }
            ]
        })
        r = self.app.post('http://localhost:5000/api/submit',
                          headers={"Content-Type": "application/json"}, data=payload)
        # Should return an error message
        self.assertEqual(str, type(r.json['error']))
        self.assertEqual(r.status_code, 400)  # Should return status 201

    def test_05_post_job_data_fail(self):
        """ Test incorrect job submit fields are missing: POST """
        payload = json.dumps({
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/2.jpg",
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:53"
                },
                {
                    "store_id": "S01408764",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02 00:00:56"
                }
            ]
        })
        r = self.app.post('http://localhost:5000/api/submit',
                          headers={"Content-Type": "application/json"}, data=payload)
        # Should return an error message
        self.assertEqual(str, type(r.json['error']))
        self.assertEqual(r.status_code, 400)  # Should return status 201

    def test_06_get_job_info(self):
        """ Test the status of a successful job"""
        r = self.app.get('http://localhost:5000/api/status?jobid=1')
        self.assertEqual(str, type(r.json['status']))  # Should return a status
        self.assertEqual(r.status_code, 200)

    def test_07_get_job_info_fail(self):
        """ Test the status of a non existing job"""
        r = self.app.get('http://localhost:5000/api/status?jobid=3004')
        self.assertEqual(r.status_code, 400)

    def test_08_get_visit_info(self):
        """ Test the status of a correct visiting info request"""
        r = self.app.get(
            'http://localhost:5000/api/visits?area=700029&storeid=S00339218')
        # Should return a status
        self.assertEqual(list, type(r.json['results']))
        self.assertEqual(r.status_code, 200)
