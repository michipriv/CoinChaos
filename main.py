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


import argparse



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
    
    
    '''
    python main.py -m 1 -s=BTCUSDT -i=15m -b=30
    python main.py -m 1 -s=SOLUSDT -i=15m -b=30

    '''
    
    
    args =  parse_arguments()     #daten von der EIngabezeile einlesen
    
    # Standardwerte für die Entwicklung
    if args.mode == 0:
        symbol = 'BTCUSDT'
        symbol = 'MATICUSDT'
        interval = '1m'
        balken = 20
    else:
        symbol = args.symbol
        interval = args.interval
        balken = args.balken



    
    #Datum/ UTC setzen

    binance_client = BinanceClient(api_keys.get('binance_api_key'), api_keys.get('binance_secret_key'), 'Europe/Vienna') 
    message_sender = SendMessage(api_keys.get('pushbullet_api'))    #initalisiere Message Dienst Pushbullet
    
    # Daten abrufen und aufbereiten
    binance_client.initialize_data()
    binance_client.get_data_binance(symbol, interval,  balken )  # korrigierte Reihenfolge der Parameter
  
    #technische INdikatoren berechnen für die abgerufenen Daten und im Panda Framework abspeichern    
    
    #die technischen indikatoren gehören in dieser reihenfolge abgearbeitet sonst kann es zu logik fehen kommen
    # wenn in der grafik sachen aus ode reingeschaltet werden, trotzdem die indikatoren alle berechnen lassen
    # und in der candlestick klasse die funktionen aus oder einschalten in der main plot funktion: plot_candlestick()
    technical_indicators = TechnicalIndicators(binance_client)
    technical_indicators.calculate_ema(5)
    technical_indicators.calculate_ema(13)
    technical_indicators.calculate_ema(50)
    technical_indicators.calculate_ema(100)
    technical_indicators.calculate_ema(200)
    technical_indicators.calculate_ema(800)
    
    technical_indicators.calc_vector_candles()      #vector candle berechnen  
    technical_indicators.calculate_candle_color()   #kerzenfarbe berechnen
    technical_indicators.lower_low()            # suche das letzte tiefste tief
    technical_indicators.w_pattern()
    
    
    
    
    binance_client.print_data()         # Frame Data anzeigen
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
        chart.plot( symbol, interval, balken)
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
