import axonius_job_scrapper
import comeet_job_scrapper
import fundbox_job_scrapper
import greenhouse_job_scrapper
import jobvite_job_scrapper
import panorays_job_scrapper
import papayaglobal_job_scrapper
import payoneer_job_scrapper
import unipaas_job_scrapper
import os


class JobScrapper:
    jobs_url = {"https://www.comeet.com/jobs/sunbit/37.001": comeet_job_scrapper.main,
                "https://www.axonius.com/company/careers/open-jobs": axonius_job_scrapper.main,
                "https://panorays.com/careers/": panorays_job_scrapper.main,
                "https://fundbox.com/careers/": fundbox_job_scrapper.main,
                "https://boards-api.greenhouse.io/v1/boards/sentinellabs/jobs/?content=true":
                    greenhouse_job_scrapper.main,
                "https://jobs.jobvite.com/varonis/search?nl=1&"
                "j=oG0sifwa&j=osf0efwF&j=o8Lmifwh&j=oPhqifwy&j=oLwuifwN&j=o7cEifwZ&j=ofWgjfwu&j=oTUcjfw2&j=okx1gfwS&"
                "j=ohgCifwb&j=o3bEifwU&j=ofuzffwh&j=oYcphfwA&j=orKLifwY&j=otefjfwZ&j=oyZcjfwM&j=ozxuifwC&j=ot3Zifwx&"
                "j=oVIaifwP&j=oNRpifw5&j=oWn4ifwp&j=o4Ejgfw1&j=oaxHhfwp&j=osfsifwb&j=ogWgjfwv&j=omQejfwt&j=o7mnhfwR&"
                "j=oIZncfw0&j=o0c6ifwk&j=oorwffwk&j=oG6phfwc&j=o7Azhfwh&j=o90uifwF&j=oKjEifwJ&j=otcHdfwj&j=ooQkifwA&"
                "j=oWBzhfw7&j=oDsijfwq&j=ojakjfwQ&j=ooHhifwo&j=o1hHhfw0&j=o4aVdfw6&j=o6Dmjfw8&"
                "jvk=JobListing&jvi=oIZncfw0%2CJobListing&j=oIZncfw0&__jvst=Employee&__jvsd=sF6rpjwp&__jvsc=Url&"
                "bid=n4alSZwV&nl=1&fr=true": jobvite_job_scrapper.main,
                "https://www.papayaglobal.com/careers/": papayaglobal_job_scrapper.main,
                "https://www.payoneer.com/careers/": payoneer_job_scrapper.main,
                "https://www.payoneer.com/careers/?gh_src=4858e6881us": payoneer_job_scrapper.main,
                "https://grnh.se/4858e6881us": payoneer_job_scrapper.main,
                "https://www.unipaas.com/careers": unipaas_job_scrapper.main
                }

    def __init__(self, github_code="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"):
        os.environ["GH_TOKEN"] = github_code

    def scrape(self, url, file_name):
        try:
            self.jobs_url[url](file_name)
        except KeyError:
            print(f"URL {url} not known. ")

            
if __name__ == '__main__':
    js = JobScrapper()
    js.scrape("https://www.payoneer.com/careers/", "data.txt")