import argparse
import pandas as pd
from binance.client import Client
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetch and plot Binance data.')
    parser.add_argument('--interval', help='Data interval (1h, 4h, 1d)', default='1h', choices=['1h', '4h', '1d'])
    parser.add_argument('--days', help='Number of days to fetch', type=int, default=7)
    args = parser.parse_args()
    return args



def get_api_keys(file_name):
    keys = {}
    with open(file_name, 'r') as file:
        for line in file:
            if "BINANCE_API_KEY" in line:
                keys['binance_key'] = line.split('=')[1].strip()
            elif "BINANCE_API_SECRET" in line:
                keys['binance_secret'] = line.split('=')[1].strip()
    return keys

def fetch_binance_data(client, symbol, interval, lookback):
    bars = client.get_historical_klines(symbol, interval, lookback + " ago UTC")
    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)
    df['open'] = pd.to_numeric(df['open'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['close'] = pd.to_numeric(df['close'])
    df['volume'] = pd.to_numeric(df['volume'])  # Konvertierung der Volumen-Daten
    return df


def main():
    args = parse_arguments()

    api_keys = get_api_keys('config.txt')
    client = Client(api_keys['binance_key'], api_keys['binance_secret'])

    interval_map = {
        "1h": Client.KLINE_INTERVAL_1HOUR,
        "4h": Client.KLINE_INTERVAL_4HOUR,
        "1d": Client.KLINE_INTERVAL_1DAY
    }
    interval = interval_map[args.interval]
    lookback = f"{args.days} day"
    symbol = "BTCUSDT"

    # Abrufen und Plotten der Candlestick-Daten
    df = fetch_binance_data(client, symbol, interval, lookback)
    mpf.plot(df, type='candle', style='charles', title=f"{symbol} {interval} Chart", volume=True)



if __name__ == "__main__":
    main()

