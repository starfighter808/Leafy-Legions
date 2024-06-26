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
    def __init__(self):
        """
        Initialize a SoundManager object.
        """
        pygame.mixer.init()
        self.paused = False
        self.muted = False
        self.volume = 0.05
        self.currently_playing = None

    def play_music(self, music_file: str, volume: float = 0.05) -> None:
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
            if self.currently_playing != music_path:
                self.volume = volume
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self.currently_playing = music_path
        else:
            raise FileNotFoundError(f"No music file at {music_path}")

    def play_sound(self, effect_file: str, volume: float = 0.05) -> None:
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
            if not self.muted:
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(volume)
                sound.play()
        else:
            raise FileNotFoundError(f"No sound effect at {sound_path}")

    def toggle_music(self, option: bool = None) -> None:
        """
        Pause music
        """
        if option is not None:
            self.paused = option
            if self.paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        else:
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            self.paused = not self.paused

    def mute_sounds(self, option: bool = None) -> None:
        """
        Mute music
        """
        if option is not None:
            self.muted = option
            if self.muted:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.volume)
        else:
            if self.muted:
                pygame.mixer.music.set_volume(self.volume)
            else:
                pygame.mixer.music.set_volume(0)
            self.muted = not self.muted

    def reset(self) -> None:
        """
        Resets the sound manager state
        """
        self.toggle_music(False)
        self.mute_sounds(False)
        self.currently_playing = None
