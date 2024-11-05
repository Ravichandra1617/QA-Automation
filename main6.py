import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Load Excel file
file_path = r"C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\Desktop\Article page url list.xlsx"
df = pd.read_excel(file_path)

# Launch the browser (ensure you have the appropriate driver installed)
driver = r'C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\chromedriver-win64\chromedriver.exe' 
service = Service(driver)
driver = webdriver.Chrome(service=service)


# Store URLs for duplicate tab ids
duplicate_tab_ids = {}

# Iterate through each row in the Excel file
for index, row in df.iterrows():
    url = row['Url']
    expected_tab_id = row['Tabid']

    # Open the URL in the browser
    driver.get(url)

    try:
        # Find element by tab id using Selenium's `find_element` method
        element = driver.find_element(By.ID, expected_tab_id)
        if element:
            print(f"Tab ID '{expected_tab_id}' found for URL: {url}")

            # Check if this tab id was already found for another URL
            if expected_tab_id in duplicate_tab_ids:
                print(f"Duplicate Tab ID '{expected_tab_id}' found for URLs: {duplicate_tab_ids[expected_tab_id]}, {url}")
                print("Test Case: PASS")
            else:
                duplicate_tab_ids[expected_tab_id] = url

    except:
        print(f"Tab ID '{expected_tab_id}' not found for URL: {url}")
        print("Test Case: FAIL")

# Close the browser
driver.quit()
