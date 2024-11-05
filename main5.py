import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Load data from the Excel file
excel_file_path =  r"C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\Desktop\Article page url list.xlsx"  # Replace with the path to your Excel file
df = pd.read_excel(excel_file_path)

# Placeholder tab ID
placeholder_tab_id = '//ponds.in/cdn/shop/files/Combo-FOP_Brightness-Powerhouses_{width}x.png?v=1722253507'

# Configure Chrome WebDriver
driver = r'C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\chromedriver-win64\chromedriver.exe' 
service = Service(driver)
driver = webdriver.Chrome(service=service)

# List to store flagged URLs
flagged_urls = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    url = row['Url']
    tab_id = str(row['Tabid'])  # Convert tab id to string for comparison

    try:
        # Open the URL in the browser
        driver.get(url)

        # Find the main div using the provided CSS selector
        main_div = driver.find_element(By.CSS_SELECTOR, '#template-product > div.flex.flex-col.items-center.bg-white.container > div > div > div.relative.product__slides.product-single__photos.sm\:w-\[50\%\].w-full > div > div.product__slides.product-single__photos.flickity-enabled.is-draggable.is-fade > div > div > div.product__photo.product__slide.is-selected')


        # Check if the found tab id matches the placeholder
        if main_div.get_attribute('tab-id') == placeholder_tab_id:
            flagged_urls.append(url)
            
            print(f"URL {url} flagged: Placeholder tab ID found.")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Close the browser
driver.quit()

# Print the flagged URLs
if flagged_urls:
    print("\nFlagged URLs:")
    for flagged_url in flagged_urls:
        print(flagged_url)
else:
    print("No URLs with the placeholder tab ID were found.")
