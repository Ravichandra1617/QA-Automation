import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set up your WebDriver path (e.g., ChromeDriver)
driver_path = r"C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\chromedriver-win64\chromedriver.exe"

def setup_driver(driver_path):
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    return driver

# Open the webpage
def open_page(driver, url):
    driver.get(url)

# Find the tab ID on the page
def get_tab_id(driver, tab_id_locator):
    # Modify this locator based on the structure of the webpage
    return driver.find_element(By.ID, tab_id_locator).text

# Read URLs and Tab IDs from an Excel sheet
def read_csv(file_path):
    data = pd.read_csv(file_path)  # This reads the Excel file from the provided path
    return data


# Close the driver
def close_driver(driver):
    driver.quit()

# Main function to execute the test
def main():
    driver_path = r'C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\chromedriver-win64\chromedriver.exe'  # Correct WebDriver path
    csv_path = r'https://langoordigital-my.sharepoint.com/:x:/g/personal/ravichandra_a_langoor_com/EQmrh9uCGSNGoddP5bExu4oBI3m7ynmDSSTJ-_3EATKXRA?e=SXCmH2'  # Path to the Excel file with URLs and Tab IDs

    # Read data from Excel file
    data = read_csv(csv_path)

    # Set to track unique Tab IDs
    unique_tab_ids = set()

    driver = setup_driver(driver_path)
    
    try:
        all_tests_passed = True
        
        # Loop through each URL and Tab ID from the Excel file
        for index, row in data.iterrows():
            url = row['URL']
            expected_tab_id = row['TabID']

            # Open the webpage
            open_page(driver, url)
            
            # Retrieve the actual Tab ID from the page
            try:
                actual_tab_id = get_tab_id(driver, 'tab-id-element')  # Replace with actual Tab ID element's ID or locator
                
                # Check if Tab ID is unique
                if actual_tab_id in unique_tab_ids:
                    print(f"Fail: Duplicate Tab ID '{actual_tab_id}' found on page {url}")
                    all_tests_passed = False
                else:
                    unique_tab_ids.add(actual_tab_id)
                    print(f"Pass: Tab ID '{actual_tab_id}' is unique for page {url}")
                    
                # Verify that the actual Tab ID matches the expected Tab ID from the Excel sheet
                if actual_tab_id != expected_tab_id:
                    print(f"Fail: Expected Tab ID '{expected_tab_id}' does not match actual Tab ID '{actual_tab_id}' for page {url}")
                    all_tests_passed = False
                else:
                    print(f"Pass: Tab ID matches for page {url}")
            
            except Exception as e:
                print(f"Fail: Could not retrieve Tab ID for page {url}. Error: {e}")
                all_tests_passed = False

        if all_tests_passed:
            print("Test Passed: All URLs and Tab IDs are unique and correct.")
        else:
            print("Test Failed: Some URLs or Tab IDs did not pass the tests.")

    finally:
        close_driver(driver)

if __name__ == "__main__":
    main()
