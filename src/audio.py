import pygame


class AudioManager:
    def __init__(self):
        self._menu_song = pygame.mixer.Sound('res/sounds/music.wav')
        self._game_song = pygame.mixer.Sound('res/sounds/music2.wav')

    def play_menu(self):
        self._menu_song.play(-1)

    def stop_menu(self):
        self._menu_song.stop()

    def play_game(self):
        self._game_song.play(-1)

    def stop_game(self):
        self._game_song.stop()

    def pause_all(self):
        pygame.mixer.pause()