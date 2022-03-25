import settings
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
refreshed_assets = []
skipped_assets = []
error_assets = []

for asset in settings.ASSET_LIST:
    # open page and wait
    driver.get(f'https://opensea.io/assets/{settings.CHAIN}/{settings.CONTRACT_ADDRESS}/{asset}')
    time.sleep(3)

    # check if content is already indexed by OpenSea
    try:
        driver.find_element(by=By.XPATH, value="//p[normalize-space()='Content not available yet']")
        content_available = False
    except NoSuchElementException:
        content_available = True

    if settings.SKIP_INDEXED and content_available:
        settings.VERBOSE and print('Skipping already indexed asset:', asset)
        skipped_assets.append(asset)
    else:
        # Refresh metadata and verify if query succeeded
        try:
            driver.find_element(by=By.XPATH, value="//section[@class='item--header']//button[1]").click()
        except NoSuchElementException:
            settings.VERBOSE and print('Unable to refresh asset:', asset)
            error_assets.append(asset)
        time.sleep(1)
        try:
            driver.find_element(by=By.XPATH, value="//div[normalize-space()='timer']")
            refreshed_assets.append(asset)
        except NoSuchElementException:
            settings.VERBOSE and print('Unable to verify refresh for asset:', asset)
            error_assets.append(asset)


print('refreshed_assets:', refreshed_assets)
print('skipped_assets:', skipped_assets)
print('error_assets:', error_assets)
print('')
print('Total refreshed assets:', len(refreshed_assets))
print('Total skipped assets:', len(skipped_assets))
print('Total error assets:', len(error_assets))