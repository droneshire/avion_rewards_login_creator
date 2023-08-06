import platform

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util import log

fake = faker.Faker()


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

    def login(self, username, password):
        time.sleep(1)
        driver.get("https://pl.imvu.com/next/home/")
        driver.maximize_window()

        wait = WebDriverWait(driver, 30)
        element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/section/div/div/div/section/div/div/button")
            )
        )
        button = driver.find_element(
            By.XPATH, "/html/body/section/div/div/div/section/div/div/button"
        )  # cookie accept
        button.click()

        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/nav/ul[2]/button"))
        )
        button = driver.find_element(By.XPATH, "/html/body/div[7]/nav/ul[2]/button")
        button.click()

        input_field = driver.find_element(
            By.XPATH, "/html/body/div[7]/section[2]/div/div/div/section/form/div[1]/input"
        )
        input_field.send_keys(username)

        input_field = driver.find_element(
            By.XPATH, "/html/body/div[7]/section[2]/div/div/div/section/form/div[2]/div[2]/input"
        )
        input_field.send_keys(password)

        button = driver.find_element(
            By.XPATH, "/html/body/div[7]/section[2]/div/div/div/section/form/div[4]/button"
        )
        button.click()


def create_account(name, wiek1, wiek2):
    username = (
        fake.user_name()
        + random.choice("abcdefghijklmnopqrstuvwxyz")
        + random.choice("abcdefghijklmnopqrstuvwxyz")
    )
    email = (
        random.choice("abcdefghijklmnopqrstuvwxyz")
        + random.choice("abcdefghijklmnopqrstuvwxyz")
        + fake.email()
    )
    password = generate_random_string(10)
    driver.get("https://pl.secure.imvu.com/welcome/ftux/account/")
    driver.maximize_window()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/section/div/div/div/section/div/div/button")
        )
    ).click()  # cookie accept

    input_field = driver.find_element(By.NAME, "signup_displayname")
    input_field.send_keys(username)

    rndm = generate_random_string(10)

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
    input("Press Enter to continue...")

    print(username + ":" + password)
    return f"{username}:{password}"


def setup_account(name):
    driver.get("https://pl.imvu.com/next/home/")

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.ID, "saveAndExit")))
    button = driver.find_element(By.ID, "saveAndExit")
    button.click()

    driver.get("https://pl.imvu.com/next/av/" + name)


def main():
    # Provide your 2captcha API key

    create_account("xd144241", 19, 25)

    time.sleep(10)

    input("Press Enter to continue...")

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    main()
