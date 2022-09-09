from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os





def scrape_job(url, driver):
    try:
        data = {"apply link": url}
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        data["title"] = title.text
        departament_location = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='-tracking-sm "
                                                                                         "text-p-1 leading-14 "
                                                                                         "tablet:text-p-2 "
                                                                                         "tablet:leading-125 "
                                                                                         "laptop:leading-135 "
                                                                                         "desktop:text-p-3 "
                                                                                         "desktop:leading-15']")))
        data["department"] = departament_location[0].text
        data["location"] = departament_location[1].text
        description = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='description "
                                                                           "text-p-1 leading-15 laptop:text-p-2 "
                                                                           "laptop:leading-145 text-blue/70']")))
        data["description"] = description.text
        return data
    except Exception as e:
        print(e, type(e))
        return None


def main( file_name = "website_6_jobs.txt"):
    url = "https://www.papayaglobal.com/careers/"
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    position_items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='col single-position "
                                                                               "items-center py-[27px] border-b-[1px] "
                                                                               "border-b-black/15 transition-all "
                                                                               "duration-300 no-underline "
                                                                               "bg-transparent active desktop "
                                                                               "hover:shadow-"
                                                                               "[0_5px_24px_rgba(29,31,69,0.1)]']")))
    position_urls = []
    for pi in position_items:
        position_urls.append(pi.get_attribute("href"))
    f = open(file_name, "w", encoding="utf-8")

    for p in position_urls:
        data = scrape_job(p, driver)
        if data is not None:
            print(f"Title: {data['title']}")
            print(f"Apply link: {data['apply link']}")
            print(f"Location: {data['location']}")
            print(f"Department: {data['department']}")
            print(f"Description: {data['description']}")
            f.write(f"-----------------------------------------------"
                    f"---------------------------------------------------\n")
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