from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set up your WebDriver path (e.g., ChromeDriver)
driver_path = r"C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\chromedriver-win64\chromedriver.exe"
def setup_driver(driver_path):
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service)
    return driver

# Open the webpages
def open_page(driver, url):
    url = r'https://ponds.in/blogs/skin-science/brighten-your-skin-for-diwali-with-ponds-vit-c-e-a-range'
    driver.get(url)

# Find all divs within the main div
def get_main_divs(driver):
    # Assuming there's a main div with some known class or id (modify this if needed)
    main_div = driver.find_element(By.CLASS_NAME, 'wrapper')  # Change to specific locator if necessary
    return main_div.find_elements(By.TAG_NAME, 'div')

# Check if images in divs have the src attribute
def check_images_in_divs(divs):
    for index, div in enumerate(divs):
        try:
            img = div.find_element(By.TAG_NAME, 'img')
            img_src = img.get_attribute('src')
            
            if not img_src:
                print(f"Fail: No 'src' found for image in div {index + 1}")
                return False
            else:
                print(f"Pass: 'src' found for image in div {index + 1}")
        
        except Exception as e:
            # If no image is found in this div, consider it a fail
            print(f"Fail: No image found in div {index + 1}")
            return False
    return True

# Close the driver
def close_driver(driver):
    driver.quit()

# Main function to execute the test
def main():
    driver_path = r'C:\Users\Ravichandra\OneDrive - Langoor Digital Pvt. Ltd\chromedriver-win64\chromedriver.exe'  # Correct WebDriver path
    url = r'https://ponds.in/blogs/skin-science/brighten-your-skin-for-diwali-with-ponds-vit-c-e-a-range'  # Replace with actual article page URL

    driver = setup_driver(driver_path)
    open_page(driver, url)
    
    try:
        divs = get_main_divs(driver)
        result = check_images_in_divs(divs)
        
        if result:
            print("Test Passed: All images have 'src' attribute.")
        else:
            print("Test Failed: Some images are missing 'src' attribute or not found.")
    
    finally:
        close_driver(driver)

if __name__ == "__main__":
    main()
