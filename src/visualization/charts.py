
import pandas as pd
import matplotlib.pyplot as plt
import os

input_folder = "data/processed"
output_folder = "reports/charts"

os.makedirs(output_folder, exist_ok=True)

files = [
    f for f in os.listdir(input_folder)
    if f.endswith("_indicators.csv")
]

for file in files:

    name = file.replace("_indicators.csv", "")

    print(f"Creating chart for {name}...")

    try:
        df = pd.read_csv(
            os.path.join(input_folder, file)
        )

        df["Date"] = pd.to_datetime(df["Date"])
        df["close"] = pd.to_numeric(
            df["close"], errors="coerce"
        )

        df = df.dropna(subset=["close"])

        # Price and SMA chart
        plt.figure(figsize=(14, 6))

        plt.plot(
            df["Date"], df["close"],
            label="Close Price"
        )

        for col in ["SMA_20", "SMA_50", "SMA_200"]:
            if col in df.columns:
                plt.plot(
                    df["Date"], df[col],
                    label=col
                )

        plt.title(f"{name} - Price & Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            f"{output_folder}/{name}_chart.png"
        )

        plt.close()

        # RSI chart
        if "RSI_14" in df.columns:
            plt.figure(figsize=(14, 4))

            plt.plot(
                df["Date"], df["RSI_14"],
                label="RSI 14"
            )

            plt.axhline(70, linestyle="--")
            plt.axhline(30, linestyle="--")

            plt.title(f"{name} - RSI Indicator")
            plt.xlabel("Date")
            plt.ylabel("RSI")
            plt.legend()
            plt.grid(True)

            plt.tight_layout()

            plt.savefig(
                f"{output_folder}/{name}_RSI.png"
            )

            plt.close()

        print("Charts saved successfully!")

    except Exception as e:
        print("Error:", e)

print("\nAll charts generated!")
