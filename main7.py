import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to read URLs and unique IDs from an Excel sheet
def read_excel(file_path):
    df = pd.read_excel(file_path)
    urls = df['Url'].tolist()  # Assuming the column name for URLs is 'Url'
    ids = df['Tabid'].tolist()  # Assuming the column name for Unique IDs is 'Tabid'
    return df, urls, ids

# Function to check if unique ID is present in the page source
def check_unique_id_in_page(Url, Tabid):
    # Setup Chrome options for headless browsing
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Optional, run without opening the browser
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Open the URL
        driver.get(Url)
        
        # Get the page source (Inspect Mode)
        page_source = driver.page_source

        # Convert Tabid to a string, in case it's an integer or other type
        unique_id_str = str(Tabid)
        
        # Check if the unique ID is present in the page source
        if unique_id_str in page_source:
            return True  # Return True if unique ID is found
        else:
            return False
    
    finally:
        driver.quit()

# Main function to process the Excel and validate each URL
def main():
    # Path to the Excel file
    file_path = r"C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\Desktop\Article page url list.xlsx"  # Update with your actual Excel file path
    
    # Read URLs and Unique IDs from the Excel
    df, urls, unique_ids = read_excel(file_path)
    
    # Create a new column to store the results
    df['ID Found'] = ''  # Create a new column 'ID Found' for storing the result in column C
    df['count']=''
    
    count = 0
    # Iterate through each URL and unique ID, and perform the check
    for index, (url, unique_id) in enumerate(zip(urls, unique_ids)):
        if check_unique_id_in_page(url, unique_id):
            df.at[index, 'ID Found'] = 'Yes' 
            count +=1 # Mark 'Yes' if the unique ID is found
            df.at[index, 'count']=count
        else:
            df.at[index, 'ID Found'] = 'No'  # Mark 'No' if the unique ID is not found
            df.at[index, 'count']='0'
  
    # Save the updated DataFrame back to the same Excel file
    df.to_excel(file_path, index=False)
    
    print(f"Results have been logged in the Excel file at {file_path}")

# Run the script
if __name__ == "__main__":
    main()
