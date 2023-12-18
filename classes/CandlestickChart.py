import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

class CandlestickChart:
    def __init__(self, binance_client):
        """
        Initialisiert die CandlestickChart-Klasse.

        Args:
            binance_client (BinanceClient): Eine Instanz der BinanceClient-Klasse.
            technical_indicators (TechnicalIndicators, optional): Eine Instanz der TechnicalIndicators-Klasse.
        """
        self.binance_client = binance_client

    def plot(self, symbol, interval, days_ago):
        # Daten von Binance abrufen
        df = self.binance_client.get_data()

        # Diagramm zeichnen
        self.plot_candlestick(df, symbol, interval)

   





    def prepare_dataframe(self, df):
        df['Date'] = pd.to_datetime(df['time'], unit='ms')
        df['Date'] = df['Date'].apply(mdates.date2num)
        return df

  
    def draw_candles(self, ax, df):
        for idx, row in df.iterrows():
            candle_color = row['vector_color']

            # Bestimmen der Docht-Farbe basierend auf der 'Kerze'-Spalte
            if row['Kerze'] == 'Grün':
                wick_color = 'green'
            elif row['Kerze'] == 'Rot':
                wick_color = 'red'
            else:
                wick_color = 'black'  # Standardfarbe, falls 'Kerze' weder 'Grün' noch 'Rot' ist

            # Docht zeichnen
            ax.plot([row['Date'], row['Date']], [row['low_price'], row['high_price']], color=wick_color)

            # Kerzenkörper zeichnen
            ax.plot([row['Date'], row['Date']], [row['open_price'], row['close_price']], color=candle_color, linewidth=8)



    def draw_ema_lines(self, ax, df):
        ax.plot(df['Date'], df['ema_50'], label='EMA-50', color='blue', linewidth=2)
        ax.plot(df['Date'], df['ema_100'], label='EMA-100', color='purple', linewidth=2)

    def plot_candlestick(self, df, symbol, interval):
        if 'ema_50' not in df.columns or 'ema_100' not in df.columns or 'vector_color' not in df.columns:
            raise ValueError("Eine oder mehrere erforderliche Spalten fehlen im DataFrame.")

        df = self.prepare_dataframe(df)
        fig, ax = plt.subplots()
        self.draw_candles(ax, df)
        self.draw_ema_lines(ax, df)

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.title(f'{symbol} Candlestick Chart ({interval})')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
