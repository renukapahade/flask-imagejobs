"""
This module run the image processing job asynchronously
"""
import time


class ImageProcessing():
    """
    This class loads the settings for the database and constants
    """

    def __init__(self, jobid, visits):
        # Load expected variables into different variables
        self.job_id = jobid
        self.visits = visits

    def process(self):
        print(f"Started:{str(self.job_id)} {time.strftime('%X')}")
        time.sleep(3)
        print(f"Ended:{str(self.job_id)} {time.strftime('%X')}")
