import json 
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
#import Tables_are_fun
from Tables_are_fun import insert_person
#Projects/Abomination/Natalie/Tables_are_fun.py
players_data = []
gender = 0      # 0->male, 1->female
page = 2
max_page = 10

def players(gender=0, page=1):
    print('looking for player')
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, necessary for certain environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Set a user-agent
    count_page = 0
    url = f'https://www.fifaindex.com/players/?page={page}&gender={gender}&order=desc' #male
    
    driver = webdriver.Chrome(options=chrome_options)  # or use 'webdriver.Firefox()' for Firefox
    driver.get(url)
    try:
        time.sleep(2)
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-players"))
        )
    except Exception as e:
        print('break - No table')
        driver.quit()
        return 'No_table'
    time.sleep(2)
    # Wait for the page to fully load (you can add explicit waits if needed)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the browser
    driver.quit()

    # Now try finding the table
    table = soup.find('table', {'class': 'table table-striped table-players'})
    #print(table)
    if not table:
        print('break - No table-player')
        return 'No_table'
    #if page > 70: break
    else:
        print('table')
        rows = table.find_all('tr', {'data-playerid': True})
        team_list = []
        for row in rows:
            print('row')
            if gender == 0: player_gender = 'Male'
            if gender == 1: player_gender = 'Female'
            else: player_gender = ''
            nationality = row.find('td', {'data-title': 'Nationality'}).find('a').get('title')
            ovr_pot = row.find('td', {'data-title': 'OVR / POT'}).find_all('span')
            ovr = ovr_pot[0].text
            pot = ovr_pot[1].text
            name = row.find('td', {'data-title': 'Name'}).find('a').text
            positions = [pos.text for pos in row.find('td', {'data-title': 'Preferred Positions'}).find_all('span')]
            
            pos = ''
            for n in positions:
                pos += n+ ' ' 
            age = row.find('td', {'data-title': 'Age'}).text
            team = row.find('td', {'data-title': 'Team'}).find('a').get('title').replace(' FIFA 24','')
            team_list.append(team)
            # Convert the list of positions to a JSON-formatted string
            json_positions = json.dumps(positions)
            
            insert_person([name, age, team,  nationality, json_positions])   # insering date on DataBase ----------------------------------------------------####
            
            # players_data.append([name, player_gender,  nationality, ovr, pot, positions, int(age), team])
            print(gender, page, name, age, team,  nationality, json_positions)
        #page += 1
        time.sleep(2)
        return team_list
        #if count_page>=max_page: break
        #count_page += 1
        
# for player in players_data:
#     print(player)

