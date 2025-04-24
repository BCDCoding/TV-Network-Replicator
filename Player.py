import tkinter as tk
import types
import time
import subprocess
import os, sys
import scheduler
import cv2
import pygame
import moviepy as mp
from PIL import Image, ImageTk
class VideoPlayer:

    #initialize tkinter window class and create widgets
    def __init__(self, root, video_files):
        #root = name of main tkinter window
        self.root = root
        # list of video file paths
        self.video_files = video_files
        #starting index value for video_files
        self.current_video_index = 0

        self.label = tk.Label(root)
        self.label.pack()

        #calls method to begin playing videos
        self.play_next_video()

    def play_next_video(self):
        #method goes through every file in list
        if self.current_video_index < len(self.video_files):
            video_path = self.video_files[self.current_video_index]
            print(video_path)
            self.current_video_index += 1
            #plays currently loaded video path
            self.play_video(video_path, self.play_next_video)
        else:
            #window self terminates once list is finished
            self.root.quit()

    def play_video(self, video_path, callback):
        # Reduce memory usage by loading only video dimensions
        #ensure smoother playback by locking at 30 fps
        # Moviepy class variable of current video file read from path
        clip = mp.VideoFileClip(video_path, target_resolution=(720, 720)).with_fps(30)

        #Opencv2; read and open current video file from path
        cap = cv2.VideoCapture(video_path)

        # Extract and save audio separately
        audio_path = "temp_audio.mp3"
        clip.audio.write_audiofile(audio_path, logger=None, fps=44100, bitrate="64k")

        # pygame used for playing generated sound file
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        # Save current time in seconds
        start_time = time.time()
        fps = 30  # Ensure base FPS

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            elapsed_time = time.time() - start_time
            expected_frame = int(elapsed_time * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, expected_frame)

            frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            self.root.update()

            time.sleep(1 / fps)

        cap.release()
        pygame.mixer.music.stop()
        pygame.mixer.quit()  # Ensures the file is released

        # Remove temp audio file safely
        try:
            os.remove(audio_path)
        except PermissionError:
            print(f"Warning: Unable to delete {audio_path}, it may still be in use.")

        callback()


def install(package):
    subprocess.check_call([sys.executable ,"sudo", "pip", "install", package])

def imports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__


