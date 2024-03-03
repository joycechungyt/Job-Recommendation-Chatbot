from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException

# Instantiate the WebDriver (using Firefox in this example)
driver = webdriver.Firefox()

# Maximize the browser window (optional)
driver.maximize_window()

# Set an implicit wait (optional)
driver.implicitly_wait(5)  # Reduced implicit wait to 5 seconds

# Load the Indeed job search page
driver.get('https://hk.indeed.com/')

# Use WebDriver to interact with the page
input_what = driver.find_element(By.CSS_SELECTOR, '#text-input-what')
input_what.send_keys('Data Scientist')

# Simulate pressing the Enter key
input_what.send_keys(Keys.ENTER)

# Use JavaScript Executor to wait until the page is fully loaded
wait = WebDriverWait(driver, 10)  # Reduced WebDriverWait to 10 seconds
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

# Wait for the cookie privacy notice banner to appear
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gnav-CookiePrivacyNoticeBanner")))

# Scroll the page to bring the "OK" button into view
ok_button = driver.find_element(By.CLASS_NAME, "gnav-CookiePrivacyNoticeButton")
driver.execute_script("arguments[0].scrollIntoView(true);", ok_button)

# Find and click the "OK" button to remove the cookie privacy notice banner
driver.execute_script("arguments[0].click();", ok_button)

# Perform the job scraping logic
job_details = []

while True:
    # Wait for the page to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".resultContent")))

    # Close the job alerts banner if present
    try:
        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-yi9ndv.e8ju0x51')))
        # Perform the mouse hover action on the close button
        actions = ActionChains(driver)
        actions.move_to_element(close_button).perform()
        # Click the close button
        close_button.click()
    except:
        pass

    # Extract the page source and create a BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.select(".resultContent")

    if not job_listings:
        break  # Exit the loop if no job listings found

    for job in job_listings:
        try:
            title_element = job.select_one("h2.jobTitle span[title]")
            duration_element = job.select_one('div.jobMetaDataGroup [data-testid="attribute_snippet_testid"]')
            company_element = job.select_one('div.company_location [data-testid="company-name"]')
            location_element = job.select_one('div.company_location [data-testid="text-location"]')

            if title_element and duration_element and company_element and location_element:
                title = title_element.text
                duration = duration_element.text
                company = company_element.text
                location = location_element.text

                # Find and click the job title button
                job_title_button = job.select_one('.jcs-JobTitle.css-jspxzf.eu4oa1w0')
                driver.execute_script("arguments[0].click();", job_title_button)

                # Wait for the full job description to load
                wait.until(EC.presence_of_element_located((By.ID, 'jobDescriptionText')))

                # Switch to the inline frame
                inline_frame_element = driver.find_element(By.CSS_SELECTOR, '.jobsearch-EmbeddedBody.css-1u1f945.eu4oa1w0')
                driver.switch_to.frame(inline_frame_element)

                # Extract the full job description
                job_description_element = driver.find_element(By.ID, 'jobDescriptionText')
                job_description_text = str(job_description_element)  # Convert to string

                # Switch back to the main frame
                driver.switch_to.default_content()

                # # Go back to the previous page with job listings
                # driver.execute_script("window.history.go(-1)")

                job_details.append({'Title': title, 'Duration': duration, 'Company': company, 'Location': location, 'Description': job_description_text})
            else:
                print("Some job details are missing. Skipping this job listing.")
        except Exception as e:
            print(f"Error occurred while scraping job listings: {e}")

# Close the WebDriver
driver.quit()

# Create a DataFrame from the scraped job details
df = pd.DataFrame(job_details)

# Print the DataFrame
print(df)