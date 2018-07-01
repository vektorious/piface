#!/usr/bin/python
# coding: utf8

import RPi.GPIO as GPIO
import subprocess
from subprocess import check_output
from re import findall
import Adafruit_DHT
from time import sleep, strftime, time, asctime
import matplotlib.pyplot as plt

LCD_RS = 25
LCD_E = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22

sensor = Adafruit_DHT.DHT22
gpio = 4

def write_log(temp, hum):
        name = "/home/pi/templog_data/flat_parameter_{0}.csv".format(strftime("%Y-%m-%d"))
        with open(name, "a") as log:
                log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(temperature), str(humidity)))

while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        temperature = float("{0:.3f}".format(temperature))
        humidity = float("{0:.3f}".format(humidity))
        write_log(temperature, humidity)
        print "flat_parameter_{0}.csv".format(strftime("%Y-%m-%d"))
        print("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(temperature), str(humidity)))

        zeile1 = asctime()
        zeile2 = "T={0}'C H={1}%".format(temperature, humidity)

        lcd_anzeige(zeile1, zeile2)

        sleep(60)