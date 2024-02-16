#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
from pytz import timezone
import pytz

class BinanceClient:
    """
    Eine Klasse zur Interaktion mit der Binance-API.

    Diese Klasse ermöglicht das Abrufen historischer Handelsdaten von der Binance-Plattform
    und ihre Speicherung in einem Pandas DataFrame.

    :param api_key: Der API-Schlüssel für die Binance-API.
    :type api_key: str
    :param api_secret: Das API-Geheimnis für die Binance-API.
    :type api_secret: str

    :ivar client: Eine Instanz des Binance API-Clients.
    :vartype client: binance.client.Client
    :ivar data: Ein DataFrame zur Speicherung der abgerufenen Handelsdaten.
    :vartype data: pandas.DataFrame
    """

    def __init__(self, api_key, api_secret, time_zone='UTC'):
         
        """
        Initialisiert die BinanceClient-Klasse mit API-Schlüsseln.

        :param api_key: Der API-Schlüssel für die Binance-API.
        :type api_key: str
        :param api_secret: Das API-Geheimnis für die Binance-API.
        :type api_secret: str
        """
            
        self.client = Client(api_key, api_secret)
        self.data = pd.DataFrame()
        self.time_zone = timezone(time_zone)
        

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
        
            time            open_price   high_price  low_price  close_price volume    vector_color lowest_low    symbol interval    ema_5         ema_13         ema_50        ema_100       ema_200       ema_800        Kerze    lower_low  lower_low_start lower_low_ende  w1 w_middle w2
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
        
        """       
        .. py:method:: BinanceClient.get_data_binance(symbol, interval, days_ago)

        Ruft Handelsdaten für ein bestimmtes Kryptowährungssymbol von der Binance API ab und speichert sie in einem DataFrame. Diese Methode verwendet die aktuelle Serverzeit von Binance, um sicherzustellen, dass die Zeitberechnung genau ist. Die abgerufenen Daten enthalten verschiedene Details zu jedem Handelsintervall, wie Öffnungs-, Höchst-, Tiefst- und Schlusspreise sowie das gehandelte Volumen.

        :param str symbol: Das Handelssymbol für die Abfrage, beispielsweise 'BTCUSDT'.
        :param str interval: Das Zeitintervall für die Daten. Die unterstützten Intervalle sind beispielsweise '1m' (eine Minute), '1h' (eine Stunde), '1d' (ein Tag). Standardmäßig ist das Intervall auf '1d' gesetzt.
        :param int limit: Die Anzahl der Kerzen die abgerufen werden sollen. 

        Die Methode beginnt mit der Abfrage der aktuellen Serverzeit von Binance und berechnet den Start- und Endzeitpunkt für die Datensammlung. Anschließend werden die historischen Kerzendaten ('klines') für das angegebene Symbol und Intervall von der Binance API abgerufen. Jede Kerze wird in ein Datumsformat (im UTC-Standard) umgewandelt und zusammen mit anderen relevanten Handelsdaten in den DataFrame eingefügt.

        :return: Diese Methode gibt nichts zurück, sondern aktualisiert den internen DataFrame der Klasse mit den abgerufenen Handelsdaten.
        :rtype: None

        Beispiel::

        # Erstellen einer Instanz der BinanceClient-Klasse
        client = BinanceClient(api_key, api_secret)

        # Abrufen von Handelsdaten für BTCUSDT für die letzten 10 Balken im 1h Format
        client.get_data_binance('BTCUSDT', '1h', 10)

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

    
        # Abrufen der historischen Kurse mit Limit
        candles = self.client.get_historical_klines(symbol, interval, start_str, end_str, limit=limit)


        for candle in candles:
            
            time = candle[0]
            # Zeitzone konvertieren
            dt = datetime.fromtimestamp(time / 1000, pytz.utc).astimezone(self.time_zone)
            
            # Formatieren des Zeitstempels im ISO 8601-Format
            formatted_time = dt.strftime('%Y-%m-%dT%H:%M:%S')
        
            open_price = float(candle[1])
            high_price = float(candle[2])
            low_price = float(candle[3])
            close_price = float(candle[4])
            volume = float(candle[5])
    
            # Verwende die append_data-Methode, um die Daten zum DataFrame hinzuzufügen

            self.append_data(         
               time=time,
               symbol=symbol,
               interval=interval,
               open_price=open_price,
               high_price=high_price,
               low_price=low_price,
               close_price=close_price,
               volume=volume
           )


   

    def append_data(self, **kwargs):
        """
        Hängt Daten an ein vorhandenes Pandas DataFrame an.

        :param kwargs: Keyword-Argumente für die Daten, die hinzugefügt werden sollen.
                       Beinhaltet: 'time', 'open_price', 'high_price', 'low_price', 
                       'close_price' und 'volume'.
        """
        
        new_row = kwargs
        new_row_df = pd.DataFrame([new_row])
        self.data = pd.concat([self.data, new_row_df], ignore_index=True)
        
 
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
   
    def add_column(self, column_name, values):
        """
        Fügt eine neue Spalte zum DataFrame hinzu.

        :param column_name: Name der neuen Spalte.
        :type column_name: str
        :param values: Werte für die neue Spalte.
        :type values: list, pandas.Series
        """


        self.data[column_name] = values
        


    def get_data(self):
        """
        Gibt den aktuellen DataFrame mit Handelsdaten zurück.

        :return: Der DataFrame mit Handelsdaten.
        :rtype: pandas.DataFrame
        """
        
        return self.data

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
