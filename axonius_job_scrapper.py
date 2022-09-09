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
    iframes = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//iframe")))
    iframe = None
    for frame in iframes:
        if frame.get_attribute("id") == "grnhse_iframe":
            iframe = frame
            break
    if iframe is not None:
        driver.switch_to.frame(iframe)
    title = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='app-title']")))
    data["title"] = title.text
    location = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='location']")))
    data["location"] = location.text
    description = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='content']")))
    data["description"] = description.text
    data['department'] = "Not known"
    return data


def main(file_name="website_7_jobs.txt"):
    url = "https://www.axonius.com/company/careers/open-jobs"
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe")))
    driver.switch_to.frame(iframe)
    position_items = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
    position_urls = []
    for pi in position_items:
        position_urls.append(pi.get_attribute("href"))
    f = open(file_name, "w", encoding="utf-8")
    for i in range(0, len(position_urls)):
        data = scrape_job(position_urls[i], driver)
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