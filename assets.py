import glob
import os.path as path

import pygame

ASSETS = {}


def load():
    """Load all the game assets"""
    assetfiles = glob.glob("assets/*")
    for filename in assetfiles:
        key = path.basename(filename)
        ASSETS[key] = pygame.image.load(filename)
