
import yfinance as yf

# NIFTY 50 data
ticker = "^NSEI"

data = yf.download(
    ticker,
    period="5d",
    interval="1d",
    auto_adjust=True
)

print("\nNIFTY 50 Historical Data:")
print(data)

if not data.empty:
    print("\nYahoo Finance connection successful!")
else:
    print("\nNo data received. Please check connection.")
