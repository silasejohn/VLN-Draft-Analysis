import sys
import json
import pandas as pd

# open spreadsheet as pandas df
df = pd.read_csv('data/data.csv')
headers = df.columns.tolist()
print(f'Headers: {headers}')

# print each header, with first 5 values from each column
for header in headers:
    print(f'{header}: \n{df[header].head()}')
    print('\n')

# access json data in config folder
with open('config/new_headers.json', 'r') as file:
    new_headers = json.load(file)["new_headers"]
    print(new_headers)

# create new df using the new headers
new_df = pd.read_csv('data/data.csv')
new_df.columns = new_headers

# print each header, with first 5 values from each column
for header in new_headers:
    print(f'{header}: \n{new_df[header].head()}')
    print('\n')

# in new df, every instance of '\n' replace with '\t'
new_df = new_df.replace('\n', '\t', regex=True)

# for the header "top_3_champs", split the string into a list of strings by ',' or ' ' or "/"
new_df['top_3_champs'] = new_df['top_3_champs'].apply(lambda x: x.split(',') if ',' in x else x.split(' ') if ' ' in x else x.split('/'))

# get rid of whitespace in the beginning and end of each string in the list
new_df['top_3_champs'] = new_df['top_3_champs'].apply(lambda x: [champ.strip() for champ in x])

# print list of unique champions from 'top_3_champs', sort alphabetically
champions = set()
new_df['top_3_champs'].apply(lambda x: [champions.add(champ) for champ in x])
print(f'Champions: {sorted(champions)}')

# export df into new csv file in data folders
new_df.to_csv('data/formatted_data.csv', index=False)