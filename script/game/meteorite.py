from turtle import speed
import pygame

class Meteorite():
    # cette class gere les meteorites qui tombent du ciel
    def __init__(self, speed):
        self.sprite = ""
        self.speed = speed