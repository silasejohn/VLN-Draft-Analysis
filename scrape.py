from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException

import time
from bs4 import BeautifulSoup
from random import randint
import json
import utility as util

# summ region
# multi.gg op.gg or IGN
# info on recent champs in last month
# info on friends recently played with
# https://www.op.gg/summoners/na/dont%20ever%20stop-NA1

MAIN_WEBSITE = "https://www.op.gg/"

RANKING_SYSTEM = {
    "Iron 4": 1,
    "Iron 3": 2,
    "Iron 2": 3,
    "Iron 1": 4,
    "Bronze 4": 5,
    "Bronze 3": 6,
    "Bronze 2": 7,
    "Bronze 1": 8,
    "Silver 4": 9,
    "Silver 3": 10,
    "Silver 2": 11,
    "Silver 1": 12,
    "Gold 4": 13,
    "Gold 3": 14,
    "Gold 2": 15,
    "Gold 1": 16,
    "Platinum 4": 17,
    "Platinum 3": 18,
    "Platinum 2": 19,
    "Platinum 1": 20,
    "Emerald 4": 21,
    "Emerald 3": 22,
    "Emerald 2": 23,
    "Emerald 1": 24,
    "Diamond 4": 25,
    "Diamond 3": 26,
    "Diamond 2": 27,
    "Diamond 1": 28,
    "Master": 29,
    "Grandmaster": 30,
    "Challenger": 31
}

# Function to wait for an element to load on the page
def wait_for_element_to_load(driver, by, value, timeout=10, custom_error_msg=None):
    """Wait until the element is found or the timeout expires."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        if custom_error_msg:
            print(f"{util.RED}{custom_error_msg}{util.RESET}")
        else:
            print(f"{util.RED}{value} Element not Found!{util.RESET}")
        return None
    
# Logic to "Expand" match history on OP.GG
def expand_champ_history(driver):
    
    retrievedLast30DaysMatchHistory = False
    match_history_extention_attempts = 0

    while not retrievedLast30DaysMatchHistory:
        print(f"{util.YELLOW}\nAttempt {match_history_extention_attempts} to Expand Match History...{util.RESET}")

        # Locating the Expand Match History Button
        more_match_history_button = None # Initialize to None
        while more_match_history_button is None: # Loop until button is found
            # find all buttons of type "more" for data expansion
            find_more_type_buttons = driver.find_elements(By.CLASS_NAME, 'more')

            for button in find_more_type_buttons:
                # print(button.text)
                if "Show more" == button.text:
                    more_match_history_button = button
            
            time.sleep(0.5)  # Sleep Buffer before retrying

        # find the main game history container
        history_container = driver.find_element(By.XPATH, "//*[contains(@class, 'css-fkbae7') and contains(@class, 'er95z9k0')]")
        
        # find the match history container
        match_history_container = history_container.find_element(By.XPATH, "//*[contains(@class, 'css-1jxewmm') and contains(@class, 'ek41ybw0')]")
        
        # find the last child element of the match history container
        oldest_match = match_history_container.find_element(By.XPATH, "child::*[last()]")

        # find the only child element of the oldest match
        oldest_match_link = oldest_match.find_element(By.XPATH, "child::*")

        # find the child element of CLASS_NAME = "content"
        oldest_match_content = oldest_match_link.find_element(By.CLASS_NAME, "contents")

        # find the child element of CLASS_NAME = "inner"
        oldest_match_inner = oldest_match_content.find_element(By.CLASS_NAME, "inner")

        # find the child element which has multiple classes (css-1mk3mai,ery81n92)
        oldest_match_link = oldest_match_inner.find_element(By.XPATH, "child::*[contains(@class, 'css-1mk3mai') and contains(@class, 'ery81n92')]")

        # find the child element of CLASS_NAME = "head-group"
        oldest_match_head_group = oldest_match_link.find_element(By.CLASS_NAME, "head-group")

        # find the child element of CLASS_NAME = "time-stamp"
        oldest_match_time_stamp = oldest_match_head_group.find_element(By.CLASS_NAME, "time-stamp")

        # text box on when last match was played in format of "11 days ago"
        oldest_match_text = oldest_match_time_stamp.text

        # identify text in the time-stamp of the oldest match displayed
        print(f"{util.YELLOW}Oldest Match: {oldest_match_text}{util.RESET}")

        # extract number of days from the text
        if "days" in oldest_match_text:
            days = int(oldest_match_text.split(" ")[0])
            print(f"{util.GREEN}Currently displaying match history from the last {days} days!{util.RESET}")
            more_match_history_button.click()
            match_history_extention_attempts += 1
            print(f"{util.YELLOW}Expanding Match History...{util.RESET}")
        elif "month" in oldest_match_text: 
            # if the oldest match is from a month ago, then we have the last 30 days of match history
            retrievedLast30DaysMatchHistory = True
            break

    print(f"{util.GREEN}Match History Expanded to >>> 30 days!{util.RESET}")

# Logic to "Update" summoner profile / data
def update_summoner_profile(driver):
    try:
        # Get the last update field and print it
        last_update_field = driver.find_element(By.CLASS_NAME, 'last-update')
        content = last_update_field.text

        # Check if the last update field contains "Last Updated: "
        if "Last updated: " in content:
            print(f"{util.RED}{content}{util.RESET}")

            try: # try finding the update button on the screen + click it

                # BUTTON STATES: IDLE, REQUEST, DISABLE
                update_button = driver.find_element(By.XPATH, "//*[contains(@class, 'IDLE') and contains(@class, 'css-1ki6o6m') and contains(@class, 'e17xj3f90')]")
                update_button.click()

                # wait for "update" to register
                print(f"{util.YELLOW}Updating...{util.RESET}")
                wait_for_element_to_load(driver, By.XPATH, "//*[contains(@class, 'DISABLE') and contains(@class, 'css-1r09es5') and contains(@class, 'e17xj3f90')]")
                print(f"{util.GREEN}Update Complete!{util.RESET}")

            except Exception as e:
                print(f"{util.RED}ERROR w/ Update Button Press{util.RESET}")

            # Get the updated last update field and print it
            last_update_field = driver.find_element(By.CLASS_NAME, 'last-update')
            print(f"{util.YELLOW}Next Update {last_update_field.text}{util.RESET}")

        else: # updated within the last 2 minutes
            print(f"{util.YELLOW}Next Update {content}..{util.RESET}")
    except Exception as e:
        print(f"{util.RED}Last-Update field not found: {e}{util.RESET}")

def identify_summoner_ign(driver):
    # find h1 element with 2 class attributes (css-12ijbdy,e1swkqyq0) 
    summoner_ign_header = driver.find_element(By.XPATH, "//*[contains(@class, 'css-12ijbdy') and contains(@class, 'e1swkqyq0')]")
    summoner_ign = summoner_ign_header.text
    summoner_ign = summoner_ign.replace("\n", "")
    print(f"{util.GREEN}Summoner IGN: {summoner_ign}{util.RESET}")

def identify_rank_info(driver):
    # create a dictionary to store keys (season|rank) to score (1-31)
    rank_info = {}

    # find the rank info container
    rank_info_container = driver.find_element(By.XPATH, "//*[contains(@class, 'css-1wk31w7') and contains(@class, 'eaj0zte0')]")
    
    # extract current rank
    current_rank_container = rank_info_container.find_element(By.CLASS_NAME, "content")

    current_rank_info = current_rank_container.find_element(By.CLASS_NAME, "info")
    current_tier = current_rank_info.find_element(By.CLASS_NAME, "tier")
    current_lp = current_rank_info.find_element(By.CLASS_NAME, "lp")
    print(f"{util.GREEN}Current Rank: {current_tier.text} + {current_lp.text}{util.RESET}")

    current_win_loss_info = current_rank_container.find_element(By.CLASS_NAME, "win-lose-container")
    wins_and_losses = current_win_loss_info.find_element(By.CLASS_NAME, "win-lose")
    win_ratio = current_win_loss_info.find_element(By.CLASS_NAME, "ratio")
    win_ratio_text = (win_ratio.text).replace("Win rate ", "")
    print(f"{util.GREEN}Win-Loss: {wins_and_losses.text} ({win_ratio_text}){util.RESET}")

    # use the ranking system to score the current rank
    # replace " LP" with empty string and convert to integer
    lp_as_int = int(current_lp.text.replace(" LP", ""))
    rank_score = RANKING_SYSTEM[current_tier.text] + (lp_as_int*.01)
    rank_info["current_season_rank"] = {"tier": current_tier.text, "lp": current_lp.text, "rank_score": rank_score}

    peak_rank_container = rank_info_container.find_element(By.XPATH, "//*[contains(@class, 'css-p09zgi') and contains(@class, 'e1xo3xwn0')]")
    peak_rank_info = peak_rank_container.find_element(By.CLASS_NAME, "info")
    peak_tier = peak_rank_info.find_element(By.CLASS_NAME, "tier")
    peak_lp = peak_rank_info.find_element(By.CLASS_NAME, "lp")
    print(f"{util.CYAN}Current Season Peak Rank: {peak_tier.text} + {peak_lp.text}{util.RESET}")

    # use the ranking system to score the peak rank
    lp_as_int = int(peak_lp.text.replace(" LP", ""))
    rank_score = RANKING_SYSTEM[peak_tier.text] + (lp_as_int*.01)
    rank_info["current_season_peak"] = {"tier": peak_tier.text, "lp": peak_lp.text, "rank_score": rank_score}

    # find the prior ranks container
    prior_ranks_container = rank_info_container.find_element(By.XPATH, "//*[contains(@class, 'css-xm62d3') and contains(@class, 'e1l3ivmk0')]")
   
    # find the first child element of prior ranks container
    prior_ranks_table = prior_ranks_container.find_element(By.XPATH, "child::*")
    
    # find the last child element of the match history container
    prior_ranks_table_body = prior_ranks_table.find_element(By.XPATH, "child::*[last()]")

    # export all the <tr> rows 
    prior_ranks_table_rows = prior_ranks_table_body.find_elements(By.TAG_NAME, "tr")

    # for each row, extract the rank information
    for row in prior_ranks_table_rows:
        # there are 3 <td> elements in each row
        rank_table_data = row.find_elements(By.TAG_NAME, "td")
        season = rank_table_data[0].text
        tier = rank_table_data[1].text
        lp = rank_table_data[2].text
        print(f"{util.CYAN}Season: {season} Rank: {tier} + {lp}{util.RESET}")

        # use the ranking system to score the peak rank
        lp_as_int = int(lp.replace(" LP", ""))
        rank_score = RANKING_SYSTEM[tier] + (lp_as_int*.01)
        # print(f"{util.CYAN}Rank Score: {rank_score}{util.RESET}")
        rank_idx = f"{season}"
        rank_info[rank_idx] = {"tier": tier, "lp": lp, "rank_score": rank_score}
        

    # sort rank_score in descending order to identify top 3 ranks in the prior ranks
    sorted_rank_info = sorted(rank_info.items(), key=lambda x: x[1]["rank_score"], reverse=True)

    # only keep top 3 ranks 
    sorted_rank_info = sorted_rank_info[:3]
    
    # pretty print output of the sorted rank info
    print("\nHighest Ranks:")
    for rank in sorted_rank_info:            
        print(f"{util.CYAN}[Season] {rank[0]} - [Rank] {rank[1]['tier']} {rank[1]['lp']}{util.RESET}")


class SearchEngine:
    @staticmethod
    def get_driver(browser="chrome"):
        """Sets up and returns the WebDriver (Firefox or Chrome)."""
        
        if browser.lower() == "firefox":
            options = FirefoxOptions()
            options.headless = True  # Runs in headless mode, no UI.
            service = Service('/path/to/geckodriver')  # Path to geckodriver
            driver = webdriver.Firefox(service=service, options=options)
        elif browser.lower() == "chrome":
            options = ChromeOptions()
            options.headless = True  # Runs in headless mode, no UI.
            service = ChromeService('/opt/homebrew/bin/chromedriver')  # Path to chromedriver
            driver = webdriver.Chrome(service=service, options=options)
        else:
            raise ValueError("Only 'firefox' and 'chrome' browsers are supported.")

        return driver

    @staticmethod
    def search(query, browser="chrome", isExistingLink=False, sleep=True):
        """Parses through multiple op.gg subpages"""
        if sleep:
            time.sleep(randint(10, 100))  # Random sleep

        driver = SearchEngine.get_driver(browser)  # Initialize WebDriver

        # depending on if given a query link or query IGN
        if isExistingLink: 
            search_url = query # Go to OP.GG search page and perform summoner search
            driver.get(search_url)
        else:
            IGN = query
            search_url = MAIN_WEBSITE # use existing URL
            driver.get(search_url)

            # Find the op.gg search box
            search_box = driver.find_element(By.NAME, 'search')

            # enter the summoner IGN + enter
            search_box.send_keys(IGN + Keys.RETURN)  # Send query and hit Enter

            # Wait for the search results to load, via the top-tier class
            wait_for_element_to_load(driver, By.CLASS_NAME, 'top-tier')

        # Update the summoner profile
        update_summoner_profile(driver)
        time.sleep(0.5)  # Random sleep

        # Expand the match history
        expand_champ_history(driver)
        time.sleep(0.5)  # Random sleep

        # Identify the summoner IGN
        summoner_ign = identify_summoner_ign(driver)
        time.sleep(0.5)  # Random sleep

        # Identify current season peak rank
        identify_rank_info(driver)
        time.sleep(0.5)  # Random sleep

        time.sleep(20)

        # Snapshot 1: Main Page
        # once the match history is expanded, take a snapshot of the main page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Snapshot 2: champion history / picks

        # store HTML in a file 
        with open(f"data/test.html", "w") as file:
            file.write(str(soup))

         # Scrape the search result links
        new_results = SearchEngine.scrape_search_result(soup)

        driver.quit()  # Close the browser
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        """Scrapes search result links from OP.GG results page."""
        raw_results = soup.find_all('a', class_='result__a')
        results = []

        # Implement a check to get only 10 results and avoid duplicated URLs
        for result in raw_results:
            link = result.get('href')

            # Ensure URL is valid and not duplicated
            if link and link not in results:
                results.append(link)

            # Stop after collecting 10 results
            if len(results) == 10:
                break

        return results
        # return soup


#############Driver code############
query_results = {}  # Store search results for each query
counter = 1

# with open("100QueriesSet1.txt", "r") as file:
#     for line in file:
        # query = line.strip()
# query = "op.gg"


summoner_ign_example = "dont ever stop #NA1"
link_example = "https://www.op.gg/summoners/na/dont%20ever%20stop-NA1"

query = summoner_ign_example

if "op.gg" in query:
    isLinkInput = True
else:
    isLinkInput = False

# Option 5: single NA IGN

# could just be op.gg/summoners/search ... region=na
# Option 1: single NA op.gg/summoners/na
# Option 2: single EUW op.gg/summoners/euw
# Option 3: single multisearch op.gg/multisearch/na
# OPTION 5: single multisearch op.gg/multisearch/euw
# Option 4: list of NA IGNs comma-separated
# Option 6: list of NA op.gg/summoners/na semi--separated

# exceptions 
# Option 7: single leagueofgraphs for euw ... ignore
# OPTION: u.gg profile??? 
# Option 8: single NA IGN (need to append #NA1)...  Mrionzo10
# replace CARPETBOMBCORKI - https://www.op.gg/summoners/na/CARPETBOMBCORKI-NA1

# handle no ranked history (https://www.op.gg/summoners/na/YeetYoteJungle-NAJng)

# Perform the search
print(f"Query {counter}: {query}")
search_results = SearchEngine.search(query, browser="chrome", isExistingLink=isLinkInput, sleep=False)
query_results[query] = search_results
print(f"Search results: {search_results}")
counter += 1

# Write the dictionary to a JSON file
with open("data/search_results.json", "w") as json_file:
    json.dump(query_results, json_file, indent=2)

####################################