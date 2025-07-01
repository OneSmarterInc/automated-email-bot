from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from seleniumbase import Driver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import os
from dotenv import load_dotenv
import pyotp
import undetected_chromedriver as uc
from datetime import datetime
import sys


# #Function to get OTC
# def get_otp(secret_key='kknjpzscbmjvnfxk'):
#     totp = pyotp.TOTP(secret_key)
#     print(totp.now())
# get_otp()

load_dotenv()

def get_otp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.now()
# ------------------------------------------------------------------
# Selenium and Browser Options

# chrome_options = Options()
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#Download directory setup
# DOWNLOAD_DIR = r"E:\LagReport\Backend\excelproject\excelfile"
DOWNLOAD_DIR = r"S:\LagReport\Backend\excelproject\excelfile"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

#Chrome options with download prefs
chrome_options = uc.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True,
}
chrome_options.add_experimental_option("prefs", prefs)

chrome_options.add_argument("--disable-blink-features=AutomationControlled")

#Driver Setup
# driver = Driver(uc=True)
driver = uc.Chrome(options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 60)
shortWait = WebDriverWait(driver, 15)

#Login
try:
    web_url = "https://outlook.live.com/mail/0/"
    # driver.uc_open_with_reconnect(web_url, 4)
    driver.get(web_url)

    print("Opening Website...")
                                                                   
    signIn_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="action-oc5b26"]/span')))
    signIn_btn.click()
    print("Moving to signIn steps")
    
    #Page Switch
        # --- wait until a second window handle appears, then switch ---
    wait.until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)

    #Email
    email_box = wait.until(EC.element_to_be_clickable((By.ID, "i0116")))
    email_box.clear()
    email_box.send_keys(os.getenv('EMAIL'), Keys.ENTER)
    print("Email Entered.")
    
    #Password
    try:
        password_box = shortWait.until(EC.element_to_be_clickable((By.ID, "i0118")))
    except TimeoutException:
        password_box = shortWait.until(EC.element_to_be_clickable((By.ID, "passwordEntry")))
    password_box.clear()
    password_box.send_keys(os.getenv('PASSWORD'), Keys.ENTER)
    print("Password Entered.")

    #Click on "I can't use my Microsoft Authenticator app right now"
    sign_in_another_way = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signInAnotherWay"]')))
    sign_in_another_way.click()
    print("Selected sign-in using another way")
    
    time.sleep(5)
    #Click on "Use a Verification Code"
    verify_with_code = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idDiv_SAOTCS_Proofs"]/div[2]/div/div/div[2]/div')))
    verify_with_code.click()
    print("Clicked on verify with code")
    
    time.sleep(5)
    #OTC
    try:
        otc_input = shortWait.until(EC.element_to_be_clickable((By.ID, "idTxtBx_SAOTCC_OTC")))
    except TimeoutException:
        otc_input = shortWait.until(EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Code" and @placeholder="Code"]')))
    otc_input.clear()
    otc_input.send_keys(get_otp(os.getenv('SECRET_KEY')), Keys.ENTER)
    print("OTP Entered.")
    
    time.sleep(5)
    #No Button 1
    try:
        no_button = wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back")))
        no_button.click()
        print("Selected No.")
    except TimeoutException:
        no_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="button" and @value="No"]')))
        no_button.click()
        print("Selected No.")
    time.sleep(5)
    ########################################
    # try:
    #     name_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "content")]/div[1]')))
    #     if name_div:
    #         print("User Name:", name_div.text)
    #         name_div.click()
    #     else:
    #         print("Name element not found. Skipping this step.")
    # except TimeoutException:
    #     print("Name element not found.")
    ########################################

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="New mail"]')))
        print("Logged In to Outlook Successfully.")
    except TimeoutException:
        print("Login Failed or took too long.")
except TimeoutException:
    print("Login Timeout")
    driver.quit()
    sys.exit(1)
    
#Search
try:
    time.sleep(10)
    search_bar = wait.until(EC.element_to_be_clickable((By.ID, 'topSearchInput')))
    search_bar.click()
    time.sleep(5)
    search_bar.clear()
    
    search_date = datetime.today().strftime('%Y-%m-%d')
    search_bar.send_keys(f"SECURE AmericanBenefitCorp INVENTORY '{search_date}'")
    # For testing purpose2
    # search_bar.send_keys(f"SECURE AmericanBenefitCorp INVENTORY '2025-06-18'")
    search_bar.send_keys(Keys.ENTER)
    print("Searched for content.")
    
    
    time.sleep(5)
    #Select Inbox filter
    folders = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchScopeButtonId-option"]/span')))
    folders.click()
    time.sleep(2)
    Inbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchScopeButtonId-list1"]/span/span')))
    Inbox.click()
    time.sleep(10)
    # For testing purpose2
    # search_bar.send_keys( "SECURE AmericanBenefitCorp INVENTORY '2025-06-09'")
    
    #Select the first one div
    # try:
    #     first_search = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="listbox"]//div[@data-focusable-row="true"][1]')))
    #     first_search.click()
    #     print("Selected first search result.")
    # except NoSuchElementException:
    #     print("Searched mail not found.")
    #     driver.quit()
    #     sys.exit(1)
    
    print(f"Looking for email containing date in subject title: {search_date}")

    # Fetch all search results
    try:
        email_results = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@role="listbox"]//div[@data-focusable-row="true"]')
        ))
    except TimeoutException:
        print("No email results found.")
        driver.quit()
        sys.exit(1)

    found = False

    for i in range(len(email_results)):
        try:
            # Refresh the list to avoid stale element error
            email_list = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@role="listbox"]//div[@data-focusable-row="true"]')
            ))

            email = email_list[i]
            driver.execute_script("arguments[0].scrollIntoView(true);", email)
            email.click()
            time.sleep(5)

            # Check the subject's title attribute for the date
            try:
                subject_span = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//span[contains(@class, "JdFsz") and @title]')
                ))
                title_text = subject_span.get_attribute("title")  # e.g., "SECURE AmericanBenefitCorp INVENTORY '2025-06-23'"
            except TimeoutException:
                print("Title span not found.")
                time.sleep(3)
                continue

            if search_date in title_text:
                print(f"Found matching email with title: {title_text}")
                found = True
                break
            else:
                print(f"Email #{i+1} title does not match today's date ({search_date}). Found: {title_text}")
                time.sleep(3)
        except StaleElementReferenceException:
            print(f"Skipping stale email #{i+1}")
            continue
        except Exception as e:
            print(f"Error checking email #{i+1}: {str(e)}")
            continue

    if not found:
        print("No email found with matching subject title date.")
        driver.quit()
        sys.exit(1)
        
except TimeoutException:
    print("Error during finding email.")
    driver.quit()
    sys.exit(1)
 
#Get Link from the Email
try:
    time.sleep(3)
    link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Click here')]")))
    secure_url = link.get_attribute("href")
    print("Opening secure URL directly: ")
    driver.get(secure_url)
except NoSuchElementException:
    print("Link not found.")
    driver.quit()
    sys.exit(1)

try:
    #Enter Password of the secure link
    pass_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog:password"]')))
    pass_field.send_keys(os.getenv('SECURE_PASS'))
    pass_field.send_keys(Keys.ENTER)
    print("Secure password entered.")

    #Download File
    file_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='header-attachment-item']/a[contains(text(), 'AmericanBenefitCorpINVENTORY_') and contains(text(), '.xlsx')]")))
    file_link.click()
    print("Clicked on file.")

    #Wait while file downloads
    wait_time = 30
    print(f"Waiting for {wait_time}s, while file is being downloaded.")
    time.sleep(wait_time)
    driver.quit()
except NoSuchElementException:
    print("Error occured while downloading file.")
    driver.quit()
    sys.exit(1)
    
    
#Code Done