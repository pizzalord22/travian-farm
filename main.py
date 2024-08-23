import subprocess
import sys
import random
import keyboard
import time
import tkinter as tk

# Function to check if a package is installed, and if not, install it
def install_package(package_name):
    try:
        __import__(package_name)
        print(f"{package_name} is already installed.")
    except ImportError:
        print(f"{package_name} not found. Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"{package_name} has been installed.")


# Check and install Selenium and WebDriver Manager
install_package("selenium")
install_package("webdriver_manager")

# Now that Selenium and WebDriver Manager are installed, continue with the main program
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # For automatic WebDriver management
from selenium.webdriver.chrome.options import Options  # Use options to configure Chrome WebDriver
import time

# Configuration
TRAVIAN_URL = "https://ts8.x1.europe.travian.com/"
RALLYPOINT_URL = "https://ts8.x1.europe.travian.com/build.php?id=39&gid=16&tt=99"
USERNAME = "b.phylipsen@gmail.com"  # Replace with your username
PASSWORD = "MarkHoudtvanPizza"  # Replace with your password
OASIS_COORDINATES = (12, 34)  # Example coordinates of the oasis
RAID_MINTIME = 360 #seconds
RAID_MAXTIME = 480 #seconds

# Set up Chrome options (optional: can configure headless mode or other settings)
chrome_options = Options()
# chrome_options.add_argument("--start-maximized")  # Open Chrome maximized
chrome_options.add_argument("--disable-search-engine-choice-screen")  # We don't need to search anything
# chrome_options.add_argument("--disable-extensions")  # Disable extensions for clean run

# Use ChromeDriverManager to automatically manage ChromeDriver and create a Service object
service = Service(ChromeDriverManager().install())

# Initialize WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

def login(username, password):
    driver.get(TRAVIAN_URL)
    time.sleep(1)

    # Step 3: Enter username using the provided XPath
    username_field = driver.find_element(By.XPATH, '//*[@id="loginScene"]/div/div/div/div/div/form/div/div/label[1]/input')
    username_field.send_keys(username)

    # Step 4: Enter password using the provided XPath
    password_field = driver.find_element(By.XPATH, '//*[@id="loginScene"]/div/div/div/div/div/form/div/div/label[2]/input')
    password_field.send_keys(password)

    # Step 5: Click the submit button using the provided XPath
    submit_button = driver.find_element(By.XPATH, '//*[@id="loginScene"]/div/div/div/div/div/form/div/div/div[2]/button')
    submit_button.click()

    # Step 6: Wait for the main dashboard or village page to load after logging in
    WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.ID, "villageName"))
    )
    time.sleep(2)
    print("Logged in successfully!")




def Auto_raidList(type, minTime, maxTime, startRaid):
    global timeNewraid

    if startRaid and timeNewraid < time.time():
        # Step 1: Open rally point
        driver.get(RALLYPOINT_URL)
        time.sleep(1)
        # Step 2: Start raid
        match type:
            case "close":
                submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
                submit_button.click()
                print("Raid send successfully!")
            case "Mid":
                submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
                submit_button.click()
                print("Raid send successfully!")          

            case "far":
                submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
                submit_button.click()
                print("Raid send successfully!")
            case "":
                print("No range selected")

        # step 3 calculate new time to start raid
        timeNewraid = time.time() + random.randint(minTime, maxTime)
        print(f"New raid at: {timeNewraid}")
        
def build_structure(building_name):
    # Go to the building area and choose a building to upgrade or construct
    driver.get("https://www.travian.com/building-area")

    # Find the building by name or position
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[text()='{building_name}']"))
    )

    building_element = driver.find_element(By.XPATH, f"//div[text()='{building_name}']")
    building_element.click()

    # Click the build or upgrade button
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "build-upgrade-button"))
    )

    upgrade_button = driver.find_element(By.CLASS_NAME, "build-upgrade-button")
    upgrade_button.click()

    print(f"{building_name} is being constructed or upgraded.")
    time.sleep(5)


def train_units(unit_name, quantity):
    # Navigate to the Barracks/Stable where units can be trained
    driver.get("https://www.travian.com/barracks")

    # Find the unit type and set the quantity
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[text()='{unit_name}']"))
    )

    unit_field = driver.find_element(By.XPATH, f"//input[@name='{unit_name}']")
    unit_field.clear()
    unit_field.send_keys(str(quantity))

    # Click the train button
    train_button = driver.find_element(By.CLASS_NAME, "train-button")
    train_button.click()

    print(f"Training {quantity} {unit_name} units.")
    time.sleep(5)


def attack_oasis(coordinates, units):
    # Go to the rally point
    driver.get("https://www.travian.com/rally-point")

    # Enter the coordinates of the oasis
    x_coord = driver.find_element(By.NAME, "x")
    y_coord = driver.find_element(By.NAME, "y")
    x_coord.send_keys(str(coordinates[0]))
    y_coord.send_keys(str(coordinates[1]))

    # Assign units to the attack
    for unit_type, count in units.items():
        unit_field = driver.find_element(By.NAME, f"t{unit_type}")
        unit_field.clear()
        unit_field.send_keys(str(count))

    # Choose attack type (0 = Attack, 1 = Raid, etc.)
    attack_type_radio = driver.find_element(By.ID, "button1")  # 'Attack' button
    attack_type_radio.click()

    # Click the confirm/send button
    send_button = driver.find_element(By.NAME, "btn_ok")
    send_button.click()

    print(f"Attack sent to oasis at coordinates {coordinates}.")
    time.sleep(5)

def main():
    global startRaid
    global timeNewraid
    timeNewraid = time.time()
    startRaid = False

    try:
        login(USERNAME, PASSWORD)
        while True:
            if keyboard.is_pressed('Ctrl+F7'): #Zou vanuit UI kunnen komen straks
                startRaid = not startRaid
                print(f"Autoraid {'activated' if startRaid else 'disabled'}")

            Auto_raidList("close", RAID_MINTIME, RAID_MAXTIME, startRaid)
            
        # Step 1: Build/upgrade village structures
        # build_structure("Main Building")
        # build_structure("Barracks")
        # build_structure("Warehouse")

        # Step 2: Train units
        # train_units("Legionnaire", 10)

        # Step 3: Attack an Oasis
        # attack_oasis(OASIS_COORDINATES, {"1": 5})  # Example: Send 5 Legionnaires (unit ID = 1)
            time.sleep(1)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
