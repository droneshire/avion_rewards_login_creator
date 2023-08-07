import platform
import random
import time

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, CHROME_DRIVER_PATHS
from util import log


def get_driver() -> uc.Chrome:
    log.print_bold("Creating Chrome Driver...")
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

    log.print_ok_arrow("Successfully created chrome driver")
    return driver


class AccountCreator:
    def __init__(
        self, email: str, backup_email: str, password: str, first_name: str, last_name: str
    ):
        self.driver = get_driver()
        self.email = email
        self.backup_email = backup_email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def init(self) -> None:
        log.print_ok_arrow("Initializing Account Creator...")

    def start_new_account(self) -> None:
        time.sleep(1)
        self.driver.get(BASE_URL)
        self.driver.maximize_window()

        wait = WebDriverWait(self.driver, 30)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="join-now"]/div[2]/div/fieldset/label[2]')
            )
        )
        radio_button = self.driver.find_element(
            By.XPATH, '//*[@id="join-now"]/div[2]/div/fieldset/label[2]'
        )  # select No
        radio_button.click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="join-now"]/div[2]/div/div[1]/a'))
        )
        button = self.driver.find_element(By.XPATH, '//*[@id="join-now"]/div[2]/div/div[1]/a')
        button.click()  # click Continue

        self._input_email()

    def _input_email(self) -> None:
        email = self.email

        input_field = self.driver.find_element(By.ID, "credential")
        input_field.send_keys(email)

        input_field = self.driver.find_element(By.ID, "confirmCredential")

        for character in email:
            input_field.send_keys(character)
            time.sleep(random.uniform(0.05, 0.1))

        time.sleep(1)

        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/app-layout/div/div/app-register-primary-credential/form/div/button",  # pylint: disable=line-too-long
                )
            )
        )
        button.click()

    def input_login_code(self, code: str) -> None:
        input_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='code']"))
        )
        input_field.send_keys(code)

        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/app-layout/div/div/app-register-primary-credential-verify/form/div[2]/button[2]",  # pylint: disable=line-too-long
                )
            )
        )
        button.click()

        self._input_profile()

    def _input_profile(self) -> None:
        first_name = self.first_name
        last_name = self.last_name
        password = self.password

        input_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='firstName']"))
        )
        input_field.send_keys(first_name)

        input_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='lastName']"))
        )
        input_field.send_keys(last_name)

        input_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']"))
        )
        input_field.send_keys(password)

        input_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='confirmPassword']"))
        )
        input_field.send_keys(password)

        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/app-layout/div/div/app-register-user-profile/form/div/button[2]",  # pylint: disable=line-too-long
                )
            )
        )
        button.click()

        self._review_terms()

    def _review_terms(self) -> None:
        check_box = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/app-layout/div/div/app-register-terms-and-conditions/app-terms-and-conditions/div/div[5]/rbc-checkbox/div/label/span",  # pylint: disable=line-too-long
                )
            )
        )
        check_box.click()

        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/app-layout/div/div/app-register-terms-and-conditions/app-terms-and-conditions/div/div[5]/div/button[2]",  # pylint: disable=line-too-long
                )
            )
        )
        button.click()

        self._backup_email()

    def _backup_email(self) -> None:
        email = self.backup_email
        input_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='credential']"))
        )
        input_field.send_keys(email)

        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/app-layout/div/div/app-register-second-credential/form/div/button",  # pylint: disable=line-too-long
                )
            )
        )
        button.click()

    def input_backup_login_code(self, code: str) -> None:
        input_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='code']"))
        )
        input_field.send_keys(code)

        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/app-layout/div/div/app-register-second-credential-verify/form/div[2]/button[2]",  # pylint: disable=line-too-long
                )
            )
        )
        button.click()

    def close(self) -> None:
        self.driver.quit()
