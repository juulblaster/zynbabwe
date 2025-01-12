import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.51.1"
]

user_agent = random.choice(user_agents)

screen_resolutions = [(1920, 1080), (1366, 768), (1280, 720)]
resolution = random.choice(screen_resolutions)

chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=chrome_options
)

driver.set_window_size(resolution[0], resolution[1])

file_path = os.getenv("RESULTS_FILE_PATH", "results.txt")
divider = "-" * 50 + "\n"

def write_to_file(updated_text, flash_text):
    print(f"Debug: Writing to file - updated_text: {updated_text}, flash_text: {flash_text}")
    with open(file_path, "a", encoding="utf-8") as file:    
        quitTime = datetime.now()
        file.write(f"{divider}\n")
        file.write(f"{quitTime}\n")
        file.write(f"{updated_text}\n")
        file.write(f"{flash_text}\n")
        file.write(f"{divider}\n")

try:
    driver.get("https://boleslavsky.denik.cz/volny-cas/kapela-hudba-zabava-skupina-anketa-hlasovani-20250103.html")
    print(f"Page title: {driver.title}")

    time.sleep(random.uniform(2, 6))

    scroll_distance = random.randint(1510, 1805)  
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
    time.sleep(random.uniform(1, 5))  

    wait = WebDriverWait(driver, 15)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Fair Play Grass']")))

    actions = ActionChains(driver)
    actions.move_to_element(button).perform()
    time.sleep(random.uniform(2, 4))  

    driver.execute_script("arguments[0].click();", button)
    print("Button clicked.")

except Exception as e:
    print(f"An error occurred while pressing the button: {e}")

# Look for the flash message first
try:
    flash_message = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'survey__flash-content')]"))
    )
    flash_text = flash_message.text
    print(f"Flash Message: {flash_text}")
#    write_to_file(execution_number, f"Flash Message: {flash_text}\n", divider)
except Exception as flash_exception:
    print("Flash message not found or disappeared too quickly.")

write_to_file("Res: ", flash_text)

# Wait for the first result element after the flash message
try:
    result_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'survey__progress-text') and contains(., 'Fair Play Grass')]"))
    )
    updated_text = result_element.text
    print(f"Updated text: {updated_text}")
    write_to_file("->", updated_text)
except Exception as result_exception:
    print("Result element not found or failed to load.")

    time.sleep(random.uniform(3, 6))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    quitTime = datetime.now()
    print(f"End at: {quitTime}")
    driver.quit()