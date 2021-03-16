from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re

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

WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="ember131"]/div/div/p[3]/strong/span')
    ))

# tu jest problem, żeby się wszystko załadowało

day = driver.find_element_by_css_selector('#ember139').text
infected = driver.find_element_by_css_selector('#ember135').text
deaths_total = driver.find_element_by_xpath(r'//*[@id="ember131"]/div/div/p[3]/strong/span').text
deaths_only_covid = driver.find_element_by_xpath(r'//*[@id="ember129"]/div/div/p[3]/span/strong').text
tests_done = driver.find_element_by_xpath(r'//*[@id="ember123"]/div/div/p[3]/strong/span').text
date = ''.join(re.findall(r'(\d+.)', day))
infected_no = infected.replace('\n', '')

text_info = f"""{date}
{infected_no.capitalize()}
Śmierci: {deaths_total} w tym wyłącznie z powodu COVID: {deaths_only_covid}
Wykonanych testów: {tests_done}
Powered by Hubi"""

print(text_info)


driver.quit()
