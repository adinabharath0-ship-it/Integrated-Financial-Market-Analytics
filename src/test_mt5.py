
import MetaTrader5 as mt5

# Initialize MT5
if not mt5.initialize():
    print("MT5 connection failed!")
    print("Error:", mt5.last_error())
else:
    print("MT5 connection successful!")

    # Account information
    account = mt5.account_info()

    if account:
        print("\nAccount Information:")
        print("Login:", account.login)
        print("Server:", account.server)

    # Check available symbols
    symbols = ["EURUSD", "GBPUSD", "XAUUSD"]

    print("\nSymbol Availability:")

    for symbol in symbols:
        info = mt5.symbol_info(symbol)

        if info:
            print(symbol, "Available")
        else:
            print(symbol, "Not found")

    mt5.shutdown()
