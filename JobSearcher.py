import urllib2
import xml.etree.ElementTree as ET
import os

class JobSearcher():

    def __init__(self, location, only_partners, title=None):

        self.location = location.rstrip().replace(" ", "+").replace(",", "%2C")
        self.only_partners = only_partners
        self.title = self.process_title(title)
        self.companies = self.process_companies()
        self.publisher_ID = os.environ['PUBLISHER_ID']
        self.url = self.make_url()


    def process_companies(self):
        """Converts a file with (line-separated) company names into a 
        list of search parameters"""

        partners_path = 'PartnerCompanies.txt'

        # Add the other files. This info would be in a db or something, but
        # for now I have it in txt files. 

        partners_file = open(partners_path, 'rU')

        companies = partners_file.readlines()

        if self.only_partners == "no":
            alumnae_path = 'AlumnaeCompanies.txt'
            alumnae_file = open(filename, 'rU')
            alumnae = alumnae_file.readlines()
            companies.extend(alumnae.readlines())

        formatted_companies = []

        for company in companies:
            company = company.rstrip().replace(" ", "+")
            formatted_companies.append(company)

        return formatted_companies


    def process_title(self, title):
        """Converts a title into search parameters for URL"""

        if title and title != '':
            title = title.rstrip().replace(" ", "+")
            return title
        else: 
            return None


    def make_url(self):
        """Build the URL from the relevant search parameters"""

        base_url = 'http://api.indeed.com/ads/apisearch?userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2&limit=10'
        pub_id = '&publisher=' + self.publisher_ID
        loc_url = '&l=' + self.location
        companies_url = '&as_cmp='

        for i in range(0, len(self.companies)):
            if i < (len(self.companies)-1):
                companies_url = companies_url + self.companies[i] + '+or+'
            else:
                companies_url = companies_url + self.companies[i]

        if self.title:
            return base_url + pub_id + loc_url + companies_url + '&as_and=' + self.title
        else:
            return base_url + pub_id + loc_url + companies_url


    def get_listings(self):
        """Returns a tuple with (title, company, link, location) to pass to 
        process on front end"""

        request = urllib2.Request(self.url)
        # page = urllib2.urlopen(request) # get the page

        jobs_tree = ET.parse('sampleresponse.xml') # parse the xml
        root = jobs_tree.getroot() 
        results = root.find('results') # get the results node under root

        listings = []

        for child in results:
            title = child.find('jobtitle').text
            company = child.find('company').text
            url = child.find('url').text
            location = child.find('city').text
            listings.append((title, company, url, location))

        return listings


if __name__ == "__main__":
    newJobs = JobSearcher('San Francisco, CA', True)
    listings = newJobs.get_listings()
    print listings




#http://api.indeed.com/ads/apisearch?publisher=90705505161788&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2&l=austin%2C+tx