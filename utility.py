import pandas as pd

# ANSI escape codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'  # Reset to default color

def export_df_to_csv(df, file_name):
    df.to_csv(f'data/{file_name}', index=False)
    print(f'{GREEN}[CSV Exported] {file_name}{RESET}')

def pretty_print(msg, color):
    print(f'{color}{msg}{RESET}')

# take in a df, and a list of headers and values per header
# if the value is in that header col, then add entire row to a new df
# output and print a new df
def filter_df(df, headers, values):
    new_df = pd.DataFrame(columns=df.columns)
    for header, value in zip(headers, values):
        new_df = new_df.append(df[df[header] == value], ignore_index=True)
    return new_df