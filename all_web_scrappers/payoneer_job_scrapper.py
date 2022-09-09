from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re

def scrape_job(url, driver):
    data = {"apply link": url}
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    title = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='job-title']")))
    data["title"] = title.text
    location = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='job-loc']")))
    data["location"] = location.text
    description = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='job-desc']")))
    data["description"] = description.text
    return data


def main(file_name="website_9_jobs.txt"):
    url = "https://www.payoneer.com/careers/"
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    driver.minimize_window()
    wait = WebDriverWait(driver, 10)
    departments = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='department-item-heading']")))
    departments = [d.text.split("\n")[0] for d in departments]
    department_jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='department-jobs']")))
    department_jobs = [dj.get_attribute("innerHTML") for dj in department_jobs]
    f = open(file_name, "w", encoding="utf-8")
    for d, dj in zip(departments, department_jobs):
        results = re.findall('data-job-url="(.*?)"', dj)
        jobs_urls = [url + r for r in results]
        for j in jobs_urls:
            data = scrape_job(j, driver)
            data["department"] = d
            print(f"Title: {data['title']}")
            print(f"Apply link: {data['apply link']}")
            print(f"Location: {data['location']}")
            print(f"Department: {data['department']}")
            print(f"Description: {data['description']}")
            f.write(
                f"--------------------------------------------------------------------------------------------------\n")
            f.write(f"Title: {data['title']}\n")
            f.write(f"Apply link: {data['apply link']}\n")
            f.write(f"Location: {data['location']}\n")
            f.write(f"Department: {data['department']}\n")
            f.write(f"{data['description']}\n")
    driver.quit()
    f.close()



if __name__ == '__main__':
    os.environ["GH_TOKEN"] = "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"
    main()