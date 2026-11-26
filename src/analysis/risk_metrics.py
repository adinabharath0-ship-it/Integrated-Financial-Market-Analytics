
import pandas as pd
import numpy as np
import os
import glob

input_folder = "data/processed"
output_folder = "data/processed"

files = glob.glob(
    os.path.join(input_folder, "*_cleaned.csv")
)

for file in files:

    name = os.path.basename(file).replace(
        "_cleaned.csv", ""
    )

    print(f"\nAnalyzing {name}...")

    try:
        df = pd.read_csv(file)
        df.columns = [
            str(col).strip().lower()
            for col in df.columns
        ]

        # Find closing price column
        close_col = next(
            (col for col in df.columns
             if col in ["close", "adj close"]),
            None
        )

        if close_col is None:
            print("Close price column not found!")
            continue

        df[close_col] = pd.to_numeric(
            df[close_col], errors="coerce"
        )

        df = df.dropna(subset=[close_col])

        # Daily returns
        df["daily_return"] = df[close_col].pct_change()

        # Cumulative returns
        df["cumulative_return"] = (
            (1 + df["daily_return"].fillna(0)).cumprod() - 1
        )

        # Annualized volatility
        volatility = (
            df["daily_return"].std() * np.sqrt(252) * 100
        )

        # Maximum drawdown
        peak = df[close_col].cummax()
        drawdown = (df[close_col] / peak) - 1
        max_drawdown = drawdown.min() * 100

        # Average daily return
        avg_return = df["daily_return"].mean() * 100

        # Save results
        output_file = os.path.join(
            output_folder, f"{name}_analysis.csv"
        )

        df.to_csv(output_file, index=False)

        print("Average Daily Return:", round(avg_return, 4), "%")
        print("Annualized Volatility:", round(volatility, 2), "%")
        print("Maximum Drawdown:", round(max_drawdown, 2), "%")
        print("Saved:", output_file)

    except Exception as e:
        print("Error:", e)

print("\nRisk analysis completed!")
