import requests
import time

from bs4 import BeautifulSoup


# request_url_all_jobs = "https://info.varonis.com/careers?p=search&j=oG0sifwa&j=osf0efwF&j=o8Lmifwh&j=oPhqifwy&j=oLwuifwN&j=o7cEifwZ&j=ofWgjfwu&j=oTUcjfw2&j=okx1gfwS&j=ohgCifwb&j=o3bEifwU&j=ofuzffwh&j=oYcphfwA&j=orKLifwY&j=otefjfwZ&j=oyZcjfwM&j=ozxuifwC&j=ot3Zifwx&j=oVIaifwP&j=oNRpifw5&j=oWn4ifwp&j=o4Ejgfw1&j=oaxHhfwp&j=osfsifwb&j=ogWgjfwv&j=omQejfwt&j=o7mnhfwR&j=oIZncfw0&j=o0c6ifwk&j=oorwffwk&j=oG6phfwc&j=o7Azhfwh&j=o90uifwF&j=oKjEifwJ&j=otcHdfwj&j=ooQkifwA&j=oWBzhfw7&j=oDsijfwq&j=ojakjfwQ&j=ooHhifwo&j=o1hHhfw0&j=o4aVdfw6&j=o6Dmjfw8&jvk=JobListing&jvi=oIZncfw0%2CJobListing&j=oIZncfw0&__jvst=Employee&__jvsd=sF6rpjwp&__jvsc=Url&bid=n4alSZwV&nl=1"
# request_url = "https://jobs.jobvite.com/varonis/job/oKjEifwJ?nl=1&fr=true"


def job_request(s, request_url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    }

    r = s.get(request_url, headers=header)
    html_text = r.text

    soup = BeautifulSoup(html_text, "html.parser")
    return soup


def main(file_name="website_2_some_jobs.txt"):
    request_url_all_jobs = "https://jobs.jobvite.com/varonis/search?nl=1&j=oG0sifwa&j=osf0efwF&j=o8Lmifwh&j=oPhqifwy&j=oLwuifwN&j=o7cEifwZ&j=ofWgjfwu&j=oTUcjfw2&j=okx1gfwS&j=ohgCifwb&j=o3bEifwU&j=ofuzffwh&j=oYcphfwA&j=orKLifwY&j=otefjfwZ&j=oyZcjfwM&j=ozxuifwC&j=ot3Zifwx&j=oVIaifwP&j=oNRpifw5&j=oWn4ifwp&j=o4Ejgfw1&j=oaxHhfwp&j=osfsifwb&j=ogWgjfwv&j=omQejfwt&j=o7mnhfwR&j=oIZncfw0&j=o0c6ifwk&j=oorwffwk&j=oG6phfwc&j=o7Azhfwh&j=o90uifwF&j=oKjEifwJ&j=otcHdfwj&j=ooQkifwA&j=oWBzhfw7&j=oDsijfwq&j=ojakjfwQ&j=ooHhifwo&j=o1hHhfw0&j=o4aVdfw6&j=o6Dmjfw8&jvk=JobListing&jvi=oIZncfw0%2CJobListing&j=oIZncfw0&__jvst=Employee&__jvsd=sF6rpjwp&__jvsc=Url&bid=n4alSZwV&nl=1&fr=true"
    s = requests.session()

    soup = job_request(s, request_url_all_jobs)
    jobs_div = soup.find("div", class_="jv-job-list jv-search-list")

    jobs_detail_links = []

    for job_div in jobs_div.find_all("a"):
        job_code = job_div["href"]
        # print(job_code)
        jobs_detail_links.append(f"https://jobs.jobvite.com{job_code}?nl=1&fr=true")
        # print(jobs_div.find("div", class_="jv-job-list-name").text)

    f = open(file_name, "w", encoding="utf-8")

    for jobs_detail_link in jobs_detail_links:
        soup = job_request(s, jobs_detail_link)
        for_apply_link = jobs_detail_link.split("?")[0]
        job_apply_link = f"{for_apply_link}/apply?nl=1"
        job_title = soup.find("h2", class_="jv-header").text.strip()
        job_department_location = soup.find(
            "p", class_="jv-job-detail-meta"
        ).text.split("\n")

        job_department = job_department_location[1].strip()
        job_location = job_department_location[2].strip()
        job_description_html = soup.find(
            "div", class_="jv-job-detail-description"
        ).p.prettify()
        job_description_div = soup.find("div", class_="jv-job-detail-description")
        job_description_paras = job_description_div.find_all(["p", "li"])
        # job_description_paras = job_description_div.find_all("span")

        print("-------------------------------------------")
        print("Title: " + job_title)
        print("Apply Link: " + job_apply_link)
        print("Department: " + job_department)
        print("Location: " + job_location)
        print("Description: ")
        # print(job_description_html)
        i = 0
        for para in job_description_paras:
            if i == 0:
                i = i + 1
                continue

            elif (
                para.text == "Responsibilities:"
                or para.text == "Responsibilities:"
                or para.text == "Job Requirements:"
                or para.text == "Advantages:"
                or para.text == "Interfaces:"
            ):
                print(para.text)
                i = i + 2
                continue
            else:
                print(para.text)
                i = i + 1

        f.write(
            f"--------------------------------------------------------------------------------------------------\n"
        )
        f.write(f"Title: {job_title}\n")
        f.write(f"Apply link: {job_apply_link}\n")
        f.write(f"Location: {job_location}\n")
        f.write(f"Department: {job_department}\n")

        i = 0
        for para in job_description_paras:
            if i == 0:
                i = i + 1
                continue
            elif (
                para.text == "Responsibilities:"
                or para.text == "Responsibilities:"
                or para.text == "Job Requirements:"
                or para.text == "Advantages:"
                or para.text == "Interfaces:"
            ):
                f.write(para.text + "\n")
                i = i + 2
                continue
            else:
                f.write(para.text + "\n")
                i = i + 1

        time.sleep(3)

    f.close()

if __name__ == '__main__':
    main()