import pandas as pd
import requests
import os

# Define the URL
url = 'https://www.espncricinfo.com/records/year/team-lowest-innings-totals/2024-2024/test-matches-1'

# Define headers with a user-agent as a dictionary
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# Define the folder path where you want to save the files
folder_path = "V:/Projects/Python Projects/Web Scraping/ExtractedTables/"

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Fetch the content using requests
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Read tables from the response content
    dfs = pd.read_html(response.content)
    
    print(f"Number of tables found: {len(dfs)}")

    # Save each table to a file in the specified folder
    for i, df in enumerate(dfs):
        # Save as CSV
        df.to_csv(os.path.join(folder_path, f'table_{i+1}.csv'), index=False)
        
        # Save as Excel
        df.to_excel(os.path.join(folder_path, f'table_{i+1}.xlsx'), index=False)
        
        # Save as JSON
        df.to_json(os.path.join(folder_path, f'table_{i+1}.json'), orient='records')
        
        print(f"Table {i+1} saved as 'table_{i+1}.csv', 'table_{i+1}.xlsx', and 'table_{i+1}.json'")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
