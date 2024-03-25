"""
Leafy Legions Entities Module

This module is for importing each of the various entities (i.e. Plant)
"""

from .plant import Plant
from .zombie import Zombie
from .speedy_zombie import SpeedyZombie

__all__ = ['Plant', 'Zombie', 'SpeedyZombie']

print("Loaded Module: Entities")
