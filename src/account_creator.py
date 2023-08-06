import platform
import time

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL
from util import log


def get_driver() -> uc.Chrome:
    log.print_bold(f"Creating Chrome Driver...")
    options = Options()
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=960,540")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-web-security")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    extension = CHROME_DRIVER_PATHS[platform.system()].get("extension", "")
    if extension:
        options.add_extension(extension)
    options.binary_location = CHROME_DRIVER_PATHS[platform.system()]["browser"]
    driver = uc.Chrome(
        options=options, executable_path=CHROME_DRIVER_PATHS[platform.system()]["driver"], delay=10
    )

    driver.set_page_load_timeout(120)
    driver.implicitly_wait(120)

    log.print_ok_arrow(f"Successfully created chrome driver")
    return driver


class AccountCreator:
    def __init__(self):
        self.driver = get_driver()

    def start_new_account(self) -> None:
        time.sleep(1)
        self.driver.get(BASE_URL)
        self.driver.maximize_window()

        wait = WebDriverWait(driver, 30)
        element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="join-now"]/div[2]/div/fieldset/label[2]')
            )
        )
        radio_button = self.driver.find_element(
            By.XPATH, '//*[@id="join-now"]/div[2]/div/fieldset/label[2]'
        )  # select No
        radio_button.click()

        wait = WebDriverWait(self.driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="join-now"]/div[2]/div/div[1]/a'))
        )
        button = self.driver.find_element(By.XPATH, '//*[@id="join-now"]/div[2]/div/div[1]/a')
        button.click()  # click Continue

    def input_email(self, email: str) -> None:
        input_field = driver.find_element(By.NAME, "signup_displayname")
        input_field.send_keys(username)

        input_field = driver.find_element(By.NAME, "signup_email")
        # Send slow
        email = "noddsgnso@outlook.com"
        for character in email:
            input_field.send_keys(character)
            time.sleep(uniform(0.05, 0.1))

        input_field = driver.find_element(By.ID, "password")
        input_field.send_keys(password)

        input_field = driver.find_element(By.ID, "confirm_password")
        input_field.send_keys(password)

        time.sleep(1)

        input_field = driver.find_element(By.CLASS_NAME, "date-picker-input")
        input_field.send_keys(generate_random_date_of_birth(wiek1, wiek2))

        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="registration-submit"]'))
        )
        button.click()

    def close(self) -> None:
        self.driver.quit()
