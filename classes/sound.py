"""Sound utilities that gracefully handle missing audio devices."""
import pygame

_audio_available = False


def init_audio():
    """Initialize audio system. Returns True if audio is available."""
    global _audio_available
    try:
        pygame.mixer.init()
        _audio_available = True
    except pygame.error:
        _audio_available = False
        print("Warning: No audio device found. Running in silent mode.")
    return _audio_available


def is_audio_available():
    return _audio_available


class DummySound:
    """A no-op sound object for when audio is unavailable."""
    def play(self):
        pass

    def set_volume(self, volume):
        pass

    def stop(self):
        pass


def load_sound(path):
    """Load a sound file, returning a DummySound if audio is unavailable."""
    if _audio_available:
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            return DummySound()
    return DummySound()


def load_music(path):
    """Load music for background playback."""
    if _audio_available:
        try:
            pygame.mixer.music.load(path)
        except pygame.error:
            pass


def play_music(loops=-1):
    """Play loaded music."""
    if _audio_available:
        try:
            pygame.mixer.music.play(loops)
        except pygame.error:
            pass


def stop_music():
    """Stop music playback."""
    if _audio_available:
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass


def set_music_volume(volume):
    """Set music volume."""
    if _audio_available:
        try:
            pygame.mixer.music.set_volume(volume)
        except pygame.error:
            pass


def set_num_channels(num):
    """Set number of mixer channels."""
    if _audio_available:
        try:
            pygame.mixer.set_num_channels(num)
            for i in range(num):
                channel = pygame.mixer.Channel(i)
                channel.set_volume(0.25)
        except pygame.error:
            pass
