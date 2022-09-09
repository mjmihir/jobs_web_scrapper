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
    title = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='position-headline']")))
    data["title"] = title.text
    department = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='department-tag grey-text']")))
    data["department"] = department.text
    location = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='location-scope']")))
    data["location"] = location.text.split("|")[1]
    description = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='position-details']")))
    data["description"] = description.text
    return data


def main(file_name = "website_5_jobs.txt"):
    url = "https://www.unipaas.com/careers"
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    position_items = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                                     "//a[@class="
                                                                     "'position-card-link-block w-inline-block']")))
    position_urls = []
    for p in position_items:
        position_urls.append(p.get_attribute("href"))
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
