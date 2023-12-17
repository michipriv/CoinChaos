#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta

class BinanceClient:
    """
    Eine Klasse zur Interaktion mit der Binance-API.

    Diese Klasse ermöglicht das Abrufen historischer Handelsdaten von der Binance-Plattform
    und ihre Speicherung in einem Pandas DataFrame.

    Attributes:
        client (binance.client.Client): Eine Instanz des Binance API-Clients.
        data (pd.DataFrame): Ein DataFrame zur Speicherung der abgerufenen Handelsdaten.

    Methods:
        get_crypto_data(symbol, days_ago, interval='1d'): Ruft Handelsdaten für ein bestimmtes Symbol ab.
        update_data(symbol, days_ago, interval='1d'): Aktualisiert den vorhandenen DataFrame mit neuen Daten.
        get_data(): Gibt den aktuellen DataFrame mit Handelsdaten zurück.
        testAbruf(symbol, days_ago, interval='1d'): Testet das Abrufen von Daten und zeigt eine Vorschau an.
    """

    def __init__(self, api_key, api_secret):
        """
        Initialisiert die BinanceClient-Klasse mit API-Schlüsseln.

        Args:
            api_key (str): Der API-Schlüssel für die Binance-API.
            api_secret (str): Das API-Geheimnis für die Binance-API.
        """
        self.client = Client(api_key, api_secret)
        self.data = pd.DataFrame()
        

    def initialize_data(self):
        """
        Initialisiert den DataFrame mit den erforderlichen Spalten.
        
        time (str): Zeitstempel.
        open_price (float): Eröffnungspreis.
        high_price (float): Höchstpreis.
        low_price (float): Tiefstpreis.
        close_price (float): Schlusspreis.
        volume (int): Volumen.
              
              
        """
        columns = ['time', 'open_price', 'high_price', 'low_price', 'close_price', 
                      'volume','ema_50','ema_100','vector_candle']
        self.data = pd.DataFrame(columns=columns)

    


    def get_data_binance(self, symbol, interval, days_ago):
        
        """
        Ruft Handelsdaten für ein bestimmtes Symbol ab und speichert sie im DataFrame.
    
        Args:
            symbol (str): Das Handelssymbol, z.B. 'BTCUSDT'.
            days_ago (int): Anzahl der Tage in der Vergangenheit für den Beginn der Datenabfrage.
            interval (str, optional): Das Zeitintervall für die Daten. Standardmäßig '1d' (1 Tag).
    
        Returns:
            None: Die Methode aktualisiert den internen DataFrame mit den abgerufenen Daten.
        """
        # Umwandlung des Interval-Strings in timedelta
        end_time = datetime.now()
        days_ago=1
        start_time = end_time - timedelta(days=days_ago)
        start_str = start_time.strftime('%d %b, %Y')
        end_str = end_time.strftime('%d %b, %Y')
   
        candles = self.client.get_historical_klines(symbol, interval, start_str, end_str)
   
    
        for candle in candles:
            time = candle[0]
            open_price = float(candle[1])
            high_price = float(candle[2])
            low_price = float(candle[3])
            close_price = float(candle[4])
            volume = float(candle[5])
    
            # Verwende die append_data-Methode, um die Daten zum DataFrame hinzuzufügen
            self.append_data(
                time=time,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=volume
            )

   

    def append_data(self, **kwargs):
        """
        Hängt Daten an ein vorhandenes Pandas DataFrame an.
        
        Args:
            **kwargs: Keyword-Argumente für die Daten, die hinzugefügt werden sollen.
            
                Args:
                    time (str): Zeitstempel.
                    open_price (float): Eröffnungspreis.
                    high_price (float): Höchstpreis.
                    low_price (float): Tiefstpreis.
                    close_price (float): Schlusspreis.
                    volume (int): Volumen.
        """
        new_row = kwargs
        new_row_df = pd.DataFrame([new_row])
        self.data = pd.concat([self.data, new_row_df], ignore_index=True)
        
 
    def print_data(self):
        """
        Zeigt alle Daten des internen DataFrame an.

        Diese Methode gibt den aktuellen Inhalt des DataFrame `self.data` aus.
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
        # Fügen Sie eine neue Spalte hinzu
        self.data[column_name] = values
        


    def get_data(self):
        """
        Gibt den aktuellen DataFrame mit Handelsdaten zurück.
        """
        return self.data

    