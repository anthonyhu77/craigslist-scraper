from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import numpy as np
from time import sleep
from random import randint #avoid throttling by not sending too many requests one after the other



from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

class CraiglistScraper(object):
	def __init__(self, location, query, postal, max_price, radius):
		self.location = location
		self.query = query
		self.postal = postal
		self.max_price = max_price
		self.radius = radius

		self.url = f"https://{location}.craigslist.org/search/sss?query={query}&search_distance={radius}&postal={postal}&max_price={max_price}"
		self.driver = webdriver.Chrome(executable_path = r"C:\Users\antho\Downloads\chromedriver.exe")
		self.delay = 5

	def load_craigslist_url(self):
		self.driver.get(self.url)
		wait = WebDriverWait(self.driver, self.delay)
		wait.until(EC.presence_of_element_located((By.ID, "searchform"))) #Expected Condition Complete -> SearchForm Completely found  
	
	def test(self):
		print(self.url)


	def extract_elements(self):

		uClient = uReq(self.url)
		page_html = uClient.read()
		page_soup = soup(page_html, "html.parser") 
		uClient.close()


		results_num = page_soup.find('div', class_= 'search-legend')
		results_total = int(results_num.find('span', class_='totalcount').text) #pulled the total count of posts as the upper bound of the pages array

		pages = np.arange(0, results_total+1, 120)


		filename = "craigslist.csv"
		f = open(filename, "w")


		f.write("")


		uClient = uReq(self.url)
		page_html = uClient.read()
		uClient.close()
		containers = page_soup.find_all("li",{"class":"result-row"})
		for post_one in containers:
			try:
				the_price = post_one.a.text.strip()
			except:
				the_price = "NA"
			post_one_time = post_one.find('time', class_= 'result-date')
		
			try:
				post_one_datetime = str(post_one_time['datetime'])
			except:
				post_one_datetime = "NA"

			try:	
				post_one_title = str(post_one.find('a', class_='result-title hdrlnk'))
			except:
				post_one_title = "NA"
				
			#try:
			post_one_link = post_one.find("a", {"class": "result-title hdrlnk"})
				
			#except:
			#	post_one_link = "NA"

			try:
				titles = post_one.find('a', {'class': 'result-title'})
				titles = titles.text.split("$")
				if titles[0] == '':
					titles = titles[1]
				else:
					titles = titles[0]
			except:
				titles = "NA"

			area = post_one.find("span", {"class": "result-hood"})
			try:
				one_area = str(area.text.strip().replace('(', '').replace(')', ''))
			except:
				one_area = str(area)
			finally:
				one_area = "NA"

			sleep(randint(1,5))

			try:
				new_my_url = str(post_one_link)
				new_uClient = uReq(new_my_url) #Open connection, grabbing the page
				new_page_html = new_uClient.read() #Content as variable
				new_uClient.close()

				new_page_soup = soup(new_page_html, "html.parser") 

				text_body = new_page_soup.find("section",{"id": "postingbody"})
				text_body = str(text_body.text)
					
		
				the_text_body = text_body.replace('<br/>', '').replace(',', '-')
			except:
				the_text_body = "NA"

			f.write(str(titles.replace(',', '')) + "," + str(the_price) + "," + str(post_one_datetime) + "," + str(post_one_link).replace(',', '') + "," + str(titles.replace(',', '')) + "," + str(one_area.replace(',', '')) + "," + str(the_text_body) + "\n")

location = "sfbay"
query = "martin+guitar"
postal = "94201"
max_price = "500"
radius = "5"


scraper = CraiglistScraper(location, query, postal, max_price, radius)
scraper.load_craigslist_url()
scraper.extract_elements()
