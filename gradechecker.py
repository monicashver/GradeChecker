from selenium import webdriver
import time
import sys
import os

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def formatGradeData(data, credits, result):

	credits = credits.split(" ")

	result += "~~~~~~ CREDITS SO FAR: " + credits[2] + " ~~~~~~\n\n"

	for i in range(len(data)):
		result += "Class: " + data[i][0] + "\n"
		result += "Mark: " + data[i][2] + "\n"
		result += "Grade: " + data[i][3] + "\n"
		result += "ClassAverage: " + data[i][4] + "\n"

		if(data[i][2] == ""):
			result += "Don't worry fam, you'll get your grade soon\n"
		elif(data[i][3] <= data[i][4]):
			result += "You beat class average, fuck ya! \n"

		result += "\n\n"

	return result

def check_if_new_data(old, new):

	if(old == new):
	 	return 

	old = old.split("\n\n")
	new = new.split("\n\n")

	old_credits = old[1].split(' ')[4]
	new_credits = new[1].split(' ')[4]

	#no new credits accrewed
	if(float(old_credits) == float(new_credits)):
		return

	for i in range(2, len(old) - 1):
		old_credits = old[i].split('\n')
		new_credits = new[i].split('\n')

		#Grade number
		if(old_credits[2] != new_credits[2]):

			grade_num = new_credits[2].split(" ")[1]
			notify("Grade Update", "You have a new grade for " + old_credits[1] + 
			" of " + grade_num + "%")

		#average
		if(old_credits[4] != new_credits[4]):

			grade_letter = new_credits[3].split(" ")[1]
			class_avg = new_credits[4].split(" ")[1]

			#cool message if you beat class average
			if(grade_num < class_avg):
				notify("Grade Update", "The class average for " + old_credits[1] + " was posted."
					+ "You beat the class average with a " + grade_letter + ".", )
			else:
				notify("Grade Update", "The class average for " + old_credits[1] + " was posted."
					+ "You got an " + grade_letter + " in this class.", )

def check_past_data(data):

	results = data.split('\n')
	credentials = results[0].split(" ")

	if(len(credentials) == 2):
		return credentials, True

	return None, False

def get_pin():

	pin = int(input("Please type in your pin: "))

	while(pin >= 999999 or pin < 100000):
		pin = input("Please type in your pin: ")

	return pin

def get_id():

	studentId = input("Please type in your student number: ")

	while(studentId <= 99999999 or studentId > 9999999999):
		studentId = input("Please type in your student number: ")

	return studentId

def main():

	filename = 'workfile.txt'
	past_data = ''
	file_exists = False
	save = 'n'

	if(os.path.isfile(filename)):
		f = open(filename, 'r')
		past_data = f.read()
		f.close()
		file_exists = True

	credentials, saved = check_past_data(past_data)

	if(saved):
		studentId = credentials[0]
		pin = credentials[1]
		save = 'y'
		
	else:
		studentId = get_id()
		pin = get_pin()

		if(file_exists == False):
			save = raw_input("Would you like me to remember your credientials?: (y/n)")
			save = save.strip()

		while(save != 'y' and save != 'n'):
			save = raw_input("Please enter a valid command. sWould you like me to remember your credientials?: (y/n)")
			save = save.strip()

	#function calls to scrape the data
	url = "https://degreeexplorer.utoronto.ca/degreeExplorer/login.xhtml"

	browser = webdriver.Chrome()

	browser.get("https://sws.rosi.utoronto.ca")

	element = browser.find_element_by_name("personId")
	element.send_keys(studentId)

	element = browser.find_element_by_name("pin")
	element.send_keys(pin)

	browser.find_element_by_xpath("//*[@type='submit'][@value='Login']").click()

	#half ass error checking to finish
	try:
		browser.find_element_by_link_text("Transcripts, Academic History").click()
	except:
		print("Looks like your student number or pin is invalid please re-enter them.")
		studentId = get_id()
		pin = get_pin()
		element = browser.find_element_by_name("personId")
		element.send_keys("")
		element.send_keys(studentId)

		element = browser.find_element_by_name("pin")
		element.send_keys(pin)

		browser.find_element_by_xpath("//*[@type='submit'][@value='Login']").click()


	#status0 for first semester

	#Get parent element
	parent = browser.find_element_by_id("status1")

	#Get all children elements of the parent element
	children = parent.find_elements_by_tag_name("tr")

	grades = []
	print("ok")
	for i in range(1, len(children) - 2):
		data = children[i].find_elements_by_tag_name("td")
		class_name = data[0].text
		weight = data[1].text
		mark = data[2].text
		grade = data[3].text
		average = data[4].text

		grades.append([class_name, weight, mark, grade, average])

	credit_data_parent = children[len(children) - 2]
	credit_data = credit_data_parent.find_elements_by_tag_name("td")[0].text

	data = ''

	if(save == 'y'):
		data += str(studentId) + ' ' + str(pin) + '\n\n'

	data = formatGradeData(grades, credit_data, data)

	check_if_new_data(past_data, data)

	f = open('workfile.txt', 'w')
	f.write(data)
	f.close()

	browser.quit()



if __name__ == '__main__':


	while True:
		main()
		time.sleep(900) #repeat every 15 min

