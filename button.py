#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 18:10:05 2020

@author: jakub
"""
import pygame

class Button:
    def __init__(self, msg, x, y, width, height, color, onhover_color, action=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.onhover_color = onhover_color
        self.action = action
        self.pressed = False

    def draw(self, win):
        mouse = pygame.mouse.get_pos()
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(win, self.onhover_color, (self.x, self.y, self.width, self.height))

            self.check_action()
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(self.msg, smallText)
        textRect.center = ((self.x + (self.width / 2)), (self.y + (self.height / 2)))
        win.blit(textSurf, textRect)

    def check_action(self):
        click = pygame.mouse.get_pressed()
        if click[0] == 1 and self.action is not None and not self.pressed:
            self.action()
            self.pressed = True
        elif click[0] == 0 and self.pressed:
            self.pressed = False

black = (0, 0, 0)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
