from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

import Consts


class DriverManager:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": Consts.root+"\\data",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(webdriver, 10)

    def get_assicurazione(self):
        driver = self.driver
        wait = self.wait

        driver.get(Consts.url)
        time.sleep(1)

        made_it = False
        while not made_it:
            try:
                input_elements = driver.find_elements(By.CLASS_NAME, "tpd-inputPin")
                for index, elem in enumerate(input_elements):
                    elem.send_keys(Consts.pin[index])
                button = driver.find_element(By.XPATH, "//button[contains(@class, 'rosso')]")
                wait.until(EC.element_to_be_clickable(button))
                button.click()
                made_it = True
            except StaleElementReferenceException:
                time.sleep(1)

        time.sleep(10)

    def tear_down(self):
        self.driver.close()
