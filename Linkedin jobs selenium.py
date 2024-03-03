import pandas as pd
import re
import time
import math
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Instantiate the WebDriver (using Firefox in this example)
driver = webdriver.Firefox()

# This is the URL to test the jobs I want to scrape from
url = 'https://www.linkedin.com/jobs/search/?keywords=data%20scientist'
driver.get(url)
time.sleep(5)

driver.get('https://www.linkedin.com/login')
time.sleep(5) # waiting for the page to load

# Enter email address & password
email_input = driver.find_element(By.ID, 'username')
password_input = driver.find_element(By.ID, 'password')
email_input.send_keys("ENTER YOUR EMAIL")
password_input.send_keys("ENTER YOUR PASSWORD")

# Click the login button
password_input.send_keys(Keys.ENTER)

time.sleep(10)

driver.get("https://www.linkedin.com/jobs/search/?keywords=data%20scientist")

def scroll_to_bottom(webdriver, sleep_time=120):
    last_height = webdriver.execute_script('return document.body.scrollHeight')
    while True:
        webdriver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        new_height = webdriver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

        time.sleep(sleep_time)


soup = BeautifulSoup(driver.page_source, 'html.parser')
List_Job_IDs = []

# 1. Get number of jobs found and number of pages:
try:
    div_number_of_jobs = soup.find("div", {"class": "jobs-search-results-list__subtitle"})
    number_of_jobs = int(div_number_of_jobs.find('span').get_text().strip().split()[0])
except:
    number_of_jobs = 0

number_of_pages = math.ceil(number_of_jobs / 25)
print("number_of_jobs:", number_of_jobs)
print("number_of_pages:", number_of_pages)

def find_Job_Ids(soup):
    Job_Ids_on_the_page = []

    job_postings = soup.find_all('li', {'class': 'jobs-search-results__list-item'})
    for job_posting in job_postings:
        Job_ID = job_posting.get('data-occludable-job-id')
        Job_Ids_on_the_page.append(Job_ID)

    return Job_Ids_on_the_page

Jobs_on_1st_page = find_Job_Ids(soup)
List_Job_IDs.extend(Jobs_on_1st_page)

if number_of_pages > 1:
    for page_num in range(1, number_of_pages):
        print(f"Scraping page: {page_num}", end="...")

        url = f'https://www.linkedin.com/jobs/search/?keywords=data%20scientist&start={25 * page_num}'
        url = requests.utils.requote_uri(url)
        driver.get(url)
        scroll_to_bottom(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        Jobs_on_this_page = find_Job_Ids(soup)
        List_Job_IDs.extend(Jobs_on_this_page)

pd.DataFrame({"Job_Id": List_Job_IDs}).to_csv('Linkedin_Job_Ids.csv', index=False)
driver.quit()

# Scrape job details
job_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['style', 'script']):
        data.decompose()

    return ' '.join(soup.stripped_strings)

job = {}
list_jobs = []

for j in range(0, len(List_Job_IDs)):
    print(f"{j + 1} ... read jobId:{List_Job_IDs[j]}")

    resp = requests.get(job_url.format(List_Job_IDs[j]))
    soup = BeautifulSoup(resp.text, 'html.parser')

    job["Job_ID"] = List_Job_IDs[j]

    try:
        job["Job_txt"] = remove_tags(resp.content)
    except:
        job["Job_txt"] = None

    try:
        job["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        job["company"] = None

    try:
        job["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
    except:
        job["job-title"] = None

    try:
        job["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace(
            "Seniority level", "").strip()
    except:
        job["level"] = None

    try:
        job["location"] = soup.find("ul", {"class": "description__job-criteria-list"}).find_all("li")[1].text.replace(
            "Location", "").strip()
    except:
        job["location"] = None

    try:
        job["posted_date"] = soup.find("ul", {"class": "description__job-criteria-list"}).find_all("li")[2].text.replace(
            "Posted", "").strip()
    except:
        job["posted_date"] = None

    list_jobs.append(job.copy())

df = pd.DataFrame(list_jobs)
df.to_csv('linkedin_job_details.csv', index=False)