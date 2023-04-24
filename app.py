from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

ser = Service('./chromedriver')
uber_url = "https://auth.uber.com/v2/"
phone_numbers_per_proxy = 4

def read_file_lines(file_name):
    '''read file lines and return a list of lines'''
    with open(file_name, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def read_phone_numbers():
    '''read phone numbers from file and return a list of phone numbers'''
    return read_file_lines("numbers.txt")

def read_proxy_list():
    '''read proxy list from file and return a list of proxies'''
    return read_file_lines("proxies.txt")


def make_webdriver_object(proxy):
    '''make a webdriver object and return it'''
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en-US")
    options.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(service=ser, options=options)


def submit_phone_number(driver, phone_number):
    '''submit phone number and return True if successful else False'''
    try:
        driver.get(uber_url)
        phone_number_input = driver.find_element(By.XPATH, "//*[@id='PHONE_NUMBER_or_EMAIL_ADDRESS']")
        phone_number_input.send_keys(phone_number)
        phone_number_input.send_keys(Keys.RETURN)
        # driver.quit()
        return True
    except NoSuchElementException:
        return False


if __name__ == '__main__':
    # read phones and proxies
    phone_numbers = read_phone_numbers()
    proxy_list = read_proxy_list()
    current_proxy_index = 0
    # loop on phones
    for phone_index, phone_number in enumerate(phone_numbers):
        # change proxy every 4 phone numbers
        if phone_index % phone_numbers_per_proxy == 0:
            current_proxy_index += 1
        # get current proxy
        current_proxy = proxy_list[current_proxy_index] if current_proxy_index < len(proxy_list) else proxy_list[0]
        # make webdriver object
        driver = make_webdriver_object(current_proxy)
        # submit phone number
        if(submit_phone_number(driver, phone_number)):
            print(f"phone number {phone_number} submitted successfully")
        else:
            print(f"phone number {phone_number} failed to submit")
        # wait for 5 seconds and close the webdriver
        sleep(5)
        driver.quit()