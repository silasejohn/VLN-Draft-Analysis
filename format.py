import sys
import pandas as pd

# open spreadsheet as pandas df
df = pd.read_csv('data.csv')
headers = df.columns.tolist()
print(f'Headers: {headers}')

# print each header, with first 5 values from each column
for header in headers:
    print(f'{header}: \n{df[header].head()}')
    print('\n')
