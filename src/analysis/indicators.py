
import pandas as pd
import numpy as np
import os
import glob

input_folder = "data/processed"

files = glob.glob(
    os.path.join(input_folder, "*_cleaned.csv")
)

for file in files:
    name = os.path.basename(file).replace(
        "_cleaned.csv", ""
    )

    print(f"\nCalculating indicators for {name}...")

    try:
        df = pd.read_csv(file)

        df.columns = [
            str(col).strip().lower()
            for col in df.columns
        ]

        if "close" not in df.columns:
            print("Close column not found!")
            continue

        df["close"] = pd.to_numeric(
            df["close"], errors="coerce"
        )

        df = df.dropna(subset=["close"]).copy()

        # Simple Moving Averages
        df["SMA_20"] = df["close"].rolling(20).mean()
        df["SMA_50"] = df["close"].rolling(50).mean()
        df["SMA_200"] = df["close"].rolling(200).mean()

        # RSI (14)
        delta = df["close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1/14, min_periods=14, adjust=False
        ).mean()

        avg_loss = loss.ewm(
            alpha=1/14, min_periods=14, adjust=False
        ).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)
        df["RSI_14"] = 100 - (100 / (1 + rs))

        # MACD
        ema_12 = df["close"].ewm(
            span=12, adjust=False
        ).mean()

        ema_26 = df["close"].ewm(
            span=26, adjust=False
        ).mean()

        df["MACD"] = ema_12 - ema_26

        df["MACD_Signal"] = df["MACD"].ewm(
            span=9, adjust=False
        ).mean()

        df["MACD_Histogram"] = (
            df["MACD"] - df["MACD_Signal"]
        )

        # Save indicator data
        output_file = (
            f"data/processed/{name}_indicators.csv"
        )

        df.to_csv(output_file, index=False)

        print("Saved:", output_file)

    except Exception as e:
        print("Error:", e)

print("\nTechnical indicators completed!")
