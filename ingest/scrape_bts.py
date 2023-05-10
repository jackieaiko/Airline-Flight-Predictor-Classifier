import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from datetime import date

def setup_driver(download_dir):
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    download_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {'download.default_directory': download_directory,
                                                "download.prompt_for_download": False,
                                                "download.directory_upgrade": True,
                                                "safebrowsing.enabled": True})
    
    options.add_experimental_option("excludeSwitches", ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30)
    return driver

# Filter Year:1987 - 2023, Filer Period:Jan - Dec
def select_dropdown(driver, year_index, period_index):
    # 1987(0) - 2022(35)
    filter_year = Select(driver.find_element(By.XPATH, '//*[@id="cboYear"]'))
    filter_year.select_by_index(year_index)

    # 0 - 11
    filter_period = Select(driver.find_element(By.XPATH, '//*[@id="cboPeriod"]'))
    filter_period.select_by_index(period_index)


def select_checkbox(driver):

    # check boxes
    driver.find_element(By.XPATH, '//*[@id="OP_CARRIER"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="OP_CARRIER_FL_NUM"]').click()
    sleep(1)

    # already checked: ORIGIN_AIRPORT_ID

    # uncheck
    driver.find_element(By.XPATH, '//*[@id="ORIGIN_AIRPORT_SEQ_ID"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="ORIGIN_CITY_MARKET_ID"]').click()
    sleep(1)

    # check boxes
    driver.find_element(By.XPATH, '//*[@id="ORIGIN"]').click()
    sleep(1)

    # already checked: DEST_AIRPORT_ID

    # uncheck
    driver.find_element(By.XPATH, '//*[@id="DEST_AIRPORT_SEQ_ID"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="DEST_CITY_MARKET_ID"]').click()
    sleep(1)

    # check boxes
    driver.find_element(By.XPATH, '//*[@id="DEST"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="CRS_DEP_TIME"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="DEP_TIME"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="DEP_DELAY_NEW"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="CRS_ARR_TIME"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="ARR_TIME"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="ARR_DELAY_NEW"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="ARR_DEL15"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="CANCELLED"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="DIVERTED"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="DISTANCE"]').click()
    sleep(1)


def scrape_bts_data(driver):
    button = driver.find_element(By.XPATH, '//*[@id="btnDownload"]')
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(button).click(button).perform()

    sleep(40)

    print("Downloaded Dataset")


def scrape_historical(driver):
    select_dropdown(driver, 35, 0)
    select_checkbox(driver)
    scrape_bts_data(driver)

    for i in range(1, 5):
        select_dropdown(driver, 35, i)
        scrape_bts_data(driver)

# scrape previous month
def scrape_timely(driver):
    year = int(date.today().year) - 1987 # 1987(0)
    month = int(date.today().month) - 1 # 0 - 11

    if month == 0:
        month = 11
    
    select_dropdown(driver, year, month - 1)
    select_checkbox(driver)
    scrape_bts_data(driver)

if __name__ == "__main__":
    print("Starting Scraping")
    driver = setup_driver("./downloads")

    url = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr"
    driver.get(url)

    scrape_historical(driver)

    #scrape_timely(driver)

    driver.quit()
