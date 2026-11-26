
import yfinance as yf
import MetaTrader5 as mt5
import pandas as pd
import os
from datetime import datetime, timedelta

os.makedirs("data/raw", exist_ok=True)

# 1. Indian Market + Forex symbols from Yahoo Finance
yahoo_symbols = {
    "NIFTY50": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "INFOSYS": "INFY.NS",
    "SBIN": "SBIN.NS",
    "ITC": "ITC.NS",
    "BHARTIARTL": "BHARTIARTL.NS",
    "LT": "LT.NS",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "AUDUSD": "AUDUSD=X",
    "USDINR": "INR=X"
}

for name, ticker in yahoo_symbols.items():
    try:
        print(f"Downloading {name}...")
        df = yf.download(
            ticker,
            period="5y",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if not df.empty:
            df.to_csv(f"data/raw/{name}.csv")
            print(f"Saved {name}: {len(df)} rows")
        else:
            print(f"No data: {name}")

    except Exception as e:
        print(f"Error {name}: {e}")


# 2. Gold data from MT5
print("\nConnecting to MT5...")

if mt5.initialize():
    possible_symbols = ["XAUUSD", "GOLD"]

    selected_symbol = None

    for symbol in possible_symbols:
        if mt5.symbol_info(symbol):
            selected_symbol = symbol
            break

    if selected_symbol:
        mt5.symbol_select(selected_symbol, True)

        end = datetime.now()
        start = end - timedelta(days=5 * 365)

        rates = mt5.copy_rates_range(
            selected_symbol,
            mt5.TIMEFRAME_D1,
            start,
            end
        )

        if rates is not None and len(rates) > 0:
            gold_df = pd.DataFrame(rates)
            gold_df["time"] = pd.to_datetime(
                gold_df["time"], unit="s"
            )
            gold_df.to_csv(
                "data/raw/XAUUSD.csv",
                index=False
            )
            print("Gold saved:", len(gold_df), "rows")
        else:
            print("Gold history unavailable. Check MT5 history.")

    else:
        print("Gold symbol not found in MT5.")

    mt5.shutdown()

else:
    print("MT5 connection failed:", mt5.last_error())

print("\nAll download tasks completed!")


