# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:20:33 2016

@author: Alex
"""

import pygame
import datetime
import sys
from pygame.locals import *

"""
import Adafruit_DHT
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

f_in = 3

GPIO.setup(f_in, GPIO.IN)
sensor = Adafruit_DHT.DHT22
sensor_gpio = 2
"""

pygame.init()

display_width = 800
display_height = 600



#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (150, 0, 0)
green = (0, 150, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
graywhite = (189, 216, 245)
thermometer_red = (213, 119, 119)
barometer_blue = (76, 155, 253)

#Fonts
largeText = pygame.font.SysFont("freeserif", 25, bold=1)
mediumText = pygame.font.SysFont("freeserif", 20, bold=1)
smallText = pygame.font.SysFont("freeserif", 15, bold=0)
smallTextb = pygame.font.SysFont("freeserif", 16, bold=1)
verysmallText = pygame.font.SysFont("freeserif", 12, bold=0)

#init clock
clock = pygame.time.Clock()

timenow = ""

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def txt(text, font, color, x, y, kill=False, killline=False, center=True):
    if kill is True:
        if center is True:
            if killline is False:
                TextSurf, TextRect = text_objects(text, font, color)
                TextRect.center = (x, y)
                pygame.draw.rect(screen, black, TextRect)
            else:
                TextSurf, TextRect = text_objects(text, font, color)
                pygame.draw.rect(screen, black, (0, y - 0.5 * TextRect[3], display_width, TextRect[3] + 20))

            TextSurf, TextRect = text_objects(text, font, color)
            TextRect.center = (x, y)
            screen.blit(TextSurf, TextRect)
        else:
            if killline is False:
                TextSurf, TextRect = text_objects(text, font, color)
                pygame.draw.rect(screen, black, (x, y, TextRect[2] + x, TextRect[3] + y))
            else:
                TextSurf, TextRect = text_objects(text, font, color)
                pygame.draw.rect(screen, black, (0, y, display_width, TextRect[3] + 20))

            TextSurf, TextRect = text_objects(text, font, color)
            screen.blit(TextSurf, (x, y))
    else:
        if center is True:
            TextSurf, TextRect = text_objects(text, font, color)
            TextRect.center = (x, y)
            screen.blit(TextSurf, TextRect)
        else:
            TextSurf, TextRect = text_objects(text, font, color)
            screen.blit(TextSurf, (x, y))

def button(msg, x, y, w, h, tc, frame=None, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        txt(msg, smallTextb, tc, (x + (w / 2)), (y + (h / 2)))
        if click[0] is 1 and action is not None:
            action()
            clock.tick(15)
    else:
        txt(msg, smallText, tc, (x + (w / 2)), (y + (h / 2)))

    if frame is not None:
        buttonbg = Background(frame, [x, y])
        screen.blit(buttonbg.image, buttonbg.rect)

def thermometerbar(x, y, annotation, temp):
    global temp_alert

    txt(str(annotation[0]), verysmallText, white, x+50, y+151, center=False)
    txt(str(annotation[1]), verysmallText, white, x+50, y+114, center=False)
    txt(str(annotation[2]), verysmallText, white, x+50, y+77, center=False)
    txt(str(annotation[3]), verysmallText, white, x+50, y+40, center=False)

    if temp >=18.8 and temp <= 22.6:
        diff = temp - 19.0
        pygame.draw.rect(screen, thermometer_red, (x + 10, (309-(diff*37.0)), 10, (23+(diff*37.0))))
        # pygame.draw.rect(screen, thermometer_red, (35, 272, 10, 60))

    elif temp < 18.8:
        pygame.draw.rect(screen, thermometer_red, (x + 10, 320, 10, 20))
        temp_alert = True

    elif temp > 22.6:
        pygame.draw.rect(screen, thermometer_red, (x + 10, 170, 10, 165))
        temp_alert = True

def barometerhand(x, y, annotation, hum):
    angle = (40.0 - hum) * 4.5
    image_zeiger = pygame.image.load("./skin/zeiger2.png").convert_alpha()
    image_rect = image_zeiger.get_rect(center=(x + 70, y + 70))
    image = pygame.transform.rotate(image_zeiger, angle)
    image_rect = image.get_rect(center=image_rect.center)
    screen.blit(image, image_rect)

    txt(str(annotation[0]), verysmallText, white, x + 16, y + 62, center=False)
    txt(str(annotation[1]), verysmallText, white, x + 32, y + 25, center=False)
    txt(str(annotation[2]), verysmallText, white, x + 62, y + 15, center=False)
    txt(str(annotation[3]), verysmallText, white, x + 93, y + 25, center=False)
    txt(str(annotation[4]), verysmallText, white, x + 109, y + 62, center=False)

def quitit():
    global running
    running = False


#init screen
screen = pygame.display.set_mode((display_width, display_height))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Fitotron surveillance")
back = Background("./skin/bg800x600.png", [0, 0])
screen.blit(back.image, back.rect)
temp = 18.6
hum = 40.0
running = True
temp_alert = False
ms_counter = 0
f_in_status = True

try:
    while running:
        screen.fill([255, 255, 255])
        screen.blit(back.image, back.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        button("Quit", (display_width-75), 25, 75, 40, white, action=quitit)

        thermometer = Background("./skin/thermo3.png", [50, 150])
        screen.blit(thermometer.image, thermometer.rect)
        thermometerbar(50, 150, [19, 20, 21, 22], temp)
        txt("%.1f" % temp, mediumText, white, 63, 370)
        temp += 0.2

        barometer = Background("./skin/baro2.png", [150, 200])
        screen.blit(barometer.image, barometer.rect)
        barometerhand(150, 200, [40, 50, 60, 70, 80], hum)
        txt("%.1f" % hum, mediumText, white, 217, 370)
        hum += 1.0

        txt("Fitotron Surveillance (V1.00)", largeText, graywhite, (display_width / 2), 30)
        txt("Chamber Parameter", smallTextb, white, 80, 100, center=False)
        txt("Water Supply:", mediumText, white, 600, 200)
        if f_in_status is True:
            txt("OK", largeText, green, 600, 240)
        else:
            txt("Refill!", largeText, bright_red, 600, 240)

        timenow = str(datetime.datetime.now())[0:19]
        txt(timenow, mediumText, graywhite, (display_width / 2), 60)

        if ms_counter == (10*60):
            ms_counter = 0
            #hum, temp = Adafruit_DHT.read_retry(sensor, sensor_gpio)
            #if GPIO.input(f_in):
                #f_in_status = True
            #else:
                #f_in_status = False

        pygame.display.update()
        clock.tick(1)

    pygame.quit()

except SystemExit:
    pygame.quit()
