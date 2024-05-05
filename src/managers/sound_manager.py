"""
Leafy Legions: SoundManager

This module contains the SoundManager class
for playing sounds and music in the application in the application
"""
# System Imports
import os
import sys

# Library Imports
import pygame


class SoundManager:
    """
    Functions to play sounds and music in the application
    """

    @staticmethod
    def play_music(music_file: str, volume: float = 0.05) -> None:
        """
        Play music

        Args:
            music_file (str): Name of the music file
            volume (float): Volume of the music (default = 0.05)

        Raises:
            FileNotFoundError: If no music is found
        """
        if getattr(sys, 'frozen', False):
            music_path = os.path.join(sys._MEIPASS, f"src/assets/music/{music_file}")
        else:
            music_path = f"src/assets/music/{music_file}"

        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        else:
            raise FileNotFoundError(f"No sound effect at {music_path}")

    @staticmethod
    def play_sound(effect_file: str, volume: float = 0.05) -> None:
        """
        Play sound effect

        Args:
            effect_file (str): Name of the sound effect file
            volume (float): Volume of the sound effect (default = 0.05)

        Raises:
            FileNotFoundError: If no sound is found
        """
        if getattr(sys, 'frozen', False):
            sound_path = os.path.join(sys._MEIPASS, f"src/assets/sounds/{effect_file}")
        else:
            sound_path = f"src/assets/sounds/{effect_file}"
        if os.path.exists(sound_path):
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(volume)
            sound.play()
        else:
            raise FileNotFoundError(f"No sound effect at {sound_path}")

