from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re

PATH = r'D:\Selenium-GRID\chromedriver.exe'
MAINPAGE_URL = "https://covid19-rcb-gis.hub.arcgis.com/"
DIRECT_IFRAME_URL = "https://rcb-gis.maps.arcgis.com/apps/opsdashboard/index.html#/fc789be735144881a5ea2c011f6c9265"

ptags_re_patterns = {'date': r'(\d\d\.\d\d\.\d{4})',
                     'infected': r'(osoby zakażone: ?\d{1,2} ?\d\d\d)',
                     'deaths': r'(przypadki śmiertelne: ?\d? ?\d\d\d)',
                     'deaths_covid': r'(wyłącznie z powodu COVID-19: ?\d*)',
                     'tests': r'(wykonane testy: ?\d* ? \d*)'
                     }

clsid_patterns = {'date': r'div[id="ember9"]',
                  'infected': r'div[id="ember54"] p:nth-child(3)',
                  'deaths': r'div[id="ember68"] p:nth-child(3)',
                  'deaths_covid': r'div[id="ember75"] p:nth-child(3)',
                  'tests': r'div[id="ember96"] p:nth-child(3)'
                  }


class CovidPage:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=PATH)

        try:
            self.driver.get(DIRECT_IFRAME_URL)
            self.scrapped_data = self.direct_iframe_scrapp(self.driver)
        except:
            self.driver.get(MAINPAGE_URL)
            self.scrapped_data = self.main_page_scrapp()

        self.driver.quit()

    @staticmethod
    def direct_iframe_scrapp(driver):
        sleep(5)
        clsid_data = {key: driver.find_element_by_css_selector(pattern).text
                      for key, pattern in clsid_patterns.items()}
        return clsid_data

    def main_page_scrapp(self):
        self.change_frame(self.driver, "iframe[title='statystyk static'")
        self.change_frame(self.driver, "iframe[id='ifrSafe']")
        return self.get_ptags_datalist(self.driver)

    @staticmethod
    def change_frame(driver, frame_selector):
        """Changes iframes embedded on source site"""
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, frame_selector)
            ))
        driver.switch_to.frame(iframe)

    @staticmethod
    def get_ptags_datalist(driver):
        """Get all of HTML p(paragraphs) tags"""
        sleep(15)  # waits 15 seconds for elements to load
        p_tags = driver.find_elements_by_css_selector('p')
        return [p_tag.text for p_tag in p_tags]

# class CovidData:
#
#     def extract_data(self):
#         """Creates data dictionary from data string using regex"""
#         self.data_dict = {}
#         for key, pattern in ptags_re_patterns.items():
#             self.data_dict[key] = re.search(pattern, self.data_string).group(1)
#
#     def get_str_raport(self):
#         str_raport = (f"""Dnia {self.data_dict['date']},
# {self.data_dict['infected'].capitalize()},
# {self.data_dict['deaths'].capitalize()},
# {self.data_dict['deaths_covid'].capitalize()},
# {self.data_dict['tests'].capitalize()}.
# Powered by Hubi""")
#         return str_raport
#
#     def __repr__(self):
#         return self.get_str_raport()


if __name__ == "__main__":
    print(CovidPage().scrapped_data)
