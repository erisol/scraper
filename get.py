import re
import string
import urlparse
import urllib
import sys

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re
from bs4 import BeautifulSoup

class SjoScrape(object):
	def __init__(self, prefix, ending):
		self.prefix = str(prefix)
		self.ending = str(ending)
		self.url = "https://www.sjofartsdir.no/shipsearch/?search="+self.prefix+self.ending
		self.driver = webdriver.PhantomJS()
		self.driver.set_window_size(1120, 550)
		#self.gulesider = "http://www.gulesider.no/person/resultat/"


	def scrape(self):
		self.driver.get(self.url)
		val = ""
		try:
			self.driver.find_element_by_name('ctl00$FullRegion$uxShipList$uxSearchResult$ctl01$ctl00').click()
			val = self.driver.find_element_by_name('ctl00$FullRegion$uxShipList$uxSearchResult$ctl01$ctl00').get_attribute('value').encode('utf-8')
			print "name of the fucking boat:",val
		except NoSuchElementException:
			print "found nothing. retard script duurrrr. exiting"
			return None
		#ventetid i sec.
		wait = WebDriverWait(self.driver, 3)
		try:
			wait.until(lambda driver: self.driver.find_element_by_class_name('sectionDetail').is_displayed() == True)
		except:
			pass
		all_info = ""
		try:
			all_info = self.driver.find_elements_by_xpath("//div[@class='sectionDetail']")
		except:
			pass
		text = ""
		for all_text in all_info:
			text += all_text.get_attribute("innerHTML")
		text = text.replace('\n', ' ')
		#text = re.sub('\s\s+', ' ',text)
		text = BeautifulSoup(text, 'html.parser')

		all_keys = text.find_all('dt',text=True)

		keys = []
		for line in all_keys:
			try:
				keys.append(line.string.encode("utf-8"))
			except:
				keys.append(line.string)
		#print keys
		all_vals = text.find_all('dd')

		vals = []
		for line in all_vals:
			try:
				vals.append(line.text.encode("utf-8"))
			except:
				vals.append(line.text)
		"""
		#get eier
		eidx = 0
		gidx = 0
		is_person = False
		is_fritid = False
		is_org = True

		for i,item in enumerate(vals):
			if item.find("Orgnr"):
				is_org = False
				break

		for i,item in enumerate(vals):
			if item.find("fritidsfart"):
				is_fritid = True
				break

		for i,item in enumerate(keys):
			if item.find("dselsnummer") != -1:
				is_person = True
				print "im a person"
				break

		for idx, item in enumerate(keys):
			#if eidx > 0 and gidx > 0:
		#		break
			if keys[idx].find("Eier") and is_person:
				if item.find("Skipseier"):
					pass
				print "setting eidx"
				eidx = idx
				pass
			if keys[idx].find("Gateadresse") and is_person:
				print "setting gidx"
				gidx = idx
				pass
			
		print vals[eidx],eidx
		print keys[eidx],eidx

		gulesider = ""

		if is_person and is_fritid and not is_org:
				gulesider += " ".join(vals[eidx].split()) + " "
				gulesider += " ".join(vals[gidx].split())
				gulesider = gulesider.replace(" ","%20")

		if len(gulesider) > 0:
			print gulesider
		"""

		
		writeline = ""
		for i in range(0,len(keys)):


			if (keys[i] is None):
				writeline += "_nokey_"
				writeline += ":"
			else:
				writeline += " ".join(keys[i].split())
				writeline += ":"
			if (vals[i] is None):
				writeline += "_noval_"
				if (i != len(keys)-1):
					writeline += "||"
			else:
				writeline += " ".join(vals[i].split())
				if (i != len(keys)-1):
					writeline += "||"
				
						
		writeline += "\n"
		print writeline
		
		#write to file
		#with open ("scrape/"+self.prefix+".txt",'a') as scraped:
		#	scraped.write(writeline)
		
if __name__ == '__main__':

	p = "LG"
	from_ = 3200
	to_ = 3250

for i in range(from_,to_):
	scraper = SjoScrape(p,i)
	scraper.scrape()
