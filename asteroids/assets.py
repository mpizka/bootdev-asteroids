import glob
import os.path as path

import pygame
import pygame.freetype as freetype

ASSETS = {}
FONT_ASSETS = {}


def _load_sprite_assets():
    extensions = ["png", "jpg"]
    assetfiles = glob.glob("assets/*.png") + glob.glob("assets/*.jpg")
    for filename in assetfiles:
        key = path.basename(filename)
        ASSETS[key] = pygame.image.load(filename)


def _load_font_assets():
    fontfiles = glob.glob("assets/*.ttf")
    for filename in fontfiles:
        key = path.basename(filename)
        FONT_ASSETS[key] = freetype.Font(filename)


def load():
    """Load all the game assets"""
    _load_sprite_assets()
    _load_font_assets()
