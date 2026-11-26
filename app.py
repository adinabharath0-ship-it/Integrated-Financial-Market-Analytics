
from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import os

app = Flask(__name__)

DATA_FOLDER = "data/processed"

INDIAN_COMPANIES = {
    "NIFTY50": "NIFTY 50",
    "BANKNIFTY": "BANK NIFTY",
    "RELIANCE": "Reliance",
    "TCS": "TCS",
    "INFOSYS": "Infosys",
    "HDFCBANK": "HDFC Bank",
    "ICICIBANK": "ICICI Bank",
    "SBIN": "SBI",
    "BHARTIARTL": "Bharti Airtel",
    "ITC": "ITC",
    "LT": "Larsen & Toubro"
}

ALL_MARKETS = [
    "NIFTY50", "BANKNIFTY", "RELIANCE", "TCS",
    "INFOSYS", "HDFCBANK", "ICICIBANK", "SBIN",
    "BHARTIARTL", "ITC", "LT", "EURUSD",
    "GBPUSD", "USDJPY", "USDINR", "AUDUSD", "XAUUSD"
]


def load_csv(symbol):

    path = os.path.join(DATA_FOLDER, f"{symbol}_indicators.csv")

    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]

    return df


def get_market_data(symbols):

    results = []

    for symbol in symbols:

        try:
            df = load_csv(symbol)

            if df is None or df.empty or "close" not in df.columns:
                continue

            latest = df.iloc[-1]

            results.append({
                "name": symbol,
                "price": round(float(latest["close"]), 2),
                "rsi": round(float(latest["rsi_14"]), 2)
                if pd.notna(latest.get("rsi_14")) else "N/A",
                "sma20": round(float(latest["sma_20"]), 2)
                if pd.notna(latest.get("sma_20")) else "N/A",
                "date": str(latest.get("date", "N/A"))
            })

        except Exception as e:
            print(f"Error loading {symbol}: {e}")

    return results


def create_chart(symbol):

    df = load_csv(symbol)

    if df is None or df.empty:
        return None

    if "close" not in df.columns:
        return None

    if "date" not in df.columns:
        return None

    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["close", "date"]).tail(1250)

    if df.empty:
        return None

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["close"],
        mode="lines",
        name="Closing Price"
    ))

    if "sma_20" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["sma_20"],
            mode="lines",
            name="SMA 20"
        ))

    if "sma_50" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["sma_50"],
            mode="lines",
            name="SMA 50"
        ))

    company_name = INDIAN_COMPANIES.get(symbol, symbol)

    fig.update_layout(
        title=f"{company_name} Historical Price Analysis",
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        height=500
    )

    return fig.to_json()


@app.route("/")
def home():

    market_data = get_market_data(ALL_MARKETS)
    chart_json = create_chart("NIFTY50")

    return render_template(
        "index.html",
        market_data=market_data,
        chart_json=chart_json
    )


@app.route("/indian")
def indian_market():

    selected = request.args.get("symbol", "NIFTY50")

    if selected not in INDIAN_COMPANIES:
        selected = "NIFTY50"

    market_data = get_market_data(INDIAN_COMPANIES.keys())
    chart_json = create_chart(selected)

    return render_template(
        "indian.html",
        market_data=market_data,
        companies=INDIAN_COMPANIES,
        selected=selected,
        chart_json=chart_json
    )


if __name__ == "__main__":
    app.run(debug=True)
