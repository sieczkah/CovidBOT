from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re

# https://rcb-gis.maps.arcgis.com/apps/opsdashboard/index.html#/fc789be735144881a5ea2c011f6c9265
PATH = r'D:\Selenium-GRID\chromedriver.exe'
URL = "https://covid19-rcb-gis.hub.arcgis.com/"


class CovidPage:
    re_patterns = {'date': r'(\d\d\.\d\d\.\d{4})',
                   'infected': r'(osoby zakażone: ?\d{1,2} ?\d\d\d)',
                   'deaths': r'(przypadki śmiertelne: ?\d? ?\d\d\d)',
                   'deaths_covid': r'(wyłącznie z powodu COVID-19: ?\d*)',
                   'tests': r'(wykonane testy: ?\d* ? \d*)'
                   }

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=PATH)
        self.driver.get(URL)
        self.driver.maximize_window()

        self.change_frame("iframe[title='statystyk static'")
        self.change_frame("iframe[id='ifrSafe']")

# Data string is created by joining all scrapped html paragraphs
        self.data_string = ' '.join(self.get_ptags_list())
        self.extract_data()
        self.driver.quit()

    def change_frame(self, frame_selector):
        """Changes iframes embedded on source site"""
        iframe = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, frame_selector)
            ))
        self.driver.switch_to.frame(iframe)

    def get_ptags_list(self):
        """Get all of HTML p(paragraphs) tags"""
        sleep(15)  # waits 15 seconds for elements to load
        p_tags = self.driver.find_elements_by_css_selector('p')
        return [p_tag.text for p_tag in p_tags if p_tag.text != ' ']

    def extract_data(self):
        """Creates data dictionary from data string using regex"""
        self.data_dict = {}
        for key, pattern in self.re_patterns.items():
            self.data_dict[key] = re.search(pattern, self.data_string).group(1)

    def get_str_raport(self):
        str_raport = (f"""Dnia {self.data_dict['date']},
{self.data_dict['infected'].capitalize()},
{self.data_dict['deaths'].capitalize()},
{self.data_dict['deaths_covid'].capitalize()},
{self.data_dict['tests'].capitalize()}.
Powered by Hubi""")
        return str_raport

    def __repr__(self):
        return self.get_str_raport()


if __name__ == "__main__":
    print(CovidPage())
