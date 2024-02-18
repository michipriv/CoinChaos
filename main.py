#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Crypto-Projekt-Modul

Dieses Modul ist der Hauptteil des Crypto-Projekts. Es enthält die Hauptfunktion, 
die für die Ausführung des gesamten Prozesses des Abrufens und Visualisierens von 
Kryptowährungs-Daten verantwortlich ist.

Das Modul führt folgende Schritte aus:
1. Liest API-Konfigurationen und erstellt einen Binance-Client.
2. Ruft Handelsdaten für ein spezifisches Kryptowährungssymbol ab.
3. Berechnet technische Indikatoren basierend auf den abgerufenen Daten.
4. Zeichnet ein Candlestick-Diagramm für die Analyse der Preisbewegungen.

Classes:
    ApiConfigReader: Liest API-Konfigurationsdaten aus einer externen Datei.
    BinanceClient: Dient als Schnittstelle zur Binance API.
    CandlestickChart: Visualisiert Handelsdaten in Candlestick-Diagrammen.
    TechnicalIndicators: Berechnet technische Indikatoren aus Handelsdaten.
"""

from classes.ApiConfigReader import ApiConfigReader
from classes.BinanceClient import BinanceClient
from classes.CandlestickChart import CandlestickChart
from classes.TechnicalIndicators import TechnicalIndicators
from classes.SendMessage import SendMessage
from classes.export import Export
from classes.sqlite import CoinChaosDB


import argparse
import sys



def main():
    """
    Hauptfunktion des Crypto-Projekts.

    Diese Funktion steuert den gesamten Prozess des Abrufens, Verarbeitens und Visualisierens 
    der Handelsdaten für eine spezifische Kryptowährung. Sie liest zunächst die API-Konfiguration, 
    initialisiert den BinanceClient, ruft die Handelsdaten ab, berechnet technische Indikatoren 
    und zeigt schließlich ein Candlestick-Diagramm an.

    Der Prozess umfasst folgende Schritte:
    1. Lesen der API-Konfigurationen aus einer externen Datei.
    2. Initialisieren des BinanceClients mit den gelesenen API-Schlüsseln.
    3. Definieren der Handelssymbol-, Intervall- und Tagesparameter für den Datenabruf.
    4. Abrufen der Handelsdaten vom Binance-Client.
    5. Berechnen technischer Indikatoren für die abgerufenen Daten.
    6. Visualisieren der Daten in einem Candlestick-Diagramm.
    """
    
    config_path = 'etc/config.txt'
    config_reader = ApiConfigReader(config_path)
    api_keys = config_reader.read_config()
    
    
    # Initalisiere Datenbank sqlite
    db = CoinChaosDB(api_keys.get('db_path') )
    
    # erstelle datenbank und Tabellen falls nicht vorhanden
    # db.delete_database()
    
    #db.install()  # nur am anfang aufrufen löscht alle tabellen !!!
    
    '''
    python main.py -m 1 -s=BTCUSDT -i=15m -b=30
    python main.py -m 1 -s=SOLUSDT -i=15m -b=30

    '''
    
    
    args =  parse_arguments()     #daten von der EIngabezeile einlesen
    
    # Standardwerte für die Entwicklung
    if args.mode == 0:
        #symbol = 'BTCUSDT'
        #symbol = 'MATICUSDT'
        symbol = 'RUNEUSDT'
        interval1 = '5m' # scalping chart
        interval2 = '1m' # für ausstieg beim scalpen
        balken = 50
    else:
        symbol = args.symbol
        interval = args.interval
        balken = args.balken


    #Initalisiere Klassen
    
    # Initalisiere binance
    binance_client = BinanceClient(
        api_keys.get('binance_api_key'), 
        api_keys.get('binance_secret_key'), 
        api_keys.get('time_zone'),
        db
        ) 
    
    # Initalisiere messenger    
    message_sender = SendMessage(api_keys.get('pushbullet_api'))    #initalisiere Message Dienst Pushbullet
    
    # commission abfragen
    #binance_client.get_commission()     #gebühren abfragen  
    #binance_client.show_commission('BNBUSDT') #anzeige der gebühren für alle symbole oder zu einem einzelnen
    #binance_client.get_funding_rate_history('BNBUSDT')
    #binance_client.list_symbols_by_commission('0')    # 0 keine gebühren <0   >0
    
    #initalisiere Technische Indikatoren
    technical_indicators = TechnicalIndicators(binance_client, db)
    
    
    ### start schleife
    
    binance_client.get_BinanceTime()

    
    
    # Daten von Binance abrufen und in DB speichern
    #binance_client.initialize_data()    #durch sqlite eine leere funktion
    
    # abruf der interval1 5min
    ret = binance_client.get_data_binance(
        symbol, 
        interval1, 
        balken 
        )  
    
    # abruf der interval2 1min
    ret = binance_client.get_data_binance(
        symbol, 
        interval2,   
        int(interval1[:-1]) * balken # 1min x5 um gleiche datenmenge zu erhalten)
        )  

    #Kerzen Farbe setzen
    technical_indicators.calculate_candle_color(symbol, interval1)   #5min kerzenfarbe berechnen
    
    
    #Vector candle berechnen
    technical_indicators.calc_vector_candles(symbol, interval1)      #5min vector candle berechnen  
    
    
    # EMA5 berechnen 
    technical_indicators.calculate_ema(5, symbol, interval1)    #5min Ema berechnen
    technical_indicators.calculate_ema(5, symbol, interval2)    #1min Ema berechnen
    
    
    # EMA13 berechnen 
    technical_indicators.calculate_ema(13, symbol, interval1)    #5min Ema berechnen
    technical_indicators.calculate_ema(13, symbol, interval2)    #1min Ema berechnen


    #EMA 50 berechnen
    technical_indicators.calculate_ema(50, symbol, interval1)    #5min Ema berechnen
    
    #EMA 100 berechnen
    technical_indicators.calculate_ema(100, symbol, interval1)    #5min Ema berechnen
    
    #EMA 200 berechnen
    technical_indicators.calculate_ema(200, symbol, interval1)    #5min Ema berechnen
    
    #EMA 800 berechnen
    technical_indicators.calculate_ema(800, symbol, interval1)    #5min Ema berechnen
    
    
    
    
    
   

    
    
    """
    technical_indicators.calculate_ema(5)
    technical_indicators.calculate_ema(13)
    technical_indicators.calculate_ema(50)
    technical_indicators.calculate_ema(100)
    technical_indicators.calculate_ema(200)
    technical_indicators.calculate_ema(800)
    
    
    
    technical_indicators.lower_low()                # suche das letzte tiefste tief
    technical_indicators.w_pattern()
    """
    
    
    
    
    #Frame Daten exportieren 
    #exporter = Export(binance_client.get_data(), 'exported_data.csv')
    #exporter.to_csv()

   
    title = "Programm Start"
    body = "Das ist eine Testbenachrichtigung von der SendMessage-Klasse."
    # Sende die Benachrichtigung
    #result = message_sender.send_notification(title, body)
    #result=message_sender.send_notification_with_image(title, body, "https://www.heise.de/select/ct/2018/21/1539404357063695/contentimages/image-1537944903544367.jpg")

    #Anzeige des Chart
   
    if args.mode == 0:  ## bei Live anzeige kein Chart anzeigen
        chart = CandlestickChart(binance_client)
        #chart.plot( symbol, interval, balken)
    else:
        #live Modus sende nachricht
        i=1
    

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crypto-Projekt-Modul')
    parser.add_argument('-m', '--mode', type=int, choices=[0, 1], default=0,
                        help='Setzen Sie den Modus: 0 für Entwicklung (Standard), 1 für Live')
    parser.add_argument('-s', '--symbol', type=str, default='BTCUSDT',
                        help='Handelssymbol, z.B. BNBUSDT')
    parser.add_argument('-i', '--interval', type=str, default='15m',
                        help='Intervall, z.B. 15m')
    parser.add_argument('-b', '--balken', type=int, default=50,
                        help='Anzahl der Balken, z.B. 30')

    args = parser.parse_args()
    return args



if __name__ == "__main__":
    main()
