import requests
import time
import random
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager


def main(file_name="website_1_all_jobs.txt"):
    request_url = "https://boards-api.greenhouse.io/v1/boards/sentinellabs/jobs/?content=true"
    #os.environ["GH_TOKEN"] = "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"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    }

    s = requests.session()


    r = s.get(request_url, headers=header)

    r_json = r.json()
    # print("------------------------------------------")
    jobs_json = r_json["jobs"]
    # print(jobs_json)

    PATH = GeckoDriverManager().install()

    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=PATH)

    numbers = [9, 4, 7, 3, 4, 6]

    f = open(file_name, "w", encoding="utf-8")

    for job in jobs_json:
        job_title = job["title"]
        job_absolute_url = job["absolute_url"]
        job_location = job["location"]["name"]
        job_department = job["departments"][0]["name"]

        print(
            "--------------------------------------------------------------------------------"
        )
        print("Title: " + job_title)
        print("Apply link: " + job_absolute_url)
        print("Location: " + job_location)
        print("Department: " + job_department)

        print(r_json["jobs"][0]["metadata"][0]["value"])
        # print(r_json["jobs"][0]["content"])
        # paragraph = r_json["jobs"][0]["content"]

        # soup = BeautifulSoup(paragraph, "html.parser")

        driver.get(job_absolute_url)

        time.sleep(5)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "job_details",
                )
            )
        )

        # element.click()

        element_html = element.get_attribute("innerHTML")
        element_html_splitted = element_html.split("</div></div>")[1]
        soup = BeautifulSoup(element_html_splitted, "html.parser")
        # print(soup)
        # print("---------------------------------")
        print("Description: " + soup.text)
        # print("---------------------------------")
        time.sleep(random.choice(numbers))
        f.write(
            f"--------------------------------------------------------------------------------------------------\n"
        )
        f.write(f"Title: {job_title}\n")
        f.write(f"Apply link: {job_absolute_url}\n")
        f.write(f"Location: {job_location}\n")
        f.write(f"Department: {job_department}\n")
        f.write(f"Description:\n  {soup.text}\n")
    f.close()
    driver.quit()

if __name__ == '__main__':
    os.environ["GH_TOKEN"] = "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"
    main()