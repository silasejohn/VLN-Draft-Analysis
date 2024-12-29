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