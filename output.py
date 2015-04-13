#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk
import threading

from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import InputMessageConnector #import modułów konektora msg_stream_connector
from ComssServiceDevelopment.connectors.tcp.stream_connector import InputStreamConnector
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

import pyaudio
import numpy as np #import modułu biblioteki Numpy

service_controller = DevServiceController("audioVolumeService.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("audioOutput", InputStreamConnector(service_controller)) #deklaracja interfejsu wejściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WYJŚCIEM usługi, do której "zaślepka" jest podłączana
service_controller.declare_connection("filtersOnOutput", InputObjectConnector(service_controller)) #analogicznie jak wyżej dla drugiego interfejsu

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "server_output7.wav"
WIDTH = 2
frames = []

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)


def watch_filters(): 
    filter_input = service_controller.get_connection("filtersOnOutput")
    while True:
        new_filters = filter_input.read()

threading.Thread(target=watch_filters).start()

connection = service_controller.get_connection("audioOutput")

i=1
while True: #główna pętla programu
    obj = connection.read() #odczyt danych z interfejsu wejściowego
    data = obj #załadownaie ramki do obiektu NumPy
    i=i+1
    print i
    stream.write(data)

