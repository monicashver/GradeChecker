import requests
import json
from selenium import webdriver
import time
def main():


	url = 'https://degreeexplorer.utoronto.ca/degreeExplorer/login.xhtml'

	browser = webdriver.Chrome()

	browser.get('https://sws.rosi.utoronto.ca')

	element = browser.find_element_by_name("personId")
	element.send_keys("**********")


	element = browser.find_element_by_name("pin")
	element.send_keys("*****")


	browser.find_element_by_xpath("//*[@type='submit'][@value='Login']").click()
	#browser.find_element_by_css_selector('input.button .c_button .s_button').click()

	browser.find_element_by_link_text("Transcripts, Academic History").click()


	browser.find_element_by_id('status1')

	time.sleep(60)

	browser.quit()

if __name__ == '__main__':
	main()