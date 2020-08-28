from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from django.test import TestCase
from django.test import LiveServerTestCase
from django.utils.text import slugify
from django.urls import reverse
import unittest
from time import sleep
"""
class LoginViewSeleniumTest(LiveServerTestCase):

    def test_selenium_login(self):

        #Driver
        self.driver = webdriver.Chrome('FunctionalTesting/chromedriver.exe')

        # 1) Aprire home page sito
        self.driver.get("http://localhost:8000/")
        sleep(3)

        # 2) Cliccare sul tasto "login" della navbar
        button = self.driver.find_element_by_xpath("//span[contains(text(),'Login')]")
        self.driver.execute_script("arguments[0].click();", button)

        # Test che sia nella corretta pagina
        self.assertIn("http://localhost:8000/accounts/login", self.driver.current_url)
        sleep(3)

        # 3) Compilare i campi per fare login
        usernameField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='id_login']")))
        passwordField = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='id_password']")))
        usernameField.send_keys("simone_sudati")
        passwordField.send_keys("miaomiao")
        sleep(3)

        # 4) Cliccare il tasto "Sign In"
        button = self.driver.find_element_by_xpath("//button[@class='btn btn-primary waves-effect waves-light']")
        self.driver.execute_script("arguments[0].click();", button)


        # Test che sia nella corretta pagina
        self.assertIn("http://localhost:8000/", self.driver.current_url)

        #chiusura driver
        sleep(5)
        self.driver.quit()
"""