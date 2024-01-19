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

    symbol = 'BTCUSDT'

    symbol = 'RNDRUSDT'
    interval = '4h'  # String für INterval 1m,3m,5m,1d, 1w, 1M
    days_ago = 50      # Integer für abzurufende Tage


    
    binance_client = BinanceClient(api_keys.get('api_key'), api_keys.get('secret_key'), 'Indian/Mahe')
    
    # Daten abrufen und aufbereiten
    binance_client.initialize_data()
    binance_client.get_data_binance(symbol, interval,  days_ago, )  # korrigierte Reihenfolge der Parameter
  
    #technische INdikatoren berechnen für die abgerufenen Daten und im Panda Framework abspeichern    
    
    technical_indicators = TechnicalIndicators(binance_client)
    technical_indicators.calculate_ema(5)
    technical_indicators.calculate_ema(13)
    technical_indicators.calculate_ema(50)
    technical_indicators.calculate_ema(100)
    technical_indicators.calculate_ema(200)
    technical_indicators.calculate_ema(800)
    
    technical_indicators.calc_vector_candles()      #vector candle berechnen
        
    technical_indicators.calculate_candle_color()   #kerzenfarbe berechnen
    
    #erst nach cnadle color ausführen "
    technical_indicators.lower_low()            # suche das letzte tiefste tief
    #technical_indicators.higher_high()            # suche das letzte tiefste tief
    technical_indicators.w_pattern()
    
    
    
    
    binance_client.print_data()         # Frame Data anzeigen
   
    
   #Anzeige des Chart
    chart = CandlestickChart(binance_client)
    chart.plot( symbol, interval, days_ago)
    
    
if __name__ == "__main__":
    main()
