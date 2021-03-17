from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re

# https://rcb-gis.maps.arcgis.com/apps/opsdashboard/index.html#/fc789be735144881a5ea2c011f6c9265

driver = webdriver.Chrome(executable_path=r'D:\Selenium-GRID\chromedriver.exe')
driver.get("https://covid19-rcb-gis.hub.arcgis.com/")
driver.maximize_window()

iframe_1 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "iframe[title='statystyk static'")
    ))
driver.switch_to.frame(iframe_1)

iframe_2 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.ID, "ifrSafe")
    ))
driver.switch_to.frame(iframe_2)

sleep(15)

p_tags = driver.find_elements_by_css_selector('p')

p_list = [p_tag.text for p_tag in p_tags if p_tag.text != ' ']
data_string = ' '.join(p_list)

date = re.search(r'(\d\d\.\d\d\.\d{4})', data_string).group(1)
infected = re.search(r'(osoby zakażone: \d{1,2} ?\d\d\d)', data_string).group(1)
deaths = re.search(r'(przypadki śmiertelne: \d? ?\d\d\d)', data_string).group(1)
deaths_covid = re.search(r'(wyłącznie z powodu COVID-19: \d*)', data_string).group(1)
tests = re.search(r'(wykonane testy: \d* ? \d*)', data_string).group(1)

covid_info = (f"""Dnia {date},
{infected.capitalize()},
{deaths.capitalize()},
{deaths_covid.capitalize()},
{tests.capitalize()}.
Powered by Hubi""")

print(covid_info)

driver.quit()
