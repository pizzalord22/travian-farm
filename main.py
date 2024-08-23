import subprocess
import sys
import random
import time
import tkinter as tk
from tkinter import messagebox
import threading

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # For automatic WebDriver management
from selenium.webdriver.chrome.options import Options  # Use options to configure Chrome WebDriver

# Configuration
TRAVIAN_URL = "https://ts8.x1.europe.travian.com/"
RALLYPOINT_URL = "https://ts8.x1.europe.travian.com/build.php?id=39&gid=16&tt=99"
USERNAME = "b.phylipsen@gmail.com"  # Replace with your username
PASSWORD = "MarkHoudtvanPizza"  # Replace with your password
OASIS_COORDINATES = (12, 34)  # Example coordinates of the oasis

# Global variables for raid times and raid states
raid_min_time_close, raid_max_time_close = 360, 480
raid_min_time_mid, raid_max_time_mid = 360, 480
raid_min_time_far, raid_max_time_far = 360, 480
startRaid_close = startRaid_mid = startRaid_far = False
timeNewraid_close = timeNewraid_mid = timeNewraid_far = time.time()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")
service = Service(ChromeDriverManager().install())
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

def auto_raid_list(raid_type, minTime, maxTime, startRaid, next_raid_time):
    if startRaid and next_raid_time < time.time():
        # Open rally point
        driver.get(RALLYPOINT_URL)
        time.sleep(1)

        # Send raid based on type
        raid_button_xpath = '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button'
        submit_button = driver.find_element(By.XPATH, raid_button_xpath)
        submit_button.click()
        print(f"{raid_type.capitalize()} raid sent successfully!")

        # Calculate new time to start the raid
        return time.time() + random.randint(minTime, maxTime)
    return next_raid_time

def toggle_raid(raid_type):
    global startRaid_close, startRaid_mid, startRaid_far
    global raid_min_time_close, raid_max_time_close
    global raid_min_time_mid, raid_max_time_mid
    global raid_min_time_far, raid_max_time_far
    global timeNewraid_close, timeNewraid_mid, timeNewraid_far

    try:
        # Update times and toggle the corresponding raid
        if raid_type == "close":
            raid_min_time_close = int(min_entry_close.get())
            raid_max_time_close = int(max_entry_close.get())
            startRaid_close = not startRaid_close
            timeNewraid_close = time.time()
            status = "activated" if startRaid_close else "deactivated"
            update_button("close", startRaid_close)
        elif raid_type == "mid":
            raid_min_time_mid = int(min_entry_mid.get())
            raid_max_time_mid = int(max_entry_mid.get())
            startRaid_mid = not startRaid_mid
            timeNewraid_mid = time.time()
            status = "activated" if startRaid_mid else "deactivated"
            update_button("mid", startRaid_mid)
        elif raid_type == "far":
            raid_min_time_far = int(min_entry_far.get())
            raid_max_time_far = int(max_entry_far.get())
            startRaid_far = not startRaid_far
            timeNewraid_far = time.time()
            status = "activated" if startRaid_far else "deactivated"
            update_button("far", startRaid_far)

        messagebox.showinfo("Success", f"{raid_type.capitalize()} raid {status} with updated times.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for Min and Max times.")

def update_button(raid_type, startRaid):
    button = start_buttons[raid_type]
    if startRaid:
        button.config(text="Stop", bg="red")
    else:
        button.config(text="Start", bg="green")

def update_countdown():
    global timeNewraid_close, timeNewraid_mid, timeNewraid_far

    def time_left(next_raid_time):
        seconds_left = int(max(next_raid_time - time.time(), 0))
        minutes, seconds = divmod(seconds_left, 60)
        return f"{minutes:02}:{seconds:02}"

    # Update the countdown labels
    countdown_label_close.config(text=f"Close Raid: {time_left(timeNewraid_close)}")
    countdown_label_mid.config(text=f"Mid Raid: {time_left(timeNewraid_mid)}")
    countdown_label_far.config(text=f"Far Raid: {time_left(timeNewraid_far)}")

    # Call this function again after 1000 ms (1 second)
    root.after(1000, update_countdown)

def run_auto_raids():
    global timeNewraid_close, timeNewraid_mid, timeNewraid_far
    while True:
        timeNewraid_close = auto_raid_list("close", raid_min_time_close, raid_max_time_close, startRaid_close, timeNewraid_close)
        timeNewraid_mid = auto_raid_list("mid", raid_min_time_mid, raid_max_time_mid, startRaid_mid, timeNewraid_mid)
        timeNewraid_far = auto_raid_list("far", raid_min_time_far, raid_max_time_far, startRaid_far, timeNewraid_far)
        time.sleep(1)

def setup_gui():
    global min_entry_close, max_entry_close
    global min_entry_mid, max_entry_mid
    global min_entry_far, max_entry_far
    global countdown_label_close, countdown_label_mid, countdown_label_far
    global root, start_buttons

    root = tk.Tk()
    root.title("Travian Auto-Raider")

    def create_frame(parent, title, color):
        frame = tk.Frame(parent, borderwidth=2, relief="groove")
        title_label = tk.Label(frame, text=title, font=('Helvetica', 10, 'bold'), bg=color, fg='white')
        title_label.grid(row=0, column=0, columnspan=3, sticky='ew')
        return frame

    # Create frames for each raid type
    frame_close = create_frame(root, "Close Raid", "#ff6666")  # Light Red
    frame_close.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

    frame_mid = create_frame(root, "Mid Raid", "#66b3ff")  # Light Blue
    frame_mid.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    frame_far = create_frame(root, "Far Raid", "#99ff99")  # Light Green
    frame_far.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

    # Labels and entry fields for Close raid times
    tk.Label(frame_close, text="Min:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame_close, text="Max:").grid(row=1, column=1, padx=5, pady=5)
    min_entry_close = tk.Entry(frame_close, width=5)
    max_entry_close = tk.Entry(frame_close, width=5)
    min_entry_close.grid(row=2, column=0, padx=5)
    max_entry_close.grid(row=2, column=1, padx=5)

    start_buttons = {}
    start_buttons["close"] = tk.Button(frame_close, text="Start", bg="green", command=lambda: toggle_raid("close"))
    start_buttons["close"].grid(row=2, column=2, rowspan=2, padx=5, pady=5)

    # Labels and entry fields for Mid raid times
    tk.Label(frame_mid, text="Min:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame_mid, text="Max:").grid(row=1, column=1, padx=5, pady=5)
    min_entry_mid = tk.Entry(frame_mid, width=5)
    max_entry_mid = tk.Entry(frame_mid, width=5)
    min_entry_mid.grid(row=2, column=0, padx=5)
    max_entry_mid.grid(row=2, column=1, padx=5)

    start_buttons["mid"] = tk.Button(frame_mid, text="Start", bg="green", command=lambda: toggle_raid("mid"))
    start_buttons["mid"].grid(row=2, column=2, rowspan=2, padx=5, pady=5)

    # Labels and entry fields for Far raid times
    tk.Label(frame_far, text="Min:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame_far, text="Max:").grid(row=1, column=1, padx=5, pady=5)
    min_entry_far = tk.Entry(frame_far, width=5)
    max_entry_far = tk.Entry(frame_far, width=5)
    min_entry_far.grid(row=2, column=0, padx=5)
    max_entry_far.grid(row=2, column=1, padx=5)

    start_buttons["far"] = tk.Button(frame_far, text="Start", bg="green", command=lambda: toggle_raid("far"))
    start_buttons["far"].grid(row=2, column=2, rowspan=2, padx=5, pady=5)

    # Labels to display countdown
    countdown_label_close = tk.Label(root, text="Close Raid: --:--")
    countdown_label_close.grid(row=0, column=1, padx=10, pady=5)

    countdown_label_mid = tk.Label(root, text="Mid Raid: --:--")
    countdown_label_mid.grid(row=1, column=1, padx=10, pady=5)

    countdown_label_far = tk.Label(root, text="Far Raid: --:--")
    countdown_label_far.grid(row=2, column=1, padx=10, pady=5)

    # Start the countdown updates
    update_countdown()

    root.mainloop()

def main():
    login(USERNAME, PASSWORD)

    # Start the GUI in a separate thread to keep it responsive
    gui_thread = threading.Thread(target=setup_gui)
    gui_thread.daemon = True
    gui_thread.start()

    # Start the raid loop
    run_auto_raids()

if __name__ == "__main__":
    main()