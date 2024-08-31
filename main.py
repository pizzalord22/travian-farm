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

with open("Config.csv", "r", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    config = next(reader)
    travian_URL = config['Travian_URL']
    startVillage_MapID = int(config['StartVillage_MapID'])
    username = config['Username']
    password = config['Password']

# Set up Chrome options (optional: can configure headless mode or other settings)
chrome_options = Options()
# chrome_options.add_argument("--start-maximized")  # Open Chrome maximized
chrome_options.add_argument("--disable-search-engine-choice-screen")  # We don't need to search anything
chrome_options.add_argument("--force-device-scale-factor=0.8")
# chrome_options.add_argument("--disable-extensions")  # Disable extensions for clean run

# Use ChromeDriverManager to automatically manage ChromeDriver and create a Service object
service = Service(ChromeDriverManager().install())

# Initialize WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)

def login(username, password):
    driver.get(travian_URL)
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
        # Open rally point page on driver
        driver.get(f'{travian_URL}build.php?id=39&gid=16&tt=99')
        time.sleep(1)    
        try:
            # Press the start farm list button
            submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
            submit_button.click()
        except:
            print("Close Start Raid button could not be found") # path has changed when my plus account expired, so check path in new game
        # Create new random time for next raid
        close_newRaidTime = time.time() + random.randint(raid_min_time_close, raid_max_time_close)
        raid_frames[0](close_newRaidTime)
        print("Close raid send successfully!")

    if start_raidMid and mid_newRaidTime < time.time():
        # Open rally point page on driver
        driver.get(f'{travian_URL}build.php?id=39&gid=16&tt=99')
        time.sleep(1)  
        try:
            # Press the start farm list button
            submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
            submit_button.click()
        except:
            print("Mid Start Raid button could not be found") # path has changed when my plus account expired, so check path in new game
        # Create new random time for next raid
        mid_newRaidTime = time.time() + random.randint(raid_min_time_mid, raid_max_time_mid)
        raid_frames[1](mid_newRaidTime)
        print("Mid raid send successfully!")      

    if start_raidFar and far_newRaidTime < time.time():
        # Open rally point page on driver
        driver.get(f'{travian_URL}build.php?id=39&gid=16&tt=99')
        time.sleep(1)  
        try: 
            # Press the start farm list button
            submit_button = driver.find_element(By.XPATH, '//*[@id="rallyPointFarmList"]/div[2]/div[2]/div/div/button')
            submit_button.click()
        except:
            print("Far Start Raid button could not be found") # path has changed when my plus account expired, so check path in new game
        # Create new random time for next raid
        far_newRaidTime = time.time() + random.randint(raid_min_time_far, raid_max_time_far)
        raid_frames[2](far_newRaidTime)
        print("Far raid send successfully!")

    root.after(1000, Auto_raidList, root)

def index_fields(x_offset, y_offset, oasis_frame, village_frame):
    try:
        with open("gevonden_oases.csv", "w", newline='', encoding='utf-8') as file:
           print("CSV-file has been cleared.")
    except:
        print("Opening CSV file failure")

    # create headers
    with open("gevonden_oases.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["MapID", "Coordinates", "Distance", "Troops", "Bounty/HP"])

    try:
        with open("villages.csv", "w", newline='', encoding='utf-8') as file:
           print("CSV-file has been cleared.")
    except:
        print("Opening CSV file failure")

    # create headers
    with open("villages.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["MapID", "Coordinates", "Distance", "Population", "Player",  "Alliance", "Tribe", "RaidList"])

    oases = []
    villages = []

    for x in range(-int(x_offset.get()), int(x_offset.get()) + 1):
        for y in range(-int(y_offset.get()), int(y_offset.get()) + 1):
            map_id = startVillage_MapID + x + y * 401
            url = f"{travian_URL}position_details.php?mapId={map_id}"
            driver.get(url)
            time.sleep(1)

            try:
                # find field title
                field_type = driver.find_element(By.XPATH, '//*[@id="tileDetails"]/h1')
                captured_text = field_type.text
                cleaned_text = captured_text.replace('\u202D', '')
                cleaned_text = cleaned_text.replace('\u2212', '-')
                
                # Check if field is an oasis
                if "Unoccupied oasis" in cleaned_text:
                    # get Coordinates from title
                    coords_match = re.search(r'\(([^)]+)\)', cleaned_text)
                    coordinates = coords_match.group(1) if coords_match else "Onbekend"
                    
                    try:
                        distance_element = driver.find_element(By.XPATH, '//*[@id="distance"]/tbody/tr/td[2]')
                        distance_text = distance_element.text.strip()
                        distance_match = re.match(r'(\d+(\.\d+)?) fields', distance_text)
                        distance = float(distance_match.group(1)) if distance_match else float('inf')
                    except Exception:
                        distance = float('inf')  # Fallback voor onbekende of ontbrekende afstanden

                    print(f"Onbezette oase gevonden bij: {map_id} met coördinaten {coordinates} en afstand {distance}")
                    oases.append((map_id, coordinates, distance))
                elif not("Wilderness" in cleaned_text or "Abandoned" in cleaned_text or "water" in cleaned_text):
                    # get Coordinates from title
                    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)
                    coords_match = re.search(r'([+-]?\d+)\s*[\|,]\s*([+-]?\d+)', cleaned_text)
                    coordinates = f"{coords_match.group(1)}|{coords_match.group(2)}"

                    # get distance
                    try: 
                        distance_element = driver.find_element(By.XPATH, '//*[@id="village_info"]/tbody/tr[5]/td')
                        distance_text = distance_element.text.strip()
                        distance_match = re.match(r'(\d+(\.\d+)?) fields', distance_text)
                        distance = float(distance_match.group(1)) if distance_match else float('inf')
                    except Exception:
                        print("distance not found")
                        return

                    # get population
                    try: 
                        population_element = driver.find_element(By.XPATH, '//*[@id="village_info"]/tbody/tr[4]/td')
                        population = population_element.text.strip()
                    except Exception:
                        print ("Population not found")
                        return

                    # get Player
                    try: 
                        player_element = driver.find_element(By.XPATH, '//*[@id="village_info"]/tbody/tr[3]/td')
                        Player = player_element.text.strip()
                    except Exception:
                        print ("Population not found")
                        return

                    # get Alliance
                    try: 
                        alliance_element = driver.find_element(By.XPATH, '//*[@id="village_info"]/tbody/tr[2]/td')
                        Allaince = alliance_element.text.strip()
                    except Exception:
                        print ("Population not found")
                        return

                    # get Tribe
                    try:
                        tribe_element = driver.find_element(By.XPATH, '//*[@id="village_info"]/tbody/tr[1]/td')
                        Tribe = tribe_element.text.strip()
                    except Exception:
                        print ("Population not found")
                        return

                    if y != 0 and x !=0:    
                        villages.append((map_id, coordinates, distance, population, Player, Allaince, Tribe))

            except Exception as e:
                print(f"Fout bij indexering van oase op {url}: {e}")

    # Sorteer de oases en villages op basis van afstand
    oases.sort(key=lambda x: x[2])
    villages.sort(key=lambda x: x[2])

    with open("gevonden_oases.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for oasis in oases:
            writer.writerow(oasis)

    with open("villages.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for village in villages:
            writer.writerow(village)

    update_oasis_gui(oasis_frame)
    update_villages_gui(village_frame)

    print("Oases and villages zijn geïndexeerd en opgeslagen in CSVs.")

    check_oasis()

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

def raid_hero(coordinates):  
    # Open rally point page on driver
    driver.get(f'{travian_URL}build.php?id=39&gid=16&tt=2')
    time.sleep(1)

    # Add Hero as unit
    try:
        hero_quantity = driver.find_element(By.XPATH, '//*[@id="troops"]/tbody/tr[3]/td[4]/input')
        hero_quantity.send_keys("1")
    except:
        print("Raid Hero function: Adding hero failed")
        return

    #split Coordinates
    X_value, Y_Value = coordinates.split('|')

    # Add X coordinate
    try:
        X_Coordinates = driver.find_element(By.XPATH, '//*[@id="xCoordInput"]')
        X_Coordinates.send_keys(X_value)
    except:
        print("Raid Hero function: Adding X coordinate failed")
        return

    # Add X coordinate
    try:
        X_Coordinates = driver.find_element(By.XPATH, '//*[@id="yCoordInput"]')
        X_Coordinates.send_keys(Y_Value)
        time.sleep(0.5)
    except:
        print("Raid Hero function: Adding Y coordinate failed")
        return

    try:
        # Select 'Attack: Raid'
        Raid_checkbox = driver.find_element(By.XPATH, '//*[@id="build"]/div/form/div[2]/label[3]/input')
        Raid_checkbox.click()
    except:
        print(f"Raid Hero function: Raid checkbox failed")
        return
    
    # Click on the send button in troop overview
    try:
        send_button = driver.find_element(By.XPATH, '//*[@id="ok"]')
        send_button.click()
        time.sleep(1)
    except:
        print("Raid Hero function: send button in troop overview failed")
        return

    # Click on the confirm button
    try:
        Confirm_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div[3]/div/form/div[1]/button[3]')
        Confirm_button.click()
    except:
        print("Raid Hero function: Confirm button in attack overview failed")
        return

def show_confirmation_popup(Coordinates):
    popup = tk.Toplevel()
    popup.title("Confirm Action")

    tk.Label(popup, text=f"Send Hero to oasis {Coordinates}?", font=("Arial", 12)).pack(pady=10)
    
    def confirm_action():
        raid_hero(Coordinates)
        popup.destroy()

    confirm_button = tk.Button(popup, text="Confirm", command=confirm_action)
    confirm_button.pack(side="left", padx=20, pady=20)
    
    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
    cancel_button.pack(side="right", padx=20, pady=20)

def heroTraveling():
    HeroStatus_Icon = driver.find_element(By.XPATH, '//*[@id="topBarHero"]/div/a/i')
    HeroStatus = HeroStatus_Icon.get_attribute('class')
    heroIsTraveling = "heroRunning" == HeroStatus
    return heroIsTraveling

def update_oasis_gui(list_frame):
    # Verwijder alle bestaande widgets uit het list_frame
    for widget in list_frame.winfo_children():
        widget.pack_forget()

    try:
        with open("gevonden_oases.csv", "r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            oases = list(reader)
            
            # Maak headers
            header_frame = tk.Frame(list_frame)
            header_frame.pack(fill="x")

            tk.Label(header_frame, text="Coordinates", width=11, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Distance", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Troops", width=40, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Bounty/HP", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)

            for row in oases:
                map_id = row['MapID']
                coordinates = row['Coordinates']
                distance = row['Distance']
                troops = row['Troops']
                bountyVSHeath = row['Bounty/HP']

                # Maak een frame voor elke rij
                row_frame = tk.Frame(list_frame)
                row_frame.pack(fill="x")

                # Toon coördinaten
                text = f"{coordinates}"
                url = f"{travian_URL}position_details.php?mapId={map_id}"
                link = tk.Label(row_frame, text=text, fg="blue", cursor="hand2", width=11, anchor="w")
                link.pack(side="left", fill="x", padx=5, pady=2)
                link.bind("<Button-1>", lambda e, url=url: webbrowser.open(url))

                # Toon afstand
                distance_label = tk.Label(row_frame, text=distance, width=10, anchor="w")
                distance_label.pack(side="left", fill="x", padx=5, pady=2)

                # Toon troops
                if troops == "none" or bountyVSHeath == "0" or heroTraveling():
                    troops_label = tk.Label(row_frame, text=troops, width=40, anchor="w")
                    troops_label.pack(side="left", fill="x", padx=5, pady=2)
                else:
                    link = tk.Label(row_frame, text=troops, fg="blue", cursor="hand2", width=40, anchor="w")
                    link.pack(side="left", fill="x", padx=5, pady=2)
                    link.bind("<Button-1>", lambda e, c = coordinates: show_confirmation_popup(c))

                # Toon Bounty vs heath
                troops_label = tk.Label(row_frame, text=bountyVSHeath, width=10, anchor="w")
                troops_label.pack(side="left", fill="x", padx=5, pady=2)

    except FileNotFoundError:
        print("CSV file not found.")

def update_villages_gui(list_frame):
    # Verwijder alle bestaande widgets uit het list_frame
    for widget in list_frame.winfo_children():
        widget.pack_forget()

    try:
        with open("villages.csv", "r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            oases = list(reader)
            
            # Maak headers
            header_frame = tk.Frame(list_frame)
            header_frame.pack(fill="x")

            tk.Label(header_frame, text="Coordinates", width=11, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Distance", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Population", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Player", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Alliance", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)
            tk.Label(header_frame, text="Tribe", width=10, font=("Arial", 9, "bold"), anchor="w").pack(side="left", padx=5, pady=5)

            for row in oases:
                map_id = row['MapID']
                coordinates = row['Coordinates']
                distance = row['Distance']
                Population = row['Population']
                Player = row['Player']
                Alliance = row['Alliance']
                Tribe = row['Tribe']

                # Maak een frame voor elke rij
                row_frame = tk.Frame(list_frame)
                row_frame.pack(fill="x")

                # Toon coördinaten
                text = f"{coordinates}"
                url = f"{travian_URL}position_details.php?mapId={map_id}"
                link = tk.Label(row_frame, text=text, fg="blue", cursor="hand2", width=11, anchor="w")
                link.pack(side="left", fill="x", padx=5, pady=2)
                link.bind("<Button-1>", lambda e, url=url: webbrowser.open(url))

                # Toon afstand
                distance_label = tk.Label(row_frame, text=distance, width=10, anchor="w")
                distance_label.pack(side="left", fill="x", padx=5, pady=2)

                # Toon Population
                troops_label = tk.Label(row_frame, text=Population, width=10, anchor="w")
                troops_label.pack(side="left", fill="x", padx=5, pady=2)

                # Toon Player name
                troops_label = tk.Label(row_frame, text=Player, width=10, anchor="w")
                troops_label.pack(side="left", fill="x", padx=5, pady=2)

                # Toon Alliantie
                troops_label = tk.Label(row_frame, text=Alliance, width=10, anchor="w")
                troops_label.pack(side="left", fill="x", padx=5, pady=2)

                # Toon Tribe
                troops_label = tk.Label(row_frame, text=Tribe, width=10, anchor="w")
                troops_label.pack(side="left", fill="x", padx=5, pady=2)

    except FileNotFoundError:
        print("CSV file not found.")

def oasis_gui(parent):
    oasis_list_frame = tk.Frame(parent, padx=10, pady=10, borderwidth=2, relief="groove")
    oasis_list_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="ns")

    title_bar = tk.Frame(oasis_list_frame, bg="red", height=1)
    title_bar.grid(row=0, column=0, sticky="ew")
    title_label = tk.Label(title_bar, text="Oases/Villages list", bg="red", fg="white", font=("Arial", 10, "bold"), height=1)
    title_label.grid(row=0, column=0, padx=2, pady=2)

    # Maak twee frames voor Oases en Villages
    oasis_frame = tk.Frame(oasis_list_frame)
    village_frame = tk.Frame(oasis_list_frame)
    oasis_frame.grid(row=1, column=0, sticky="nsew")
    village_frame.grid(row=1, column=0, sticky="nsew")

    oasis_list_frame.grid_rowconfigure(1, weight=1)
    oasis_list_frame.grid_columnconfigure(0, weight=1)

    # Initialiseer de Oasis GUI
    update_oasis_gui(oasis_frame)
    update_villages_gui(village_frame)

    input_frame = tk.Frame(oasis_list_frame)
    input_frame.grid(row=2, column=0, sticky="ew", pady=(5, 10))

    global viewOasis
    viewOasis = False

    def switch_view():
        global viewOasis
        viewOasis = not viewOasis
        # Wissel zichtbaarheid van de frames
        if viewOasis:
            oasis_frame.tkraise()  # Breng het Oasis frame naar voren
            villageOasis_switch.config(text="Villages")
        else:
            village_frame.tkraise()  # Breng het Village frame naar voren
            villageOasis_switch.config(text="Oases")

    villageOasis_switch = tk.Button(input_frame, text="Villages", command= switch_view)
    villageOasis_switch.pack(side="left", padx=(5, 200))

    tk.Label(input_frame, text="X Offset:").pack(side="left", padx=(0, 5))
    x_offset_entry = tk.Entry(input_frame, width=5)
    x_offset_entry.pack(side="left", padx=(0, 15))

    tk.Label(input_frame, text="Y Offset:").pack(side="left", padx=(0, 5))
    y_offset_entry = tk.Entry(input_frame, width=5)
    y_offset_entry.pack(side="left", padx=(0, 15))

    # Start button to trigger the index_oasis function
    start_button = tk.Button(input_frame, text="Start Index", command=lambda: index_fields(x_offset_entry, y_offset_entry, oasis_frame, village_frame))
    start_button.pack(side="left", padx=(5, 0))

    oasis_frame.tkraise()

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

    #TODO calculate and add the amound of troops needed to keep raiding all oasis in this class
    
    tk.Label(frame, text="min sec").grid(row=3, column=0, sticky="w", padx=5)
    min_entry = tk.Entry(frame, textvariable=tk.IntVar(value=min_Time))
    min_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame, text="max sec").grid(row=4, column=0, sticky="w", padx=5)
    max_entry = tk.Entry(frame, textvariable=tk.IntVar(value=max_Time))
    max_entry.grid(row=4, column=1, padx=5, pady=5)

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

def calculate_resourcesVSheath(MapId):
    # Open de simulation battle page for this Oasis
    driver.get(f"https://ts8.x1.europe.travian.com/build.php?id=39&tt=3&screen=combatSimulator&kid={MapId}")
    time.sleep(1)

    try:
        # set all field on 0
        for i in range(1, 11):
            unit_field = driver.find_element(By.XPATH, f'//*[@id="combatSimulatorForm"]/div[2]/div[3]/div[3]/table/tbody/tr[2]/td[{i}]/input')
            driver.execute_script("arguments[0].value = '';", unit_field)
            unit_field.send_keys("0")
    except:
        print(f"Simulation fight: Troop field failure at {MapId}")
        return 0

    try:
        # Make sure checkbox hero is on
        hero_checkbox = driver.find_element(By.XPATH, '//*[@id="combatSimulatorForm"]/div[2]/div[3]/div[3]/table/tbody/tr[2]/td[11]/input')
        if not hero_checkbox.is_selected():
            hero_checkbox.click()
    except:
        print(f"Simulation fight: Cannot find state or click on hero checkbox @ {MapId}, state: {hero_checkbox.is_selected():}")
        return 0

    try:
        # start simulation by clicking on the button
        simulate_button = driver.find_element(By.XPATH, '//*[@id="simulate"]')
        simulate_button.click()
        time.sleep(2)
    except:
        print(f"Simulation fight: Simulate button failure {MapId}")
        return 0
    
    HeroSurvival = driver.find_element(By.XPATH, '//*[@id="combatSimulator"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[11]')
    if HeroSurvival.text == "−1":
        return 0

    try:
        healthLoss_field = driver.find_element(By.XPATH, '//*[@id="combatSimulator"]/div[2]/div[2]/div[3]/table/tbody/tr/td')
        healthLoss_tekst = healthLoss_field.text
        if 'might die' in healthLoss_tekst: # The hero survives with such low health that they might die in a real battle!
            heath_lost = 100
            new_health = 0 # To make bountyVSHeath 0
        else:
            parts = healthLoss_tekst.split() # 'Hero's health lowered from [initial_heath] to [new_health]'
            initial_health = int(parts[4])
            new_health = int(parts[6])
            heath_lost = initial_health - new_health
    except: # Als hero geen health schade heeft opgelopen
        heath_lost = 1

    try:
        # Check wood resource bounty
        resource_field = driver.find_element(By.XPATH, '//*[@id="combatSimulator"]/div[2]/div[4]/div[2]/div/div[1]')
        single_Resourcebounty = int(resource_field.text)
        resource_bounty = single_Resourcebounty*4 #Bounty of all four resources is always the same
    except:
        return 0

    if heath_lost == 0:
        return 0
    else:
        BountyVSheath = round(resource_bounty/heath_lost)
        return BountyVSheath

def Edit_raidList(troops_values, MapId):
    try:
        # Click on link to open edit raid list
        links = driver.find_elements(By.XPATH, '//*[@id="crud-raidlist-button"]')
        for link in links: # find correct link because ID is used more then onces
            link_tekst = driver.execute_script("return arguments[0].textContent;", link)
            if 'Edit' in link_tekst:
                link.click()
                time.sleep(0.5)
                break
        try:
            # Deactivate oasis in raid list if animals are present
            Deactivate_checkbox = driver.find_element(By.XPATH, '//*[@id="farmListTargetForm"]/div[4]/label/input')
            if Deactivate_checkbox.is_selected() == (troops_values == "none"):
                Deactivate_checkbox.click()
                time.sleep(0.5)
            try:
                # Click on Edit farm list ('type of farmlist')
                save_button = driver.find_element(By.XPATH, '//*[@id="farmListTargetForm"]/div[5]/button[3]')
                save_button.click()
                time.sleep(1)
            except:
                print(f"Edit raid list @{MapId}: save button failed")
        except:
            print(f"Edit raid list @{MapId}: deactivate checkbox failed")
    except:
        print(f"Edit raid list @{MapId}: Open edit farm list failed")

def check_oasis():
    # Open CSV file
    with open("gevonden_oases.csv", "r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        oases = list(reader)
        if len(oases) == 0:
            return

    # Check all oasises in CSV
        for row in oases:
            if row:
                map_id = row['MapID']
                old_troops = row['Troops'] # Save troops that were in oasis the last time to check if anything has changed
                url = f"{travian_URL}position_details.php?mapId={map_id}" # Open oasis URL
                driver.get(url)
                time.sleep(0.5)

                try:
                    troop_rows = driver.find_elements(By.XPATH, '//*[@id="troop_info"]/tbody/tr') # Find troop info fields and combine in list
                    troops_values = []
                    
                    for troop_row in troop_rows:
                        troop_text = troop_row.text
                        if "simulate raid" in troop_text: # As soon as 'simulate raid' has been found the troops info is over
                            break
                        troops_values.append(troop_text)
                    troops_value = ", ".join(troops_values) # If multiple types of troops are in the oasis combine these in one string           

                except Exception as e:
                    troops_value = None
                    BountyVSHeath = 0
                    print(f"Error fetching troop info: {e}")

                # Check if raid list needs to be (de-)activated, because troops have spawned or cleared
                if (old_troops == 'none') != (troops_value == 'none'): 
                    Edit_raidList(troops_value, map_id)

                # Check if the troops have changed, then the simulation neeeds to be done again, and they need to be changed in the CSV
                if old_troops != troops_value:
                        if troops_value != 'none':
                            BountyVSHeath = calculate_resourcesVSheath(map_id)
                        else:
                            BountyVSHeath = 0
                        row["Bounty/HP"] = BountyVSHeath
                        row['Troops'] = troops_value if troops_value else "No data"

        with open("gevonden_oases.csv", "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=oases[0].keys())
            writer.writeheader()
            writer.writerows(oases)
            
    print("Oasis updated")

def check_Oasis_after(root):
    check_oasis()

    timeUntillNextCheck = random.randint(480000, 600000) # Randomly select a time to update oasis to make it more human-like
    root.after(timeUntillNextCheck, check_Oasis_after, root)

def main():     
    initialise() 
    login(username, password)
    check_oasis()

    root = setup_gui()
    root.after(1000, Auto_raidList, root)
    root.after(600000, check_Oasis_after, root)
    root.mainloop()

if __name__ == "__main__":
    main()
