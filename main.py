import settings
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Automatically get the good url for the selected chain
try:
    URL = [url for url, names in settings.SUPPORTED_CHAINS.items() if settings.CHAIN in names][0]
except:
    print("[-] Unknown chain")
    print("\tPlease check that you entered a chain from the supported chain list")
    print("\tOpen an issue if you still have a problem")
    quit("Quitting...")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
refreshed_assets = []
skipped_assets = []
error_assets = []

if settings.REFRESH_FROM_FILE:
    settings.VERBOSE and print("[+] Refreshing from the error file")
    try:
        f = open(settings.ERROR_FILE_NAME, 'r')
    except:
        print("[-] There are no error file")
        quit("Quitting...")
    settings.ASSET_LIST = list(set([x.strip() for x in f.readlines()]))
    f.close()

for asset in settings.ASSET_LIST:
    # open page and wait
    driver.get(f'{URL}/{settings.CHAIN}/{settings.CONTRACT_ADDRESS}/{asset}')
    time.sleep(2)

    # check if content is already indexed by OpenSea
    try:
        driver.find_element(by=By.XPATH, value="//p[normalize-space()='Content not available yet']")
        content_available = False
    except NoSuchElementException:
        content_available = True

    if settings.SKIP_INDEXED and content_available:
        settings.VERBOSE and print('[+] Skipping already indexed asset:', asset)
        skipped_assets.append(asset)
    else:
        # Refresh metadata and verify if query succeeded
        try:
            driver.find_element(by=By.XPATH, value="//button[@aria-label='More']").click()
            time.sleep(.4)
            driver.find_element(by=By.XPATH, value="//span[text()='Refresh metadata']").click()
        except NoSuchElementException:
            settings.VERBOSE and print('[-] Unable to refresh asset:', asset)
            error_assets.append(str(asset))
        time.sleep(.8)
        try:
            driver.find_element(by=By.XPATH, value="//div[contains(text(),'this item for an update')]")
            refreshed_assets.append(asset)
        except NoSuchElementException:
            settings.VERBOSE and print('[-] Unable to verify refresh for asset:', asset)
            error_assets.append(str(asset))

# Remove duplicate
error_assets = list(set(error_assets))

if settings.REFRESH_FROM_FILE:
    # Erase the content of the error file
    settings.VERBOSE and print("[+] Erasing the content of the error file")
    open(settings.ERROR_FILE_NAME, 'w').close()

if settings.SAVE_IN_FILE:
    settings.VERBOSE and print(f"[+] Saving all errors in the error file [{settings.ERROR_FILE_NAME}]")
    f = open(settings.ERROR_FILE_NAME, "a")
    f.write("\n".join(error_assets) + "\n")
    f.close()

print('------------ TOTAL ------------')
print('\t[+] refreshed_assets:', refreshed_assets)
print('\t[+] skipped_assets:', skipped_assets)
print('\t[+] error_assets:', error_assets)
print('')
print('\t[+] Total refreshed assets:', len(refreshed_assets))
print('\t[+] Total skipped assets:', len(skipped_assets))
print('\t[+] Total error assets:', len(error_assets))	