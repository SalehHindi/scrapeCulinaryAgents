import requests
#import csv_writer
import pprint
import time
from bs4 import BeautifulSoup

formatted_data = {}
great_fit_count = 0
explicit_retirement_count = 0
total_count = 0
# open the file
with open('restaurant_jobs_ny_1.txt', 'r') as f:
    # read each line
    for line in f:
        time.sleep(2)
        total_count += 1
        # fetch the HTML
        response = requests.get(line)
        # parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # do something with the parsed HTML
        try: 
            business_name = soup.find(class_="business-name").text
        except:
            business_name = ""

        try:
            role_name = soup.find('h1').text
        except:
            role_name = ""

        try:
            job_compensation1 = soup.find(class_="job-compensation").text
        except:
            job_compensation1 = ""


        #location
        try:
            job_details = soup.find(id='job-details').text
        except:
            job_details = ""

        try:
            job_requirements = soup.find(id='requirement').text
        except:
            job_requirements = ""

        try:
            h5 = soup.find('h5', text='Compensation Details')
            parent = h5.parent
            comp_details = parent.text
        except:
            comp_details = ""        

        try:
            required_skills = soup.find('h5', text='Required Skills').text
        except:
            required_skills = ""
        
        great_fit = "enefits" in comp_details and "401" not in comp_details and "etirement" not in comp_details
        explicit_retirement = "enefits" in comp_details and ("401" in comp_details or "etirement" in comp_details)

        if explicit_retirement:
            explicit_retirement_count += 1

        data = {
          "business_name": business_name,
          #"location": location,
          "role_name": role_name,
          "job_compensation1": job_compensation1,
          "job_details": job_details,
          "job_requirements": job_requirements,
          "comp_details": comp_details,
          "required_skills": required_skills,
          "great_fit": great_fit,
        }

        if great_fit:
            great_fit_count += 1
            print(f"great_fit_count: {great_fit_count}")
            print(f"explicit_retirement_count: {explicit_retirement_count}")
            print(f"total_count: {total_count}")
            print("---------")
            pprint.pprint(data)
