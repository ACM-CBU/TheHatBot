import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class GitHubHelper:

    @staticmethod
    def make_driver():
        # selenium depends on the browser installed, and the driver version to be compatible.
        # with a pi running raspian it is easy enough to install the driver
        # with sudo apt-get install chromium-chromedriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=chrome_options)

    @staticmethod
    def login_to_github(driver: WebDriver, username: str, password: str):
        login_url = 'https://github.com/login'
        email_input = '//*[@id="login_field"]'
        signin_button = '//*[@id="login"]/form/div[4]/input[9]'
        password_input = '//*[@id="password"]'
        driver.get(login_url)
        time.sleep(.5)
        driver.find_element_by_xpath(email_input).send_keys(username)
        driver.find_element_by_xpath(password_input).send_keys(password)
        driver.find_element_by_xpath(signin_button).click()
        time.sleep(.5)
        assert 'https://github.com/' == driver.current_url
        return driver

    @staticmethod
    def add_user_to_organization(driver: WebDriver, organization_name: str, user_to_add: str):
        organization_invite_url = f'https://github.com/orgs/{organization_name}/invitations/{user_to_add}/edit'
        send_invite_button = '//*[@id="js-pjax-container"]/div[2]/form/div[4]/div/button'
        driver.get(organization_invite_url)
        time.sleep(.5)
        assert "Page not found" not in driver.title
        driver.find_element_by_xpath(send_invite_button).click()
        return driver
