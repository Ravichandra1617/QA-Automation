from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the WebDriver (make sure chromedriver is in your PATH)
driver = webdriver.Chrome()


url = "https://www.wiproconsumerlighting.com/"
driver.get(url)

# Define the correct order of heading tags
expected_order = ["h1", "h2", "h3", "h4", "h5", "h6"]

# Locate all heading tags on the page
heading_tags = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6")

# Initialize variables to keep track of the last seen heading tag
last_heading_level = 0
is_order_correct = True

print("Heading tags and their text:")

# Loop through each heading tag found on the page
for heading in heading_tags:
    # Get the tag name and text of each heading
    tag_name = heading.tag_name
    tag_text = heading.text.strip()
    current_level = expected_order.index(tag_name) + 1  

    # Print the heading tag and its text
    print(f"{tag_name}: {tag_text}")

    # Check if the current heading level is not lower than the last level (ensuring order)
    if current_level < last_heading_level:
        is_order_correct = False
        print(f"Order error: {tag_name} appeared after {expected_order[last_heading_level - 1]}")
    
    last_heading_level = current_level  # Update last heading level


if is_order_correct:
    print("Heading tags are in correct order.")
else:
    print("Heading tags are NOT in correct order.")


driver.quit()
