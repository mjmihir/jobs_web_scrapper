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
    title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    data["title"] = title.text
    department_location = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='career__location']")))
    department_location = department_location.text.split(" | ")
    data["department"] = department_location[0]
    data["location"] = department_location[1]
    description = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='career__details']")))
    data["description"] = description.text
    return data


def main(file_name = "website_8_jobs.txt"):
    url = "https://panorays.com/careers/"
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    position_items = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
    position_urls = []
    for pi in position_items:
        href = pi.get_attribute("href")
        if re.match(".*/careers/[a-zA-Z0-9].*", href):
            position_urls.append(href)
    print(position_urls)
    f = open(file_name, "w", encoding="utf-8")

    for p in position_urls:
        data = scrape_job(p, driver)
        print(f"Title: {data['title']}")
        print(f"Apply link: {data['apply link']}")
        print(f"Location: {data['location']}")
        print(f"Department: {data['department']}")
        print(f"Description: {data['description']}")
        f.write(f"--------------------------------------------------------------------------------------------------\n")
        f.write(f"Title: {data['title']}\n")
        f.write(f"Apply link: {data['apply link']}\n")
        f.write(f"Location: {data['location']}\n")
        f.write(f"Department: {data['department']}\n")
        f.write(f"{data['description']}\n")
    f.close()
    driver.quit()
if __name__ == '__main__':
    os.environ["GH_TOKEN"] = "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"
    main()