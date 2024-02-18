#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import time

class BinanceClient:
    """
     Eine Klasse zur Interaktion mit der Binance-API.
    
     Diese Klasse ermöglicht das Abrufen historischer Handelsdaten von der Binance-Plattform
     und ihre Speicherung in einem Pandas DataFrame oder einer SQLite-Datenbank.
    
     :param api_key: Der API-Schlüssel für die Binance-API.
     :type api_key: str
     :param api_secret: Das API-Geheimnis für die Binance-API.
     :type api_secret: str
     :param time_zone: Die Zeitzone für die Zeitstempel der Daten.
     :type time_zone: str
     :param db_handler: Handler für die SQLite-Datenbank.
     :type db_handler: CoinChaosDB
    
     :ivar client: Eine Instanz des Binance API-Clients.
     :vartype client: binance.client.Client
     :ivar data: Ein DataFrame zur Speicherung der abgerufenen Handelsdaten.
     :vartype data: pandas.DataFrame
     :ivar db_handler: Der Datenbankhandler.
     :vartype db_handler: CoinChaosDB
     """

    def __init__(self, api_key, api_secret, time_zone, db):
         
        """
         Initialisiert die BinanceClient-Klasse mit API-Schlüsseln und einem Datenbankhandler.
        
         :param api_key: Der API-Schlüssel für die Binance-API.
         :type api_key: str
         :param api_secret: Das API-Geheimnis für die Binance-API.
         :type api_secret: str
         :param db_handler: Handler für die SQLite-Datenbank.
         :type db_handler: CoinChaosDB
         :param time_zone: Die Zeitzone für die Zeitstempel der Daten.
         :type time_zone: str
         """
            
        self.client = Client(api_key, api_secret)
        self.data = pd.DataFrame()
        self.time_zone = timezone(time_zone)
        self.db = db
        
        

    def initialize_data(self):
        """
        Initialisiert den DataFrame mit den erforderlichen Spalten.
        
        """
        
        
        columns = ['time', 
                   'open_price', 
                   'high_price', 
                   'low_price', 
                   'close_price', 
                   'volume',
                   'vector_color', 
                   'lowest_low',
                   'symbol',
                   'interval',
                   'ema_5',
                   'ema_13',
                   'ema_50',
                   'ema_100',
                   'ema_200',
                   'ema_800',
                   'Kerze',
                   'lower_low',
                   'lower_low_start',
                   'lower_low_ende',
                   'w1',
                   'w_middle',
                   'w2'
                   
                   ]


        '''
        binance time ... UnixTimestamp in milliseconds
        
        pk    time            open_price   high_price  low_price  close_price volume    vector_color lowest_low    symbol interval    ema_5         ema_13         ema_50        ema_100       ema_200       ema_800        Kerze    lower_low  lower_low_start lower_low_ende  w1 w_middle w2
        0   1705814100000    41675.84    41675.84   41645.41     41656.10   96.21797  darkgrey     NaN  BTCUSDT      15m            41656.100000  41656.100000   41656.100000  41656.100000  41656.100000  41656.100000   Rot                 AA     
        1   1705815000000    41656.10    41656.10   41644.93     41649.97   71.57745  darkgrey     NaN  BTCUSDT      15m            41654.056667  41655.224286   41655.859608  41655.978614  41656.039005  41656.084694   Rot                 AA
        2   1705815900000    41649.97    41649.98   41628.46     41628.47   72.93337  darkgrey     NaN  BTCUSDT      15m            41645.527778  41651.402245   41654.785506  41655.433889  41655.764687  41656.015744   Rot
        3   1705816800000    41628.46    41654.99   41628.46     41654.98   69.95751  lightgrey    NaN  BTCUSDT      15m            41648.678519  41651.913353   41654.793133  41655.424901  41655.756879  41656.013157  Grün 
        4   1705817700000    41654.99    41654.99   41564.29     41633.43  139.76318  darkgrey     NaN  BTCUSDT      15m            41643.595679  41649.272874   41653.955363  41654.989358  41655.534721  41655.956770   Rot        LL       AA                              w1     
        5   1705818600000    41633.42    41633.43   41613.75     41613.75   53.42719  darkgrey     NaN  BTCUSDT      15m            41633.647119  41644.198178   41652.378682  41654.172737  41655.118952  41655.851385   Rot                 AA     
        6   1705819500000    41613.75    41613.76   41583.24     41597.66   86.62183  darkgrey     NaN  BTCUSDT      15m            41621.651413  41637.549866   41650.232851  41653.053673  41654.547221  41655.706088   Rot        LL       A                               w1
        7   1705820400000    41597.66    41613.10   41587.75     41596.54  116.74075  darkgrey     NaN  BTCUSDT      15m            41613.280942  41631.691314   41648.127249  41651.934591  41653.970035  41655.558357   Rot   
        8   1705821300000    41596.55    41630.00   41587.27     41629.99   66.25310  lightgrey    NaN  BTCUSDT      15m            41618.850628  41631.448269   41647.415985  41651.500044  41653.731428  41655.494516  Grün             
        9   1705822200000    41630.00    41669.94   41629.99     41651.11   62.12878  lightgrey    NaN  BTCUSDT      15m            41629.603752  41634.257088   41647.560848  41651.492321  41653.705344  41655.483569  Grün                                 EE            
        10  1705823100000    41651.11    41656.80   41645.04     41648.51   39.86989  darkgrey     NaN  BTCUSDT      15m            41635.905835  41636.29321    41647.598070  41651.433265  41653.653649  41655.466157   Rot 
        
        '''


        self.data = pd.DataFrame(columns=columns)

    
    def get_data_binance(self, symbol, interval, limit):
        
        
        # Prüfen, ob das Symbol und das Zeitintervall bereits in der Datenbank vorhanden sind
        c = self.db.conn.cursor()
        c.execute("SELECT COUNT(*) FROM coin_data WHERE coin = ? AND timeframe = ?", (symbol, interval))
    
        result = c.fetchone()
        count = result[0]
        
        if count > 0:
            print(f"{symbol}  {interval} wird aktualisiert.")
            self.get_data_binance_last(symbol, interval)
        else:
            print(f"{symbol} {interval} erstemal gespeichert.")
            self.get_data_binance_first(symbol, interval, limit)
                
            
    
    def get_data_binance_first(self, symbol, interval, limit):
        """
        Ruft Handelsdaten für ein bestimmtes Kryptowährungssymbol von der Binance API ab und speichert sie in der Datenbanktabelle 'coin_data'.
    
        :param str symbol: Das Handelssymbol für die Abfrage, beispielsweise 'BTCUSDT'.
        :param str interval: Das Zeitintervall für die Daten, z.B. '1m', '1h', '1d'.
        :param int limit: Die Anzahl der abzurufenden Datenpunkte.
        """
    
        # Abrufen der aktuellen Serverzeit von Binance
        server_time = self.client.get_server_time()
        server_dt = datetime.fromtimestamp(server_time['serverTime'] / 1000, pytz.utc)
    
        # Berechnung des Startzeitpunkts basierend auf 'limit' und 'interval'
        if interval.endswith('m'):
            delta = timedelta(minutes=int(interval[:-1]) * limit)
        elif interval.endswith('h'):
            delta = timedelta(hours=int(interval[:-1]) * limit)
        elif interval.endswith('d'):
            delta = timedelta(days=int(interval[:-1]) * limit)
        else:
            raise ValueError("Ungültiges Intervallformat")
    
        start_time = server_dt - delta
    
        # Formatierung der Zeitstempel für die API-Anfrage
        start_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_str = server_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
        # Abrufen der historischen Kurse
        candles = self.client.get_historical_klines(symbol, interval, start_str, end_str, limit=limit)
    
        # Einfügen der Daten in die Datenbank
        for candle in candles:
            timeunix = candle[0]
            timestd = datetime.fromtimestamp(timeunix / 1000).strftime('%Y-%m-%d %H:%M:%S')
            open_price = candle[1]
            high_price = candle[2]
            low_price = candle[3]
            close_price = candle[4]
            volume = candle[5]
    
            self.db.conn.execute("""
                INSERT INTO coin_data (coin, timeframe, timeunix, timestd, open_price, high_price, low_price, close_price, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (symbol, interval, timeunix, timestd, open_price, high_price, low_price, close_price, volume))
    
        # Commit der Transaktion
        self.db.conn.commit()

    def get_last_entry(self, symbol, interval):
        """
        Retrieves the last entry for the specified symbol and interval from the coin_data table.

        :param symbol: The trading symbol (e.g., BTCUSDT).
        :param interval: The time interval (e.g., 1m, 5m, 1h).
        :return: The last entry for the specified symbol and interval, or None if no entry is found.
        """
        query = """
            SELECT * FROM coin_data
            WHERE coin = ? AND timeframe = ?
            ORDER BY timeunix DESC
            LIMIT 1
        """
        c = self.db.conn.cursor()
        c.execute(query, (symbol, interval))
        return c.fetchone()
        



    def get_data_binance_last(self, symbol, interval):
        """
        Retrieves and updates data from Binance for a specific symbol and interval,
        considering the specified time zone.
        """
        # Get the last entry for the symbol and interval from the table
        last_entry = self.get_last_entry(symbol, interval)
        if last_entry is None:
            print(f"Keine Daten für: {symbol} {interval}")
            return
    
        # Extract the relevant information from the last entry
        last_timeunix = last_entry[3]  # The Unix timestampms of the last entry
        last_timestd = last_entry[4]  # The standard time of the last entry
    
        # Display the last entry time for verification
        print(f"Letzter eintrag: {last_timestd}")
    
        # Get the current server time from Binance
        server_time = self.client.get_server_time()
        server_time_utc = datetime.fromtimestamp(server_time['serverTime'] / 1000, tz=pytz.utc)
        # Umrechnung der Serverzeit in Millisekunden für den Vergleich
        current_time_unix = server_time['serverTime']

        # Berechnung der minimalen Zeitdifferenz basierend auf dem Intervall
        if interval.endswith("m"):
            time_diff = int(interval[:-1]) * 60 * 1000  # Konvertierung von Minuten in Millisekunden
        elif interval.endswith("h"):
            time_diff = int(interval[:-1]) * 60 * 60 * 1000  # Konvertierung von Stunden in Millisekunden
        elif interval.endswith("d"):
            time_diff = int(interval[:-1]) * 24 * 60 * 60 * 1000  # Konvertierung von Tagen in Millisekunden
        else:
            time_diff = 1 * 60 * 1000  # Standardwert auf 1 Minute setzen, falls das Intervall nicht erkannt wird

        # Überprüfen, ob die erforderliche Zeit seit dem letzten Eintrag vergangen ist
        if current_time_unix - last_timeunix < time_diff:
            print("Kein neue Daten vorhanden.")
            return 0 # Frühe Rückkehr, wenn das erforderliche Intervall noch nicht vergangen ist

    
        # Convert the server time to the specified time zone
        server_time_converted = server_time_utc.astimezone(self.time_zone)
        #print(f"Current Binance Zeit : {server_time_converted.strftime('%Y-%m-%d %H:%M:%S')}")
    
        # Calculate the start_str for new data retrieval
        start_str = datetime.utcfromtimestamp((last_timeunix + 1) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        
      
    
  
        # Wenn das Skript hier fortgesetzt wird, bedeutet das, dass neue Daten verfügbar sind
        candles = self.client.get_historical_klines(symbol, interval, start_str, "now")
        
        if candles:
            print(f"Retrieved {len(candles)} new candles from Binance.")
        else:
            print("No new data available to retrieve.")
            
        # Track the number of added records
        added_records = 0
    
        # Insert new data into the database
        for candle in candles:
            self.db.conn.execute("""
                INSERT INTO coin_data (coin, timeframe, timeunix, timestd, open_price, high_price, low_price, close_price, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (symbol, interval, candle[0], datetime.fromtimestamp(candle[0] / 1000, tz=self.time_zone).strftime('%Y-%m-%d %H:%M:%S'), candle[1], candle[2], candle[3], candle[4], candle[5]))
            added_records += 1
    
        # Commit the transaction
        self.db.conn.commit()

        #print(f"{added_records} records were added.")
        return added_records
    
     
    #dataframe löschen
    def print_data(self):
        """
        Zeigt alle Daten des internen DataFrame an.

        Gibt den aktuellen Inhalt des DataFrame `self.data` aus.
        """
        
        
        pd.set_option('display.max_rows', None)  # Zeige alle Zeilen
        pd.set_option('display.max_columns', None)  # Zeige alle Spalten
  
        
        if self.data.empty:
            print("Der DataFrame ist leer.")
        else:
            print("init data")
            print(self.data)
            
            #achtung es werdennciht immer alle werte in einer reihe angezeigt-> selektive ausgabe verwenden
            #selektierte daten ausgeben
            #elected_columns = self.data.loc[:, ['open_price', 'high_price', 'ema_50']]
            #print(selected_columns)
    
    
    #dataframe löschen   
    def add_column(self, column_name, values):
        """
        Fügt eine neue Spalte zum DataFrame hinzu.

        :param column_name: Name der neuen Spalte.
        :type column_name: str
        :param values: Werte für die neue Spalte.
        :type values: list, pandas.Series
        """


        self.data[column_name] = values
        
    
    #dataframe löschen
    def get_data(self):
        """
        Gibt den aktuellen DataFrame mit Handelsdaten zurück.

        :return: Der DataFrame mit Handelsdaten.
        :rtype: pandas.DataFrame
        """
        
        return self.data
    
  
    # alle commission und fundingrate funktionen überprüfen

    def get_commission(self):
        """
        Ruft die Handelsgebühren von Binance ab und speichert sie in einem DataFrame.
        """
        # Versuche, die Handelsgebühreninformationen abzurufen
        try:
            fees_info = self.client.get_trade_fee()  # Ruft Gebühren für alle Handelspaare ab
            # Erstelle ein DataFrame aus den Gebühreninformationen
            fees_df = pd.DataFrame(fees_info)
            
            # Falls spezifische Bearbeitungen benötigt werden, können sie hier hinzugefügt werden
            # Zum Beispiel, Extraktion spezifischer Felder oder Anpassungen
            
            # Speichere das Ergebnis in df_fee
            self.df_fee = fees_df
            print("Handelsgebühren erfolgreich abgerufen und gespeichert.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
 
        
 
             
    def show_commission(self, symbol=None):
        """
        Zeigt die Gebühreninformationen aus dem df_fee DataFrame. Kann auf ein spezifisches Symbol gefiltert werden.
        
        :param symbol: Optional. Das Handelssymbol, für das die Gebühren angezeigt werden sollen.
        """
        #print(self.df_fee.columns)
        
        if hasattr(self, 'df_fee') and not self.df_fee.empty:
            if symbol:
                # Filtert den DataFrame auf das gegebene Symbol
                df_filtered = self.df_fee[self.df_fee['symbol'] == symbol]
                if not df_filtered.empty:
                    print(f"Gebühreninformationen für {symbol}:")
                    print(df_filtered[['symbol', 'makerCommission', 'takerCommission']])
                else:
                    print(f"Keine Gebühreninformationen für {symbol} gefunden.")
            else:
                print("Gebühreninformationen für alle Symbole:")
                print(self.df_fee[['symbol', 'makerCommission', 'takerCommission']])
        else:
            print("Keine Gebühreninformationen verfügbar.")
    
    

             
    def get_funding_rate(self, symbol):
        """
        Ruft die aktuelle Funding Rate für ein spezifisches Futures-Symbol ab.
        
        :param symbol: Das Handelssymbol für den Futures-Kontrakt (z.B. 'BTCUSDT').
        """
        try:
            # API-Endpunkt für die aktuelle Funding Rate
            funding_rate_info = self.client.futures_funding_rate(symbol=symbol)
            
            # Zeigt die Funding Rate Information
            print(f"Funding Rate für {symbol}: {funding_rate_info}")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")



    def list_symbols_by_commission(self, commission_type='0'):
        """
        Listet alle Symbole und ihre Kommissionen basierend auf der Kommissionsrate auf.
        """
        if hasattr(self, 'df_fee') and not self.df_fee.empty:
            # Stellen Sie sicher, dass die Kommissionswerte numerisch sind
            self.df_fee['makerCommission'] = pd.to_numeric(self.df_fee['makerCommission'], errors='coerce')
            self.df_fee['takerCommission'] = pd.to_numeric(self.df_fee['takerCommission'], errors='coerce')
    
            # Filtern des DataFrames basierend auf dem commission_type
            if commission_type == '0':
                filtered_df = self.df_fee[(self.df_fee['makerCommission'] == 0) & (self.df_fee['takerCommission'] == 0)]
            elif commission_type == '<0':
                filtered_df = self.df_fee[(self.df_fee['makerCommission'] < 0) | (self.df_fee['takerCommission'] < 0)]
            elif commission_type == '>0':
                filtered_df = self.df_fee[(self.df_fee['makerCommission'] > 0) | (self.df_fee['takerCommission'] > 0)]
            else:
                print("Ungültiger commission_type angegeben.")
                return
    
            if not filtered_df.empty:
                print(f"Symbole mit Kommission {commission_type}:")
                # Zeigen Sie die Symbolnamen zusammen mit ihren Kommissionen an
                for index, row in filtered_df.iterrows():
                    print(f"Symbol: {row['symbol']}, Maker-Kommission: {row['makerCommission']}, Taker-Kommission: {row['takerCommission']}")
            else:
                print(f"Keine Symbole mit Kommission {commission_type} gefunden.")
        else:
            print("Keine Gebühreninformationen verfügbar.")

    def get_funding_rate_history(self, symbol, limit=500):
        """
        Ruft die Historie der Funding Rates für ein spezifisches Futures-Symbol ab.
        :param symbol: Das Futures-Symbol, für das die Funding Rate Historie abgerufen werden soll.
        :param limit: Die maximale Anzahl an Einträgen, die abgerufen werden soll.
        """
        funding_rates = self.client.futures_funding_rate(symbol=symbol, limit=limit)
        if funding_rates:
            self.df_fundingRate = pd.DataFrame(funding_rates)
            print("Funding Rate Historie erfolgreich abgerufen und im DataFrame gespeichert.")
        else:
            print("Keine Daten zur Funding Rate gefunden.")

    
    def get_BinanceTime(self):
        """
        Ruft die aktuelle Serverzeit von Binance ab und zeigt sie in der durch self.time_zone definierten Zeitzone an.
        """
        # Abrufen der aktuellen Serverzeit von Binance
        server_time = self.client.get_server_time()
    
        # Umwandlung des Zeitstempels in Millisekunden in ein datetime-Objekt
        dt_utc = datetime.utcfromtimestamp(server_time['serverTime'] / 1000).replace(tzinfo=pytz.utc)
    
        # Konvertieren der UTC-Zeit in die in der Klasse definierte Zeitzone
        dt_converted = dt_utc.astimezone(self.time_zone)
    
        # Ausgabe der Zeit in der konvertierten Zeitzone
        print(f"Current Binance Time in {self.time_zone}: {dt_converted.strftime('%Y-%m-%d %H:%M:%S')}")
