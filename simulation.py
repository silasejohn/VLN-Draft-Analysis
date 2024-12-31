import sys
import json
import pandas as pd
import utility as util

# open spreadsheet as pandas df
df = pd.read_csv('data/updated_data.csv')
headers = df.columns.tolist()

# access new header names (json) in config folder
with open('config/new_headers.json', 'r') as file:
    new_headers = json.load(file)["new_headers"]

# add new 4 values to new_headers for new spreadsheet values
new_headers += ['', 'primary_consideration', 'secondary_consideration', 'notes']

# create new df using the new headers
df.columns = new_headers

"""
Cheese (Top)        ... mrlizwiz
Earthen (Top)       ... earthen
VLN (top lane)      ... verylastnerve
Vowels (top lane)   ... .f_g.

Hello Kitty!@ (Jungle i think)  ... recoveringschizo
Lakuna (Jungle)                 ... _lakuna
acekiller1107 (Jungle)          ... axekiller1107

Morgana, My Beloved (Mid)   ... catinatin
Lapiz Lazuli (Mid)          ... lapislazuli3824
NAQI (Mid)                  ... ffsfruit

Different (ADC)     ... different_lol
Stran (ADC)         ... .stran
Team Curse (ADC)    ... aratthe
Peepa (ADC)         ... jayrich1101
Stl Slayer (ADC)    ... stl_slayer_24

DavidEdge (Support) ... davidedge
"""

### create new simulation for draft
captains = ['DavidEdge', 
            'different_lol', 
            'recoveringschizo', 
            '_lakuna', 
            'jayrich1101', 
            '.f_g.', 
            'catinatin', 
            'acekiller1107',
            'Earthen',
            'Lapislazuli3824',
            'ffsfruit',
            'Stl_Slayer_24',
            'Stran',
            'VeryLastNerve',
            'mrlizwiz',
            'aratthe']

# remove 'opgg_link', 'peak_rank_explanation', 'availability', 'interest_in_captain', 'reference_to_vln_league', 'playstyle_description', 'join_discord_flag' columns and corresponding headers
new_df = df.drop(columns=['opgg_link', 'peak_rank_explanation', 'availability', 'interest_in_captain', 'reference_to_vln_league', 'playstyle_description', 'join_discord_flag', 'primary_consideration', 'secondary_consideration', 'notes', 'is_peak_rank_true_rank', 'champion_identity', 'secondary_role_skill_level', ''])

# print all unique 'discord_username' values
print(new_df['discord_username'].unique())

# create new df with only rows of captains that are in 'discord_username' column ... 'cap_df'
cap_df = pd.DataFrame(columns=new_df.columns)
for captain in captains:
    cap_df = pd.concat([cap_df, new_df[new_df['discord_username'] == captain]], ignore_index=True)
# print(df)

# create a df with no captain in it 'draft_df'
df = pd.read_csv('data/updated_data.csv')
headers = df.columns.tolist()
df.columns = new_headers
draft_df = df.drop(columns=['opgg_link', 'peak_rank_explanation', 'availability', 'interest_in_captain', 'reference_to_vln_league', 'playstyle_description', 'join_discord_flag', 'primary_consideration', 'secondary_consideration', 'notes', 'is_peak_rank_true_rank', 'champion_identity', 'secondary_role_skill_level', ''])
draft_df = draft_df[~draft_df['discord_username'].isin(captains)]
# print(draft_df)

# run a simulation
from collections import defaultdict

MAX_PLAYERS_PER_TEAM = 8
RANK_OPTIONS = [
    'Iron 1-4', 'Bronze 1-4', 'Silver 1-4', 'Gold 1-4', 'Platinum 1-4',
    'Emerald 4', 'Emerald 3', 'Emerald 2', 'Emerald 1',
    'Diamond 4', 'Diamond 3', 'Diamond 2', 'Diamond 1',
    'Master', 'Grandmaster']
ROLES = ['ADC', 'Mid', 'Jungle', 'Support', 'Top']

# cap_df is the cap df... important headers 'discord_username', 'primary_role', 'secondary_role', 'peak_rank_2024_split3'
# draft_df is the draft df... important headers 'discord_username', 'primary_role', 'secondary_role', 'peak_rank_2024_split3'

rank_order = {rank: i for i, rank in enumerate(RANK_OPTIONS)}
def get_rank(player_rank):
    return rank_order[player_rank]

# cap_df['rank_value'] = cap_df['peak_rank_2024_split3'].apply(get_rank)
# draft_df['rank_value'] = draft_df['peak_rank_2024_split3'].apply(get_rank)
cap_df['rank_value'] = cap_df['peak_rank_2024_split3'].apply(lambda r: RANK_OPTIONS.index(r))
draft_df['rank_value'] = draft_df['peak_rank_2024_split3'].apply(lambda r: RANK_OPTIONS.index(r))
pladraft_dfyers = draft_df.sort_values(by='rank_value', ascending=False).reset_index(drop=True)

# sort caps by rank first
cap_df = cap_df.sort_values(by=['rank_value'], ascending=True)

# print(cap_df)
# sys.exit()

# init a potential draft dictionary
draft_results = defaultdict(list)

# simulate the snake draft
snake_order = list(range(len(cap_df))) + list(range(len(cap_df) - 1, -1, -1))
captains = cap_df.to_dict('records')
players_pool = draft_df.copy()

# export player draft pool and cap draft pool in pretty print to a text file
# every 16 players, draw a line
line_idx = 0
player_idx = 1
with open('data/player_draft_pool.txt', 'w') as file:
    file.write("=== Player Draft Pool ===\n")
    # sort by rank
    players_pool = players_pool.sort_values(by=['rank_value'], ascending=False)
    for index, row in players_pool.iterrows():
        file.write(f"[{player_idx}] {row['discord_username']} - {row['peak_rank_2024_split3']} ({row['primary_role']})\n")
        if player_idx % 16 == 0:
            file.write(f"--- END DRAFT PERIOD {line_idx + 1} ---\n")
            line_idx += 1
        player_idx += 1

cap_idx = 1
with open('data/cap_draft_pool.txt', 'w') as file:
    file.write("=== Captain Draft Pool ===\n")
    for index, row in cap_df.iterrows():
        file.write(f"[{cap_idx}] {row['discord_username']} - {row['peak_rank_2024_split3']} ({row['primary_role']})\n")
        cap_idx += 1

for round_num in range(MAX_PLAYERS_PER_TEAM):
    print(f"\n=== Round {round_num + 1} ===")
    for cap_idx in snake_order:
        captain = captains[cap_idx]
        captain_id = captain['discord_username']

        # if cap alr has MAX_PLAYERS_PER_TEAM then go next
        if len(draft_results[captain_id]) >= MAX_PLAYERS_PER_TEAM:
            continue

        # determine a needed role 
        drafted_roles = [player['primary_role'] for player in draft_results[captain_id]]
        needed_roles = [role for role in ROLES if role not in drafted_roles]

        # prio needed roles 
        if needed_roles:
            eligible_player = players_pool[players_pool['primary_role'].isin(needed_roles)]
        else:
            eligible_player = players_pool

        # sort by rank
        eligible_player = eligible_player.sort_values(by=['rank_value'], ascending=False)

        if eligible_player.empty:
            print(f"{util.RED}Captain [{captain_id}] cannot pick. No eligible players left!{util.RESET}")
            continue

        # how to handle ties
        top_rank_value = eligible_player.iloc[0]['rank_value']
        top_candidates = eligible_player[eligible_player['rank_value'] == top_rank_value]

        if len(top_candidates) > 1:
            print(f"{util.YELLOW}Tie for Captain [{captain_id}]: {top_candidates[['discord_username', 'primary_role']].to_dict('records')}")
            # choice = input("Enter user_id of the player to pick: ")
            # if choice not in top_candidates['discord_username'].values:
            #     print("Invalid choice! Defaulting to the first available player.")
            selected_player = top_candidates.iloc[0]
            # else:
            # selected_player = top_candidates[top_candidates['discord_username'] == choice].iloc[0]
        else:
            selected_player = top_candidates.iloc[0]

        # add player to captains draft and remove from pool
        draft_results[captain_id].append(selected_player.to_dict())
        players_pool = players_pool[players_pool['discord_username'] != selected_player['discord_username']]
        print (f"{util.GREEN}Captain [{captain_id}] picked [{selected_player['discord_username']}] ({selected_player['primary_role']})!{util.RESET}")

# pretty print the results
print("\n=== Final Draft Results ===")
for captain_id, team in draft_results.items():
    print(f"\n{util.CYAN}Captain [{captain_id}] Team:")
    for player in team:
        print(f"{player['discord_username']} - {player['peak_rank_2024_split3']} ({player['primary_role']})")

# output pretty print results into a .txt file in /data 
with open('data/draft_results.txt', 'w') as file:
    file.write("=== Final Draft Results ===\n")
    for captain_id, team in draft_results.items():
        file.write(f"\nCaptain [{captain_id}] Team:\n")        
        for player in team:
            file.write(f"{player['discord_username']} - {player['peak_rank_2024_split3']} ({player['primary_role']})\n")
