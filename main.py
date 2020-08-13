from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import json
from time import time
from time import sleep

import config

start = time()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(config.target_url)

""" Home Page. Target =>
1. disclaimer check-box
2. continue button
"""
disclaimer = driver.find_element_by_name('disclaimer')
disclaimer.click()
sleep(0.5)

continue_button = driver.find_element_by_xpath('//*[@type="submit"]')
continue_button.click()
sleep(1)

""" Search Page. Target =>
1. lastName
2. firstName
3. partyType
4. caseType
5. county
6. search
"""
last_name = driver.find_element_by_name('lastName')
last_name.send_keys(config.last_name)
sleep(0.5)

first_name = driver.find_element_by_name('firstName')
first_name.send_keys(config.first_name)
sleep(0.5)

party_type = Select(driver.find_element_by_xpath("//select[@name='partyType']"))
party_type.select_by_value(config.party_type)
sleep(0.5)

case_type = driver.find_element_by_css_selector(f"input[type='radio'][value='{config.case_type}']")
case_type.click()
sleep(0.5)

county_name = Select(driver.find_element_by_xpath("//select[@name='countyName']"))
county_name.select_by_value(config.county_name)
sleep(0.5)

search_button = driver.find_element_by_xpath('//*[@type="submit"]')
search_button.click()
sleep(1)

""" Search Results Page. Target =>
1. find all case number links.
2. loop through them and parse data into json.
"""
cases = driver.find_elements_by_xpath("//tr[@class='odd']/td[1]/a[@href]")
cases += driver.find_elements_by_xpath("//tr[@class='even']/td[1]/a[@href]")
cases = [case.get_attribute("href") for case in cases]
# print(cases[:10])
print(len(cases))

""" Case Info. Target =>
1. case information
2. defendant information
3. charge and disposition information
"""
# data = {}
# for case in cases[:1]:
#     driver.get(case)
#     # tables = driver.find_elements_by_xpath("//table")
#     # # print(len(tables)) should be 28
#     # print(len(tables))
#     # labels = driver.find_elements_by_css_selector('span[class="FirstColumnPrompt"]')
#     # keys = driver.find_elements_by_xpath()
#     # print(len(labels),len(keys))
#     soup = BeautifulSoup(driver.page_source)
#     # print(soup.prettify())
#     x = soup.body.get_text()
#     # rows = driver.find_elements_by_xpath("//table")
#     delimiters = "Case Information","Defendant Information","Schedule Information","Charge and Disposition Information","Related Person Information"
#     regexPattern = '|'.join(map(re.escape, delimiters))
#     y = re.split(regexPattern, x)
#     print(y[1:])
#     print(len(y[1:]))
data = {}
i = 0
for case in cases:
    driver.get(case)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    x = soup.body.get_text()

    delimiters = "Case Information","Defendant Information","Schedule Information","Charge and Disposition Information","Related Person Information"
    regexPattern = '|'.join(map(re.escape, delimiters))
    y = re.split(regexPattern, x)
    data[i] = {}
    data[i]["Case Information"] = y[1]
    data[i]["Defendant Information"] = y[2]
    data[i]["Charge and Disposition Information"] = y[4]
    i += 1

with open('data.json', 'w') as f:
    json.dump(data, f)

end = time()
print("Time taken is %.2f min (or %d sec)" % (((end-start)/60), end-start))
driver.quit()
