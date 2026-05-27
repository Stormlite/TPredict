import os
import pandas as pd

def download_historical_data(start_year: int = 2022, end_year: int = 2025) -> pd.DataFrame:
    """Reads local tennis match CSV data straight from the repository data folder."""
    all_years = []
    
    for year in range(start_year, end_year + 1):
        # Read directly from your local repository files
        file_path = f"data/raw/atp_matches_{year}.csv"
        
        if os.path.exists(file_path):
            print(f"📁 Loading local file: {file_path}")
            try:
                df = pd.read_csv(file_path)
                all_years.append(df)
                print(f"   Loaded {year} data. Shape: {df.shape}")
            except Exception as e:
                print(f"❌ Error reading local file for {year}: {e}")
                continue
        else:
            print(f"⚠️ Missing local file: {file_path}")
            continue
        
    if not all_years:
        raise Exception("❌ Total Multi-Year Dataset is completely empty! Ensure CSV files exist inside data/raw/")
        
    combined_df = pd.concat(all_years, ignore_index=True)
    print(f"\n✅ Total Combined Dataset Shape: {combined_df.shape}")
    return combined_df

if __name__ == "__main__":
    download_historical_data()
