#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ComssServiceDevelopment.connectors.tcp.stream_connector import OutputStreamConnector
from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import OutputMessageConnector #import modułów konektora msg_stream_connector
from ComssServiceDevelopment.connectors.tcp.object_connector import OutputObjectConnector #import modułów konektora object_connector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

import pyaudio
import json
import Tkinter as tk #import modułu biblioteki Tkinter -- okienka

service_controller = DevServiceController("audioVolumeService.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("audioInput", OutputStreamConnector(service_controller)) #deklaracja interfejsu wyjściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WEJŚCIEM usługi, do której "zaślepka" jest podłączana
service_controller.declare_connection("filtersOnInput", OutputObjectConnector(service_controller)) #analogicznie jak wyżej dla interfesju sterującego

#record
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1


def update_all(root, stream, filters):
    #frames = []

    #for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        #data = stream.read(CHUNK)
       # frames.append(data)

  #  read_successful\
    frame = stream.read(CHUNK)#frames #odczyt obrazu z kamery
    new_filters = []
    checked_now = check1.get()
    if checked_now == 1: #sprawdzenie czy checkbox był zaznaczony
        print "changed: %d" % checked_now
        to_send = 1
        value =int(var1.get())
        m = {"isFilter": to_send, "value": value}
        new_filters = m
    else:
        print "changed: %d" % checked_now
        to_send = 0
        m = {"isFilter": to_send, "value": 1}
        new_filters = m


   # if filters ^ new_filters:
    #    filters.clear()
     #   filters.update(new_filters)
    service_controller.get_connection("filtersOnInput").send(new_filters) #wysłanie wartości parametru streującego w zależności od checkbox'a

    frame_dump = frame #zrzut ramki wideo do postaci ciągu bajtów
    service_controller.get_connection("audioInput").send(frame_dump) #wysłanie danych ramki wideo
    root.update()
    root.after(10, func=lambda: update_all(root, stream, filters))



def sel():
   selection = "Value = " + str(var1.get())
   label.config(text = selection)

root = tk.Tk()
root.title("Filters")  #utworzenie okienka

#stram z microphone
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("*recording")

var1 = tk.DoubleVar()
#obsługa checkbox'a
check1=tk.IntVar()
checkbox1 = tk.Checkbutton(root, text="Filter 1", variable=check1)
checkbox1.pack()





scale = tk.Scale( root, variable = var1 )
scale.pack(anchor=tk.CENTER)

button = tk.Button(root, text="Get Scale Value", command=sel)
button.pack(anchor=tk.CENTER)

label = tk.Label(root)
label.pack()


print("*packing")
root.after(0, func=lambda: update_all(root, stream, set())) #dołączenie metody update_all do głównej pętli programu, wynika ze specyfiki TKinter
root.mainloop()
