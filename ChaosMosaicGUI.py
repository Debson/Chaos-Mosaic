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

        Frame.__init__(self, root)
        self.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)


        # Left side panel - options go here
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._leftPanel = Frame(self)
        self._leftPanel.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E)



        # Right panel configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._rightPanel = Frame(self)
        self._rightPanel.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E)

        self._rightPanel.rowconfigure(1, weight=1)
        self._rightPanel.columnconfigure(0, weight=1)

        self._outputInfoPanel = Frame(self._rightPanel)
        self._outputInfoPanel.grid(row=0, column=0, sticky=tk.N + tk.S)

        self._outputImageLabel = Label(self._outputInfoPanel, text="Synthesized Texture")
        self._outputImageLabel.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

        self._outputImagePanel = Frame(self._rightPanel)
        self._outputImagePanel.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E)

        self._outputImagePanel.rowconfigure(0, weight=1)
        self._outputImagePanel.columnconfigure(0, weight=1)

        self._outputImage = Image.open("out/out.jpg")
        self._outputImageTk = ImageTk.PhotoImage(self._outputImage)
        self._outputImageCanvas = Canvas(self._outputImagePanel, bd=0, highlightthickness=0)
        self._outputImageCanvas.create_image(0, 0, image=self._outputImageTk, anchor=tk.NW, tags="IMG")
        self._outputImageCanvas.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.pack(fill=tk.BOTH, expand=1)

        self._rightPanel.bind("<Configure>", self.resize2)

    def resize2(self, event):
        size = (event.width, event.height)

        resized = self._outputImage.resize(size, Image.ANTIALIAS)
        self._outputImageTk = ImageTk.PhotoImage(resized)
        self._outputImageCanvas.delete("IMG")
        self._outputImageCanvas.create_image(0, 0, image=self._outputImageTk, anchor=tk.NW, tags="IMG")

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