import sys
import json
import pandas as pd
import utility as util

# open spreadsheet as pandas df
df = pd.read_csv('data/data.csv')
headers = df.columns.tolist()
print(f'Headers: {headers}')

# print each header, with first 5 values from each column
for header in headers:
    print(f'{header}: \n{df[header].head()}')
    print('\n')

# access new header names (json) in config folder
with open('config/new_headers.json', 'r') as file:
    new_headers = json.load(file)["new_headers"]
    print(new_headers)

# access list of champions (json) in config folder
with open('config/champs.json', 'r') as file:
    json_data = json.load(file)
    champions = json_data["champions"]
    champ_corrections = json_data["champ_corrections"]
    print(champions)

# create new df using the new headers
new_df = pd.read_csv('data/data.csv')
new_df.columns = new_headers

# print each header, with first 5 values from each column
for header in new_headers:
    print(f'{header}: \n{new_df[header].head()}')
    print('\n')

# in new df, every instance of '\n' replace with '\t'
new_df = new_df.replace('\n', '\t', regex=True)

# export new df into new csv file in data folder
util.export_df_to_csv(new_df, '01_cleaned_data.csv')

# for the header "top_3_champs", split the string into a list of strings by ',' or ' ' or "/"
new_df['top_3_champs'] = new_df['top_3_champs'].apply(lambda x: x.split(',') if ',' in x else x.split(' ') if ' ' in x else x.split('/'))

# get rid of whitespace in the beginning and end of each string in the list
new_df['top_3_champs'] = new_df['top_3_champs'].apply(lambda x: [champ.strip() for champ in x])

# format each champ name to be first letter capitlized, rest lowercase
new_df['top_3_champs'] = new_df['top_3_champs'].apply(lambda x: [champ.capitalize() for champ in x])

# if a champ is not in the list of champions, print "champ" name and discord_username
for index, row in new_df.iterrows():
    for champ_name in row['top_3_champs']:
        # print(f'Addressing champ_name: {champ_name}')
        champion_addressed = False
        if champ_name not in champions:
            if not champion_addressed:
                # champ_corrections is a list of tuples, where the first element is the incorrect champ name, and the second element is the correct champ name
                # if champ_name is in "incorrect" champ_corrections, replace it with the "correct" champ name
                for naming_pair in champ_corrections:
                    if champ_name == naming_pair["incorrect"]:
                        champ_name = naming_pair["correct"]
                        print(f'{util.GREEN}[Champion Corrected] {naming_pair["incorrect"]} -> {naming_pair["correct"]} {util.RESET}')
                        champion_addressed = True
                        # replace the incorrect champ name with the correct champ name in the df
                        new_df.at[index, 'top_3_champs'] = [champ_name if champ == naming_pair["incorrect"] else champ for champ in row['top_3_champs']]
                        break
                if not champion_addressed:
                    print(f'{util.RED}[Champion Not In list] {champ_name} - {row["discord_username"]}{util.RESET}')
                    champion_addressed = True

# add 3 columns (top_champ, second_champ, third_champ) to the df for of the top 3 champions
new_df['top_champ'] = new_df['top_3_champs'].apply(lambda x: x[0])
new_df['second_champ'] = new_df['top_3_champs'].apply(lambda x: x[1] if len(x) > 1 else None)
new_df['third_champ'] = new_df['top_3_champs'].apply(lambda x: x[2] if len(x) > 2 else None)

# print list of unique champions from 'top_3_champs', sort alphabetically
champions = set()
new_df['top_3_champs'].apply(lambda x: [champions.add(champ) for champ in x])
print(f'Champions: {sorted(champions)}')



# delete col with 'join_discord_flag', 'champion_identity', 'peak_rank_explanation', 'reference_to_vln_league', 'playstyle_description'
new_df = new_df.drop(columns=['join_discord_flag', 'champion_identity', 'peak_rank_explanation', 'reference_to_vln_league', 'playstyle_description'])

# export df into new csv file in data folders
util.export_df_to_csv(new_df, '02_formatted_data.csv')ls