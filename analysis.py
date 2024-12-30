import sys
import json
import pandas as pd
import utility as util

# open spreadsheet as pandas df
df = pd.read_csv('data/updated_data.csv')
headers = df.columns.tolist()
print(f'Headers: {headers}')

# access new header names (json) in config folder
with open('config/new_headers.json', 'r') as file:
    new_headers = json.load(file)["new_headers"]

# add new 4 values to new_headers for new spreadsheet values
new_headers += ['', 'primary_consideration', 'secondary_consideration', 'notes']

# create new df using the new headers
df.columns = new_headers

# in 'primary_role' column, how many of each value?
print(df['primary_role'].value_counts())

rank_options = ['Iron 1-4', 'Silver 1-4', 'Gold 1-4', 'Platinum 1-4', 'Emerald 4', 'Emerald 3', 'Emerald 2', 'Emerald 1', 'Diamond 4', 'Diamond 3', 'Diamond 2', 'Diamond 1', 'Master', 'Grandmaster', 'Challenger']

# for each value_count, bucket emerald 4, emerald 3, emerald 2, emerald 1 into emerald
df['peak_rank_2024_split3'] = df['peak_rank_2024_split3'].apply(lambda x: 'Emerald 1-4' if x in ['Emerald 4', 'Emerald 3', 'Emerald 2', 'Emerald 1'] else x)
df['peak_rank_2024_split3'] = df['peak_rank_2024_split3'].apply(lambda x: 'Diamond 1-4' if x in ['Diamond 4', 'Diamond 3', 'Diamond 2', 'Diamond 1'] else x)

print (df['peak_rank_2024_split3'].value_counts())