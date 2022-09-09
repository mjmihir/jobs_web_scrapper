from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def scrape_job(url, driver):
    data = {"apply link": url}
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    data["title"] = title.text
    sub_title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    sub_title = sub_title.text
    sub_title = sub_title.split(",")
    data["location"] = sub_title[0]
    data["department"] = sub_title[1][1:]
    description = wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
    data["description"] = description.text
    return data


def main(file_name = "website_4_jobs.txt"):
    url = "https://fundbox.com/careers/"
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    lm_wait = WebDriverWait(driver, 3)
    try:
        while True:
            load_more = lm_wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='underline text-xl']")))
            load_more.click()
    except Exception as e:
        print(e, type(e))
    wait = WebDriverWait(driver, 10)
    jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='flex-1']")))
    jobs_url = []
    for j in jobs:
        jobs_url.append(j.get_attribute("href"))
    f = open(file_name, "w", encoding="utf-8")
    for j in jobs_url:
        data = scrape_job(j, driver)
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