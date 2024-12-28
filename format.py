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

# export df into new csv file in data folders
new_df.to_csv('data/formatted_data.csv', index=False)