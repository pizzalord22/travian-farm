import subprocess
import sys
import random
import time
import csv
import re
import webbrowser
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
from tkinter import ttk

# Configuratie
TRAVIAN_URL = "https://ts8.x1.europe.travian.com/"
RALLYPOINT_URL = "https://ts8.x1.europe.travian.com/build.php?id=39&gid=16&tt=99"
STARTVILLAGE_MAPID = 120553
MAP_URL = "https://ts8.x1.europe.travian.com/position_details.php?mapId="  # zonder MAPid nummer
USERNAME = "b.phylipsen@gmail.com"
PASSWORD = "MarkHoudtvanPizza"

CHECK_IDS = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    391, 392, 393, 394, 395, 396, 397, 398, 399, 400,
    401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
    411, 793, 794, 795, 796, 797, 798, 799, 800, 801,
    802, 803, 804, 805, 806, 807, 808, 809, 810, 811,
    1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201,
    1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209,
    1210, 1211, 1212, 1595, 1596, 1597, 1598, 1599,
    1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607,
    1608, 1609, 1610, 1611, 1612, 1613, 1997, 1998,
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2398,
    2399, 2400, 2401, 2402, 2403, 2404, 2405, 2406,
    2407, 2408, 2409, 2410, 2411, 2412, 2413, 2414,
    2800, 2801, 2802, 2803, 2804, 2805, 2806, 2807,
    2808, 2809, 2810, 2811, 2812, 2813, 3202, 3203,
    3204, 3205, 3206, 3207, 3208, 3209, 3210, 3211,
    3212, 3213, 3610, 3611, 3612, 3613, 4009, 4010,
    4011
]

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

def Auto_raidList(root):
    global raid_min_time_close, raid_max_time_close, raid_min_time_mid, raid_max_time_mid, raid_min_time_far, raid_max_time_far
    global close_newRaidTime, mid_newRaidTime, far_newRaidTime
    global start_raidClose, start_raidMid, start_raidFar

    if start_raidClose and close_newRaidTime < time.time():    
        driver.get(RALLYPOINT_URL)
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
        submit_button.click()
        close_newRaidTime = time.time() + random.randint(raid_min_time_close, raid_max_time_close)
        raid_frames[0](close_newRaidTime)
        print("Close raid send successfully!")

    if start_raidMid and mid_newRaidTime < time.time():    
        driver.get(RALLYPOINT_URL)
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
        submit_button.click()
        mid_newRaidTime = time.time() + random.randint(raid_min_time_mid, raid_max_time_mid)
        raid_frames[1](mid_newRaidTime)
        print("Mid raid send successfully!")      

    if start_raidFar and far_newRaidTime < time.time():    
        driver.get(RALLYPOINT_URL)
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
        submit_button.click()
        far_newRaidTime = time.time() + random.randint(raid_min_time_far, raid_max_time_far)
        raid_frames[2](far_newRaidTime)
        print("Far raid send successfully!")

    root.after(1000, Auto_raidList, root)

def index_oasis():
    start_map_id = STARTVILLAGE_MAPID

    try:
        with open("gevonden_oases.csv", "r", newline='', encoding='utf-8') as file:
            if file.read().strip():
                print("CSV-bestand is niet leeg. Indexering wordt overgeslagen.")
                return
    except FileNotFoundError:
        pass

    with open("gevonden_oases.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Coordinates", "Distance", "Troops"])

    oases = []

    for check_id in CHECK_IDS:
        for offset in [-check_id, check_id]:
            map_id = start_map_id + offset
            url = f"{MAP_URL}{map_id}"
            driver.get(url)
            time.sleep(1)

            try:
                field_type = driver.find_element(By.XPATH, '//*[@id="tileDetails"]/h1')
                captured_text = field_type.text
                
                if "Unoccupied oasis" in captured_text:
                    coords_match = re.search(r'\(([^)]+)\)', captured_text)
                    coordinates = coords_match.group(1) if coords_match else "Onbekend"
                    
                    distance_element = driver.find_element(By.XPATH, '//*[@id="distance"]/tbody/tr/td[2]')
                    distance = distance_element.text if distance_element else "Onbekend"
                    
                    print(f"Onbezette oase gevonden bij: {url} met coördinaten {coordinates} en afstand {distance}")
                    oases.append((url, coordinates, distance))
            except Exception as e:
                print(f"Fout bij indexering van oase op {url}: {e}")

    oases.sort(key=lambda x: float(x[2].replace(',', '')) if x[2].replace(',', '').replace('.', '').isdigit() else float('inf'))

    with open("gevonden_oases.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for oasis in oases:
            writer.writerow(oasis)

    print("Oases zijn geïndexeerd en opgeslagen in gevonden_oases.csv.")

def setup_gui():
    root = tk.Tk()
    root.title("Travian tool")

    oasis_gui(root)
    raid_gui(root)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)

    return root

def create_title_bar(parent, title):
    title_bar = tk.Frame(parent, bg="red", height=1)
    title_bar.grid(row=0, column=0, sticky="ew")
    title_label = tk.Label(title_bar, text=title, bg="red", fg="white", font=("Arial", 10, "bold"), height=1)
    title_label.grid(row=0, column=0, padx=5, pady=5)
    return title_bar

def update_oasis_gui(list_frame):
    # Verwijder alle bestaande widgets uit het list_frame
    for widget in list_frame.winfo_children():
        widget.destroy()

    try:
        with open("gevonden_oases.csv", "r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            oases = list(reader)
            
            # Sorteer oases op afstand
            oases.sort(key=lambda row: float(row['Distance'].replace(',', '')) if row['Distance'].replace(',', '').replace('.', '').isdigit() else float('inf'))

            # Maak headers
            header_frame = tk.Frame(list_frame)
            header_frame.pack(fill="x")

            tk.Label(header_frame, text="Coordinates", width=11, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Distance", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Troops", width=40, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)

            for row in oases:
                url = row['URL']
                coordinates = row['Coordinates']
                distance = row['Distance']
                troops = row['Troops'] if 'Troops' in row else "No data"

                # Maak een frame voor elke rij
                row_frame = tk.Frame(list_frame)
                row_frame.pack(fill="x")

                # Toon coördinaten
                text = f"{coordinates}"
                link = tk.Label(row_frame, text=text, fg="blue", cursor="hand2", width=11, anchor="w")
                link.pack(side="left", fill="x", padx=5, pady=2)
                link.bind("<Button-1>", lambda e, url=url: webbrowser.open(url))

                # Toon afstand
                distance_label = tk.Label(row_frame, text=distance, width=10, anchor="w")
                distance_label.pack(side="left", fill="x", padx=5, pady=2)

                # Toon troops
                troops_label = tk.Label(row_frame, text=troops, width=40, anchor="w")
                troops_label.pack(side="left", fill="x", padx=5, pady=2)

    except FileNotFoundError:
        print("CSV file not found.")

def oasis_gui(parent):
    oasis_list_frame = tk.Frame(parent, padx=10, pady=10, borderwidth=2, relief="groove")
    oasis_list_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="ns")

    title_bar = tk.Frame(oasis_list_frame, bg="red", height=1)
    title_bar.grid(row=0, column=0, sticky="ew")
    title_label = tk.Label(title_bar, text="Oases list", bg="red", fg="white", font=("Arial", 10, "bold"), height=1)
    title_label.grid(row=0, column=0, padx=2, pady=2)

    list_frame = tk.Frame(oasis_list_frame)
    list_frame.grid(row=1, column=0, sticky="nsew")

    oasis_list_frame.grid_rowconfigure(1, weight=1)
    oasis_list_frame.grid_columnconfigure(0, weight=1)

    update_oasis_gui(list_frame)

    def refresh():
        update_oasis_gui(list_frame)
        parent.after(60000, refresh)

    parent.after(60000, refresh)

def raid_gui(parent):
    global raid_min_time_close, raid_max_time_close, raid_min_time_mid, raid_max_time_mid, raid_min_time_far, raid_max_time_far
    global close_newRaidTime, mid_newRaidTime, far_newRaidTime
    global start_raidClose, start_raidMid, start_raidFar

    global raid_frames
    raid_frames = []

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_rowconfigure(1, weight=1)
    parent.grid_rowconfigure(2, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    frame_close, startStop_var_close, min_entry_close, max_entry_close, update_close_time = raid_class_gui(
        0, parent, "Close", close_newRaidTime, start_raidClose, raid_min_time_close, raid_max_time_close
    )
    raid_frames.append(update_close_time)

    frame_mid, startStop_var_mid, min_entry_mid, max_entry_mid, update_mid_time = raid_class_gui(
        1, parent, "Mid", mid_newRaidTime, start_raidMid, raid_min_time_mid, raid_max_time_mid
    )
    raid_frames.append(update_mid_time)

    frame_far, startStop_var_far, min_entry_far, max_entry_far, update_far_time = raid_class_gui(
        2, parent, "Far", far_newRaidTime, start_raidFar, raid_min_time_far, raid_max_time_far
    )
    raid_frames.append(update_far_time)

    def update_globals():
        global start_raidClose, start_raidMid, start_raidFar
        start_raidClose = startStop_var_close.get()
        start_raidMid = startStop_var_mid.get()
        start_raidFar = startStop_var_far.get()

    def update_time_globals():
        global raid_min_time_close, raid_max_time_close, raid_min_time_mid, raid_max_time_mid, raid_min_time_far, raid_max_time_far
        raid_min_time_close = int(min_entry_close.get())
        raid_max_time_close = int(max_entry_close.get())
        raid_min_time_mid = int(min_entry_mid.get())
        raid_max_time_mid = int(max_entry_mid.get())
        raid_min_time_far = int(min_entry_far.get())
        raid_max_time_far = int(max_entry_far.get())

    startStop_var_close.trace_add("write", lambda *args: update_globals())
    startStop_var_mid.trace_add("write", lambda *args: update_globals())
    startStop_var_far.trace_add("write", lambda *args: update_globals())

    min_entry_close.bind("<FocusOut>", lambda event: update_time_globals())
    max_entry_close.bind("<FocusOut>", lambda event: update_time_globals())
    min_entry_mid.bind("<FocusOut>", lambda event: update_time_globals())
    max_entry_mid.bind("<FocusOut>", lambda event: update_time_globals())
    min_entry_far.bind("<FocusOut>", lambda event: update_time_globals())
    max_entry_far.bind("<FocusOut>", lambda event: update_time_globals())

def raid_class_gui(row, parent, name, newRaidTime, startStop, min_Time, max_Time):
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")

    # Titelbalk aanpassen
    title_bar = tk.Frame(frame, bg="red")
    title_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
    title_label = tk.Label(title_bar, text=f"Raid class {name}", bg="red", fg="white", font=("Arial", 10, "bold"))
    title_label.grid(row=0, column=0, padx=5, pady=5)

    # Label en Countdown aan de rechterkant
    label_next_raid = tk.Label(frame, text="Next raid in:", font=("Arial", 10))
    label_next_raid.grid(row=1, column=0, padx=5, pady=10, sticky="w")

    countdown_label = tk.Label(frame, text="0:00", font=("Arial", 10))
    countdown_label.grid(row=1, column=1, padx=5, pady=10, sticky="e")

    startStop_var = tk.BooleanVar(value=startStop)

    def Start_buttonPressed():
        if startStop_var.get():
            startStop_var.set(False)
            start_button.config(text="Start")
        else:
            startStop_var.set(True)
            start_button.config(text="Stop")

    tk.Label(frame, text="min sec").grid(row=4, column=0, sticky="w", padx=5)
    min_entry = tk.Entry(frame, textvariable=tk.IntVar(value=min_Time))
    min_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    tk.Label(frame, text="max sec").grid(row=6, column=0, sticky="w", padx=5)
    max_entry = tk.Entry(frame, textvariable=tk.IntVar(value=max_Time))
    max_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    start_button = tk.Button(frame, text="Start", borderwidth=1, relief="solid",  command=Start_buttonPressed)
    start_button.grid(row=6, column=0, columnspan=2, pady=5, sticky= "ew")

    def update_countdown():
        current_time = time.time()
        remaining_time = newRaidTime - current_time
        if remaining_time <= 0:
            countdown_label.config(text="0:00")
            return
        else:
            minutes, seconds = divmod(int(remaining_time), 60)
            countdown_label.config(text=f"{minutes}:{seconds:02d}")
        countdown_label.after(1000, update_countdown)

    def update_newRaidTime(new_time):
        nonlocal newRaidTime
        newRaidTime = new_time
        update_countdown()

    update_countdown()

    return frame, startStop_var, min_entry, max_entry, update_newRaidTime

def initialise():
    global raid_min_time_close, raid_max_time_close, raid_min_time_mid, raid_max_time_mid, raid_min_time_far, raid_max_time_far
    global close_newRaidTime, mid_newRaidTime, far_newRaidTime
    global start_raidClose, start_raidMid, start_raidFar

    close_newRaidTime = mid_newRaidTime = far_newRaidTime = time.time()
    start_raidClose = start_raidMid = start_raidFar = False
    raid_min_time_close =  raid_min_time_mid =  raid_min_time_far  = 360 
    raid_max_time_close =raid_max_time_mid = raid_max_time_far = 480

def check_oasis():
    with open("gevonden_oases.csv", "r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        oases = list(reader)

        for row in oases:
            if row:
                driver.get(row[list(row.keys())[0]])
                time.sleep(1)

                try:
                    troop_rows = driver.find_elements(By.XPATH, '//*[@id="troop_info"]/tbody/tr')
                    troops_values = []
                    
                    for troop_row in troop_rows:
                        troop_text = troop_row.text
                        if "simulate raid" in troop_text:
                            break
                        troops_values.append(troop_text)
                    
                    troops_value = ", ".join(troops_values)
                except Exception as e:
                    troops_value = None
                    print(f"Error fetching troop info: {e}")

                row['Troops'] = troops_value if troops_value else "No data"

        with open("gevonden_oases.csv", "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=oases[0].keys())
            writer.writeheader()
            writer.writerows(oases)
            
    print("Oasis updated")

def check_Oasis_after(root):
    check_oasis()
    root.after(10000, Auto_raidList, root)


def main():     
    initialise() 
    login(USERNAME, PASSWORD)
    index_oasis()
    check_oasis()

    root = setup_gui()
    root.after(1000, Auto_raidList, root)
    root.after(600000, check_Oasis_after, root)
    root.mainloop()


if __name__ == "__main__":
    main()
