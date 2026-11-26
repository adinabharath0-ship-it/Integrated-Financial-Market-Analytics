
import pandas as pd
import os
import glob

input_folder = "data/raw"
output_folder = "data/processed"

os.makedirs(output_folder, exist_ok=True)

files = glob.glob(os.path.join(input_folder, "*.csv"))

for file in files:
    try:
        name = os.path.basename(file).replace(".csv", "")

        print(f"\nCleaning {name}...")

        df = pd.read_csv(file, header=[0, 1], index_col=0)

        # Handle Yahoo Finance MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Handle MT5 CSV format
        if "time" in df.columns:
            df["Date"] = pd.to_datetime(df["time"])
            df = df.drop(columns=["time"])
        else:
            df.index = pd.to_datetime(df.index)
            df.index.name = "Date"
            df = df.reset_index()

        # Remove duplicate dates
        df = df.drop_duplicates(subset=["Date"])

        # Sort by date
        df = df.sort_values("Date")

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Save cleaned file
        output_path = os.path.join(
            output_folder, f"{name}_cleaned.csv"
        )

        df.to_csv(output_path, index=False)

        print("Original/cleaned rows:", len(df))
        print("Saved:", output_path)

    except Exception as e:
        print(f"Error cleaning {file}: {e}")

print("\nData cleaning completed!")

