"""
        class of test views Auth
    """
import time
from django.test import TestCase, Client
# Create your tests here.
from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = False


class UrlAuthTests(TestCase):
    """
    Class test of url of app Auth

    Args:
        TestCase ([type]): [description]
    """
    @classmethod
    def setUpTestData(cls):
        """This method make a account for testing the url form sign_in
        """
        browser = webdriver.Firefox(options=firefox_options)
        # print("\nCreation d'un compte\n")
        info = {"inputUsername": "Frost101",
                "inputemail": "anthony.thillerot@laposte.nettt",
                "inputPassword1": "azerty",
                "inputPassword2": "azerty",
                "inputNom": "Test_Nom",
                "inputprenom": "Test_prenom"}

        browser.get('http://127.0.0.1:8000/auth/sign_in.html')
        grid = browser.find_element_by_id('inputemail')
        grid.send_keys(info["inputemail"])
        grid = browser.find_element_by_id('inputUsername')
        grid.send_keys(info["inputUsername"])
        grid = browser.find_element_by_id('inputPassword1')
        grid.send_keys(info["inputPassword1"])
        grid = browser.find_element_by_id('inputPassword2')
        grid.send_keys(info["inputPassword2"])
        grid = browser.find_element_by_id('inputNom')
        grid.send_keys(info["inputNom"])
        grid = browser.find_element_by_id('inputprenom')
        grid.send_keys(info["inputprenom"])

        browser.execute_script(
            "document.getElementById('gridCheck').checked = true;")
        time.sleep(1)
        browser.execute_script(
            "document.getElementById('btn_submit_sign_in').click();")
        time.sleep(5)
        browser.quit()

    def setUp(self):
        """This method similar at __init__ for each instance
        """
        # Every test needs a client.
        self.client = Client()

        self.browser = webdriver.Firefox(options=firefox_options)

    def tearDown(self):
        self.browser.quit()

    def test_index_selenium(self):
        """
        test index with selenium
        """
        self.browser.get('http://127.0.0.1:8000/chess_app/index.html')
        self.assertEqual(self.browser.title, "chess at")
        time.sleep(2)

    def test_connection_selenium(self):
        """test connection with selenium
        """
        info = {"inputemail": "anthony.thillerot@laposte.nettt",
                "inputPassword1": "azerty",
                }
        self.browser.get('http://127.0.0.1:8000/chess_app/index.html')
        time.sleep(2)
        grid = self.browser.find_element_by_id('img_acc_dropdown')
        grid.click()
        grid = self.browser.find_element_by_id('inputEmail_connect')
        grid.send_keys(info["inputemail"])
        grid = self.browser.find_element_by_id('inputPassword_connect')
        grid.send_keys(info["inputPassword1"])
        grid = self.browser.find_element_by_id('button_valid_form')
        grid.click()
        time.sleep(2)
        self.assertEqual(self.browser.title, "Account")
        time.sleep(2)
