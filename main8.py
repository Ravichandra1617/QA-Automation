import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

# Function to read URLs and unique IDs from an Excel sheet
def read_excel(file_path):
    df = pd.read_excel(file_path)
    urls = df['Url'].tolist()  
    ids = df['Tabid'].tolist() 
    return df, urls, ids

# Function to check and find Tabid in img src attributes within a page's source
def find_tabid_in_img_src(Url, Tabid):
    # Setup Chrome options for headless browsing
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Optional, run without opening the browser
    
   
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
       
        driver.get(Url)
        
        # Get the page source (Inspect Mode)
        page_source = driver.page_source

        # Converting Tabid to a string 
        unique_id_str = str(Tabid)

        # Regular expression to find img src tags that contain the Tabid
        pattern = re.compile(r'<img [^>]*' + re.escape(unique_id_str) + r'[^>]*>')
        
        # Find all img src tags containing the Tabid
        matches = pattern.findall(page_source)

        # Return the count and the matches
        total_count = sum(match.count(unique_id_str) for match in matches)
        
        return total_count, matches  
    
    finally:
        driver.quit()

# Main function to process the Excel and validate each URL
def main():
    # Path to the Excel file
    file_path = r"C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\Desktop\Article page url list.xlsx"  # Update with your actual Excel file path
    
    # Read URLs and Unique IDs from the Excel
    df, urls, unique_ids = read_excel(file_path)
    
    # Create two new columns to store the results
    df['Tab ID in img src'] = ''  # Store the img src tags where Tabid is found
    df['Count in img src'] = 0  # Store the count of Tabid occurrences in img src tags
    
    # Iterate through each URL and unique ID, and perform the check
    for index, (url, unique_id) in enumerate(zip(urls, unique_ids)):
        count, matches = find_tabid_in_img_src(url, unique_id)
        
        # Store the matches (if any) and the count in the DataFrame
        if count > 0:
            df.at[index, 'Tab ID in img src'] = '; '.join(matches)  # Join the matches with ';' for better readability
        else:
            df.at[index, 'Tab ID in img src'] = 'Not Found'
        
        df.at[index, 'Count in img src'] = count  # Store the count of occurrences
    
    # Save the updated DataFrame back to the same Excel file
    df.to_excel(file_path, index=False)
    
    print(f"Results have been logged in the Excel file at {file_path}")

if __name__ == "__main__":
    main()
