import cv2
import easygui
import numpy as np
import tkinter as tk
from tkinter import filedialog, Tk, Frame, Label, Canvas
from PIL import Image, ImageTk


class ChaosMosaicGui(Frame):
    def __init__(self, root):
        self._root = root
        self._root.title("Texture Synthesis Chaos Mosaic")
        self._root.resizable(width=True, height=True)

        # Left side panel - options go here
        self._optionsFrame = Frame(self._root)



        # Output image file panel
        self._outputImageFrame = Frame(self._root)
        self._outputImageFrame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

        self._outputImageFrame.rowconfigure(0, weight=1)
        self._outputImageFrame.columnconfigure(0, weight=1)

        self._original = Image.open("out/out.jpg")
        self._image = ImageTk.PhotoImage(self._original )
        self._display = Canvas(self._outputImageFrame, bd=0, highlightthickness=0)
        self._display.create_image(0, 0, image=self._image, anchor=tk.NW, tags="IMG")

        self._display.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        self._outputImageFrame.pack(fill=tk.BOTH, expand=1)

        self._display.bind("<Configure>", self.resize)

    def resize(self, event):
        size = (event.width, event.height)

        resized = self._original.resize(size, Image.ANTIALIAS)
        self._image = ImageTk.PhotoImage(resized)
        self._display.delete("IMG")
        self._display.create_image(0, 0, image=self._image, anchor=tk.NW, tags="IMG")

    def _uploadImage(self):
        # choose image from file selector and upload to input label
        print('test')
        fileNames = filedialog.askopenfilenames(title='Please an image...')
        print(fileNames)
        if fileNames:
            fileName = fileNames[0]
            img = Image.open(fileName)
            img = ImageTk.PhotoImage(img)

    def show(self):
        self._root.mainloop()

root = Tk()
gui = ChaosMosaicGui(root)
root.mainloop()