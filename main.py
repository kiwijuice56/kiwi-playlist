from os import listdir
from os.path import isfile, join

import pygame

import subprocess

from pynput import keyboard

import pystray
from PIL import Image, ImageDraw


playlist_url = "https://www.youtube.com/playlist?list=PL9ujewBhQLIvJOmZn9lWCyBSaLbDgdqmr"
ffmpeg_path = "C:\\Program Files\\ffmpeg"
song_path = "songs/"

song_files = []
song_idx = 0
paused = False


def stop_program():
    pygame.quit()
    quit()


def update_songs():
    subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0", "--ffmpeg-location", ffmpeg_path, "--download-archive", "../archive.txt", playlist_url], cwd=song_path)


def key_input(key):
    global paused
    global song_idx

    if not key:
        return

    if key == keyboard.Key.media_play_pause:
        paused = not paused
        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    song_changed = False

    if key == keyboard.Key.media_next:
        song_changed = True
        song_idx += 1
    if key == keyboard.Key.media_previous:
        song_changed = True
        song_idx -= 1
    song_idx = (len(song_files) + song_idx) % len(song_files)

    if song_changed:
        print(join(song_path, song_files[song_idx]))
        pygame.mixer.music.load(join(song_path, song_files[song_idx]))
        pygame.mixer.music.play()


    if key == keyboard.Key.esc:
        stop_program()


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


def main():
    # update_songs()

    global song_files
    song_files = [f for f in listdir(song_path) if isfile(join(song_path, f))]

    pygame.init()

    pygame.mixer.music.load(join(song_path, song_files[song_idx]))
    # pygame.mixer.music.play()


    with keyboard.Listener(on_press=key_input) as listener:
        listener.join()

    # In order for the icon to be displayed, you must provide an icon
    icon = pystray.Icon(
        'test name',
        icon=create_image(64, 64, 'black', 'white'))


    # To finally show your icon, call run
    icon.run()


if __name__ == "__main__":
    main()