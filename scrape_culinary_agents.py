# var nodes = document.querySelectorAll(".panel-body.padding-h-15.padding-v-15.ca-single-job-card")
# var job_links = Array.from(nodes).map((x) => { return x.href})
# console.log(job_links.join("\n"))
# TODO: Make the above part of the script, so I only need to input a search URL and it'll hit "See more" for me

import requests
import csv
import pprint
import time
from bs4 import BeautifulSoup

formatted_data = {}
great_fit_count = 0
explicit_retirement_count = 0
total_count = 0
# open the file

headers = ["listing_url", "business_name", "location", "role_name", "job_compensation1", "job_details", "job_requirements", "comp_details", "required_skills", "great_fit_benefits_no_retirement", "bad_fit_has_retirement"]
# culinary_agents_listings_file = 'restaurant_jobs_ny_1'
# culinary_agents_listings_file = 'restaurant_jobs_ny_2'
# culinary_agents_listings_file = 'philadelphia_scrape_1'
# culinary_agents_listings_file = 'la_scrape_1'
# culinary_agents_listings_file = 'bay_area_scrape_1'
culinary_agents_listings_file = 'chicago_scrape_1'

with open(f"{culinary_agents_listings_file}_output.csv", 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(headers)

    with open(f"{culinary_agents_listings_file}.csv", 'r') as f:
        # read each line
        for line in f:
            time.sleep(2)
            row_data = []
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

            # TODO: add location
            try:
                location = ""
            except:
                location = ""

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
            
            great_fit_benefits_no_retirement = "enefits" in comp_details and "401" not in comp_details and "etirement" not in comp_details
            bad_fit_has_retirement = "enefits" in comp_details and ("401" in comp_details or "etirement" in comp_details)

            if bad_fit_has_retirement:
                explicit_retirement_count += 1

            data = {
                "listing_url": line,
                "business_name": business_name,
                "location": location,
                "role_name": role_name,
                "job_compensation1": job_compensation1,
                "job_details": job_details,
                "job_requirements": job_requirements,
                "comp_details": comp_details,
                "required_skills": required_skills,
                "great_fit_benefits_no_retirement": great_fit_benefits_no_retirement,
                "bad_fit_has_retirement": bad_fit_has_retirement,
            }
            for header in headers:
                row_data.append(data[header])
            csv_writer.writerow(row_data)

            if great_fit_benefits_no_retirement:
                great_fit_count += 1
                print(f"great_fit_count: {great_fit_count}")
                print(f"explicit_retirement_count: {explicit_retirement_count}")
                print(f"total_count: {total_count}")
                print("---------")
                # pprint.pprint(data)
