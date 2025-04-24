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
import Player as P




if __name__ == "__main__":
    # Create Main Window
    root = tk.Tk()
    root.title("Video Player")
    # Generate File Schedule
    video_files = scheduler.initalizer()

    # Playback files
    if video_files:
        #Main Player, OpenCV2 and Moviepy libraries. Controlled in 'Player' file
        player = P.VideoPlayer(root, video_files)
        root.mainloop()
