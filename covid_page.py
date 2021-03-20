from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re

PATH = r'D:\Selenium-GRID\chromedriver.exe'
MAINPAGE_URL = "https://covid19-rcb-gis.hub.arcgis.com/"
DIRECT_IFRAME_URL = "https://rcb-gis.maps.arcgis.com/apps/opsdashboard/index.html#/fc789be735144881a5ea2c011f6c9265x"

ptags_re_patterns = {'date': r'(\d\d\.\d\d\.\d{4})',
                     'infected': r'(osoby zakażone: ?\d{1,2} ?\d\d\d)',
                     'deaths': r'(przypadki śmiertelne: ?\d? ?\d\d\d)',
                     'deaths_covid': r'(wyłącznie z powodu COVID-19: ?\d*)',
                     'tests': r'(wykonane testy: ?\d* ?\d*)'
                     }

clsid_patterns = {'date': r'div[id="ember9"]',
                  'infected': r'div[id="ember54"] p:nth-child(3)',
                  'deaths': r'div[id="ember68"] p:nth-child(3)',
                  'deaths_covid': r'div[id="ember75"] p:nth-child(3)',
                  'tests': r'div[id="ember96"] p:nth-child(3)'
                  }


class CovidPage:

    def __init__(self):
        """Opens webdriver and scraps the covid date from Iframe, if iframe fails scraps it from main webpage"""

        self.driver = webdriver.Chrome(executable_path=PATH)
        self.clsid_data = None
        self.ptag_data = None

        try:
            self.driver.get(DIRECT_IFRAME_URL)
            self.clsid_data = self.direct_iframe_scrap(self.driver)
            self.is_directdata = True
        except:
            self.driver.get(MAINPAGE_URL)
            self.main_page_scrap()
            self.is_directdata = False
        self.driver.quit()

    @staticmethod
    def direct_iframe_scrap(driver):
        """Scrap data from iframe webpage. Locates items by css_selector located in clsid_patterns global var"""

        sleep(10)  # waits 10 seconds for elements to load
        clsid_data = {key: driver.find_element_by_css_selector(pattern).text
                      for key, pattern in clsid_patterns.items()}
        return clsid_data

    def main_page_scrap(self):
        """Scrap data from main webpage. If iframe is not available"""

        self.change_frame(self.driver, "iframe[title='statystyk static'")
        self.change_frame(self.driver, "iframe[id='ifrSafe']")
        self.get_ptags_datalist()

    @staticmethod
    def change_frame(driver, frame_selector):
        """Changes iframes embedded on source site"""

        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, frame_selector)
            ))
        driver.switch_to.frame(iframe)

    def get_ptags_datalist(self):
        """Get all of HTML p-tags from the website and returns it as one string"""

        sleep(15)  # waits 15 seconds for elements to load
        p_tags = self.driver.find_elements_by_css_selector('p')
        self.ptag_data = ''.join([p_tag.text for p_tag in p_tags])


class CovidData:

    def __init__(self):
        """Creates CovidPages object to scrap the data and handles it with main() method"""

        self.page = CovidPage()
        self.covid_dat_dict = {}
        self.covid_dat_json = None
        self.main()

    def main(self):
        """Handles and format data into dictionary according to source direct(iframe) or not"""

        if self.page.is_directdata:
            self.covid_dat_dict = self.page.clsid_data
            self.covid_dat_dict['date'] = re.search(r'(\d\d\.\d\d\.\d{4})',
                                                    self.covid_dat_dict['date']).group(1)
        else:
            self.covid_dat_dict = self.extract_data(self.page.ptag_data)

    @staticmethod
    def extract_data(data_string):
        """Creates data dictionary from data string using regex"""

        covid_dat_dict = {}
        for key, pattern in ptags_re_patterns.items():
            # to match correct data word characters are needed in regex pattern
            # to get rid of those characters to save only needed data we split the string with ':'
            data = re.search(pattern, data_string).group(1).split(':')
            # because string looks like WORDS WORDS : number data ---> we access last element from the list
            covid_dat_dict[key] = data[-1].strip()
        return covid_dat_dict

    def get_str_report(self):
        """Creates string report that contains covid data from dictionary"""

        str_report = (f"""Dnia {self.covid_dat_dict['date']},
Osoby zakażone: {self.covid_dat_dict['infected']},
Przypadki śmiertelne: {self.covid_dat_dict['deaths']},
Wyłącznie z powodu covid-19: {self.covid_dat_dict['deaths_covid']},
Wykonane testy: {self.covid_dat_dict['tests']}.
Powered by Hubi""")
        return str_report

    def __repr__(self):
        return self.get_str_report()


if __name__ == "__main__":
    print(CovidData())
