import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the Excel file
file_path = r"C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\Desktop\Article page url list.xlsx"  # Replace with the actual file path
df = pd.read_excel(file_path)

# Initialize the WebDriver (assuming Chrome, adjust if using a different browser)
driver_path = r'C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\chromedriver-win64\chromedriver.exe' 
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Define the asset ID to flag (in this case, the placeholder image asset ID)
placeholder_asset_id = '121484494'

# Define function to check the tab ID for each URL and flag placeholder asset IDs
def check_banner_tab_ids(url, expected_tab_id):
    driver.get(url)
    
    try:
        # Wait for the banner elements to be present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product__photo')))
        
        # Find the main div element for the banner using the appropriate class name
        banner_divs = driver.find_elements(By.CLASS_NAME, 'product__photo')  # Replace with actual class name
        tab_ids = []

        print(f"Found {len(banner_divs)} banner elements for URL: {url}")

        # Track if any placeholder images are found
        placeholder_found = False

        # Iterate over each banner div to get the tab id attribute or asset id
        for banner_div in banner_divs:
            tab_id = banner_div.get_attribute('data-image-src')  # Adjust this based on actual tab id attribute
            asset_id = banner_div.get_attribute('data-asset-id')  # Assuming asset ID is stored in 'data-asset-id'

            tab_ids.append(tab_id)
            
            # Check if the asset ID is the placeholder asset ID
            if asset_id == placeholder_asset_id:
                placeholder_found = True
                print(f"WARNING: Placeholder asset ID {placeholder_asset_id} found for URL: {url}")

        print(f"Tab IDs found: {tab_ids}")

        # Check if the expected tab ID matches and there are no duplicates
        if tab_ids.count(expected_tab_id) == 1 and not placeholder_found:
            print(f"PASS: Tab ID {expected_tab_id} found exactly once for URL: {url}")
            return True, None
        elif placeholder_found:
            print(f"FAIL: Placeholder image found for URL: {url}")
            return False, url
        else:
            print(f"FAIL: Tab ID {expected_tab_id} found {tab_ids.count(expected_tab_id)} times for URL: {url}")
            return False, url

    except Exception as e:
        print(f"Error while checking URL {url}: {e}")
        return False, url

# Track URLs that failed the test
failed_urls = []

# Iterate through the dataframe and check each URL with its respective tab id
for index, row in df.iterrows():
    url = row['Url']
    tab_id = str(row['Tabid'])

    test_passed, failed_url = check_banner_tab_ids(url, tab_id)
    if not test_passed and failed_url:
        failed_urls.append(failed_url)

# Final test result
if not failed_urls:
    print("All tests passed!")
else:
    print("Some tests failed for the following URLs with issues:")
    for url in failed_urls:
        print(url)

# Close the browser at the end of the test
driver.quit()
