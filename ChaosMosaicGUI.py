import cv2
import easygui
import numpy as np
import tkinter as tk
from tkinter import filedialog, Tk, Frame, Label, Canvas, Button
from PIL import Image, ImageTk


class ChaosMosaicGui(Frame):
    def __init__(self, root):
        self._root = root
        self._root.title("Texture Synthesis Chaos Mosaic")
        self._root.resizable(width=True, height=True)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)

        Frame.__init__(self, root)
        self.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S + tk.W)
        self.rowconfigure(0, weight=1)


        # Left side panel - options go here
        self.columnconfigure(0, weight=1)

        self._leftPanel = Frame(self, highlightbackground="black", highlightthickness=1)
        self._leftPanel.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self._leftPanel.rowconfigure(1, weight=1)
        self._leftPanel.columnconfigure(0, weight=1)

        # left panel top frame
        self._topFrame = Frame(self._leftPanel)
        self._topFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self._middleFrame = Frame(self._leftPanel)
        self._middleFrame.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self._bottomFrame = Frame(self._leftPanel)
        self._bottomFrame.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self._inputLabel = Label(self._topFrame, text="Input Image")
        self._inputLabel.pack()
        load = Image.open("1.jpg")
        render = ImageTk.PhotoImage(load)
        self._inputImage = Label(self._topFrame, image=render)
        self._inputImage.image = render
        self._inputImage.pack(pady=5)

        # !!! Upload callback not added !!!
        self._uploadButton = tk.Button(self._topFrame, text="Upload", width=10)
        self._uploadButton.pack(pady=5)

        # left panel mid frame
        self._inputLabel = Label(self._topFrame, text="MIDDLE OPTIONS")
        self._inputLabel.pack(pady=90)

        # left panel bot frame
        self._checkBoxState = tk.IntVar()
        self._saveCheckBox = tk.Checkbutton(self._topFrame, text="Save Image", variable=self._checkBoxState)
        self._saveCheckBox.pack(pady=5)

        self._startButton = tk.Button(self._topFrame, text="Start", width=10)
        self._startButton.pack(pady=5)

        # Right panel configuration
        self.columnconfigure(1, weight=4)

        self._rightPanel = Frame(self, highlightbackground="black", highlightthickness=1)
        self._rightPanel.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self._rightPanel.rowconfigure(1, weight=1)
        self._rightPanel.columnconfigure(0, weight=1)

        self._outputInfoPanel = Frame(self._rightPanel)
        self._outputInfoPanel.grid(row=0, column=0, sticky=tk.N + tk.S)

        self._outputImageLabel = Label(self._outputInfoPanel, text="Synthesized Texture")
        self._outputImageLabel.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S + tk.W)

        self._outputImagePanel = Frame(self._rightPanel)
        self._outputImagePanel.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=5, pady=5)

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