import os
import pandas as pd
import requests

def download_historical_data(start_year: int = 2022, end_year: int = 2026) -> pd.DataFrame:
    """Downloads and stacks multiple years of tennis data from Github."""
    os.makedirs("data/raw", exist_ok=True)
    all_years = []
    
    for year in range(start_year, end_year + 1):
        file_path = f"data/raw/atp_matches_{year}.csv"
        url = f"https://githubusercontent.com_{year}.csv"
        
        if not os.path.exists(file_path):
            print(f"Downloading {year} data...")
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                else:
                    print(f"Skipping {year}: File not found online yet.")
                    continue
            except Exception as e:
                print(f"Error downloading {year}: {e}")
                continue
                
        df = pd.read_csv(file_path)
        all_years.append(df)
        print(f"Loaded {year} data. Shape: {df.shape}")
        
    combined_df = pd.concat(all_years, ignore_index=True)
    print(f"\nTotal Multi-Year Dataset Shape: {combined_df.shape}")
    return combined_df

if __name__ == "__main__":
    download_historical_data()
