# Job search at partner companies
from bs4 import BeautifulSoup
import urllib2
# import os

#########################################################################
# Goal is to automate job search among the Hackbright partner companies 
# and among the companies in the wider almunae network. 
# User can enter a location and whether they want a partner company
# and the program can scrape glassdoor for the jobs available 
# at those specific companies. 
# User can then narrow results by specific search parameters (e.g., only
# look for 'engineer' positions)
#########################################################################

devkey = os.environ['DEVKEY']

class JobInspector():
    
    def __init__(self, location, is_partner):
        self.city = location
        self.is_partner = is_partner

        if self.city == 'sf':
            self.locID = 1147401    # SF ID 
        elif self.city == 'sb':
            self.locID = 1147442    # Sunnyvale ID

        # Get relevant companies and store their search parameters
        self.companies = self.process_companies()


    def process_companies(self):
        """Converts a file with (line-separated) company names into a 
        list of search parameters to feed into web crawler"""

        if self.city == 'sf' and self.is_partner:
            filename = 'PartnerCompaniesSFEB.txt'
        # Add the other files. Ideally this info would not be in a text file, also.

        companies_file = open(filename, 'rU')
        companies = []

        for company in companies_file:
            company = company.rstrip().replace(" ", "+")
            companies.append(company)

        return companies

    def get_listings(self, title):
        

    def get_all_titles(self, target=None):
        """Get all available job titles"""

        all_listings = []

        for company in self.companies:

            start_url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="
            mid_url = "&sc.keyword="
            end_url = "&locT=C&locId="
            full_url = start_url + company + mid_url + company + end_url + self.locID
            curr_listings = self.get_company_listings(company, full_url) # Get the listings for the company from the url 
            all_listings.extend(curr_listings)

        return all_listings 

    def get_company_listings(self, company, url):
        """Get all of the content from the company's job listings"""

        result = urllib2.urlopen(url)
        soup = BeautifulSoup(result)
        jobs = self.scrape_jobs(soup)

        next = soup.find(class_ = 'next')   #check the next button

        # If it contains a link, follow that link and add it to the pages 

        # Turn the page into soup
        # Scrape the jobs on the page
        # If there is a next link, 


    def scrape_jobs(self, soup):
        """Gets all of the relevant information off of each page."""

        page_listings = soup.find_all("a", class_= "jobLink")

        jobs = []

        for listing in page_listings:
            title = listing.get_text()
            link = "https://www.glassdoor.com" + listing['href']
            company = company
            jobs.append((title, company, link))

        return jobs

    # def narrow_titles(self, target):
    #     """Look for a particular job title.""" 

    #     return [title for self.titles if target in title]
    

newJobs = JobInspector('sf', True)




