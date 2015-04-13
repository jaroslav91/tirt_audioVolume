#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import json
from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import InputMessageConnector, OutputMessageConnector #import modułów konektora msg_stream_connector
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector, OutputObjectConnector #import modułów konektora object_connector
from ComssServiceDevelopment.connectors.tcp.stream_connector import InputStreamConnector, OutputStreamConnector
from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi
import numpy as np #import modułu biblioteki Numpy


class AudioVolumeService(Service): #klasa usługi musi dziedziczyć po ComssServiceDevelopment.service.Service
    def __init__(self): #"nie"konstruktor, inicjalizator obiektu usługi
        super(AudioVolumeService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej
        self.filters = [] #zmienna do przechowywania wartości parametru
        self.filters_lock = threading.RLock() #obiekt pozwalający na blokadę wątku

    def declare_outputs(self): #deklaracja wyjść
        self.declare_output("audioOutput", OutputStreamConnector(self)) #deklaracja wyjścia "videoOutput" będącego interfejsem wyjściowym konektora msg_stream_connector
        self.declare_output("filtersOnOutput", OutputObjectConnector(self)) #deklaracja wyjścia "filtersOnOutput" będącego interfejsem wyjściowym konektora object_connector

    def declare_inputs(self):
        self.declare_input("audioInput", InputStreamConnector(self)) #deklaracja wejścia "videoInput" będącego interfejsem wyjściowym konektora msg_stream_connector
        self.declare_input("filtersOnInput", InputObjectConnector(self)) #deklaracja wejścia "filtersOnInput" będącego interfejsem wyjściowym konektora object_connector

    def watch_filters(self): #metoda obsługująca strumień sterujacy parametrem usługi
        filter_input = self.get_input("filtersOnInput") #obiekt interfejsu wejściowego
        filter_output = self.get_output("filtersOnOutput") #obiekt interfejsu wyjściowego
        while self.running(): #główna pętla wątku obsługującego strumień sterujący
            new_filters = filter_input.read() #odczyt danych z interfejsu wejściowego
            with self.filters_lock:  #blokada wątku
                self.filters = new_filters #ustawienie wartości parametru
            filter_output.send(new_filters) #przesłanie danych za pomocą interfejsu wyjściowego 

    def run(self): #główna metoda usługi
        threading.Thread(target=self.watch_filters).start() #uruchomienie wątku obsługującego strumień sterujący

        audio_input = self.get_input("audioInput") #obiekt interfejsu wejściowego
        audio_output = self.get_output("audioOutput") #obiekt interfejsu wyjściowego

        while self.running(): #pętla główna usługi (wątku głównego obsługującego strumień wideo)
            frame_obj = audio_input.read() #odebranie danych z interfejsu wejściowego
            frame = frame_obj #załadowanie ramki do obiektu NumPy
            with self.filters_lock: #blokada wątku
                current_filters = self.filters #pobranie aktualnej wartości parametru "filtersOn"
            print current_filters
            isFilter = current_filters["isFilter"]
            if 1 == isFilter: #sprawdzenie czy parametr "filtersOn" ma wartość 1, czyli czy ma być stosowany filtr
                value = current_filters["value"]
                frame = np.fromstring(frame, np.int16) / 10 * value
            audio_output.send(frame) #przesłanie ramki za pomocą interfejsu wyjściowego

if __name__=="__main__":
    sc = ServiceController(AudioVolumeService, "audioVolumeService.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi
