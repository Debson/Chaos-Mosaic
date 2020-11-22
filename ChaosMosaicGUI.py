#########################################################################
# Author:               Michal Debski, Marcel Kowalczyk, Ivan Yanez     #
# Module:               Image Processing                                #
# College Programme:    DT211C (4th Year)                               #
# College:              TU Dublin                                       #
#########################################################################

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from ChaosMosaic import ChaosMosaic
from ttkthemes import ThemedStyle

class ChaosMosaicGui(ttk.Frame):
    def __init__(self):
        # Setup main window
        self._root = tk.Tk()
        self._root.geometry('1280x720')
        self._root.minsize(width=1280, height=720)
        self._outputImage = None

        # Set window style
        self._appStyle = ThemedStyle(self._root)
        self._appStyle.theme_use('equilux')

        # Setup class member variables
        self._outputImageTargetWidth = 800
        self._outputImageTargetHeight = 720
        self._currentCanvasWidth = self._outputImageTargetWidth
        self._currentCanvasHeight = self._outputImageTargetHeight

        # Create an instance of Chaos Mosaic algorithm
        self._chaosMosaicAPI = ChaosMosaic()

        # Create gui
        self._buildGUI()

    def _buildGUI(self):
        # Building the GUI. It includes creating necessary user controls
        # providing functionality to them and placing them correctly
        # within the frames using grid.

        self._root.title("Texture Synthesis Chaos Mosaic")
        self._root.resizable(width=True, height=True)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)

        ttk.Frame.__init__(self, self._root)
        self.grid(row=0, column=0, sticky='nswe')
        self.rowconfigure(0, weight=1)

        # Left side panel - options go here
        self.columnconfigure(0, weight=1)

        self._leftPanel = ttk.Frame(self)
        self._leftPanel.grid(row=0, column=0, sticky='nswe')
        self._leftPanel.columnconfigure(0, weight=1)
        # Stretch middle frame
        self._leftPanel.rowconfigure(2, weight=1)

        separatorMainPanel = tk.ttk.Separator(self, orient=tk.VERTICAL)
        separatorMainPanel.grid(row=0, column=1, sticky='ns', padx=0)

        paddingLeftFrameX = 5
        paddingLeftFrameY = 5

        # left panel top frame
        self._topFrame = ttk.Frame(self._leftPanel)
        self._topFrame.grid(row=0, column=0, sticky='nwe', padx=paddingLeftFrameX, pady=paddingLeftFrameY)
        self._topFrame.rowconfigure(0, weight=1)
        self._topFrame.columnconfigure(0, weight=1)
        separatorTopFrame = tk.ttk.Separator(self._leftPanel, orient=tk.HORIZONTAL)
        separatorTopFrame.grid(row=1, column=0, rowspan=1, sticky='nwe', pady=3)

        self._middleFrame = ttk.Frame(self._leftPanel)
        self._middleFrame.grid(row=2, column=0, sticky='nswe', padx=paddingLeftFrameX, pady=paddingLeftFrameY)
        self._middleFrame.columnconfigure(0, weight=1)
        separatorMiddleFrame = tk.ttk.Separator(self._leftPanel, orient=tk.HORIZONTAL)
        separatorMiddleFrame.grid(row=3, column=0, rowspan=1, sticky='swe', pady=3)

        self._bottomFrame = ttk.Frame(self._leftPanel)
        self._bottomFrame.grid(row=4, column=0, sticky='swe', padx=paddingLeftFrameX, pady=paddingLeftFrameY)
        self._bottomFrame.rowconfigure(0, weight=1)
        self._bottomFrame.columnconfigure(0, weight=1)

        # left panel top frame

        inputLabel = ttk.Label(self._topFrame, text="Input Image", anchor='center')
        inputLabel.grid(row=0, column=0, sticky='nwe')

        #image = Image.open("img/1.jpg")
        #resized = image.resize((64, 64), Image.ANTIALIAS)
        #self._inputImage = ImageTk.PhotoImage(resized)
        self._inputImageLabel = ttk.Label(self._topFrame, anchor="center")
        #self._inputImageLabel['image'] = self._inputImage
        self._inputImageLabel.grid(row=1, column=0, sticky='nwe', pady=5)

        self._uploadButton = ttk.Button(self._topFrame, text="Upload", command=self._onUploadImageButtonClickHandler)
        self._uploadButton.grid(row=2, column=0, sticky='nwe')
        separatorTopFrameBetween = ttk.Separator(self._topFrame, orient=tk.HORIZONTAL)
        separatorTopFrameBetween.grid(row=3, column=0, rowspan=1, sticky='nwe', pady=3)

        outputPathLabel = ttk.Label(self._topFrame, text="Output Image", anchor='center')
        outputPathLabel.grid(row=4, column=0, sticky='nwe')

        selectPathFrame = ttk.Frame(self._topFrame)
        selectPathFrame.grid(row=5, column=0, sticky='nwe')
        selectPathFrame.rowconfigure(0, weight=1)
        selectPathFrame.columnconfigure(1, weight=1)

        self._selectOutputPathButton = ttk.Button(selectPathFrame, text="Select Path",
                                                  command=self._onSelectOutputPathButtonClickHandler)
        self._selectOutputPathButton.grid(row=0, column=0, sticky='nswe')

        self._selectOutputPathLabel = ttk.Label(selectPathFrame, text=self._chaosMosaicAPI.getOutputImagePath(), anchor='center')
        self._selectOutputPathLabel.grid(row=0, column=1, sticky='nswe')

        outputImageWidthFrame = ttk.Frame(self._topFrame)
        outputImageWidthFrame.grid(row=6, column=0, sticky='nwe', pady=(10, 0))
        outputImageWidthFrame.rowconfigure(0, weight=1)
        outputImageWidthFrame.columnconfigure(0, weight=1)
        outputImageWidthFrame.columnconfigure(1, weight=1)

        outputImageWidthCaptionLabel = ttk.Label(outputImageWidthFrame, text="Width:",
                                                anchor='center')
        outputImageWidthCaptionLabel.grid(row=0, column=0, sticky='nswe')

        self._outputImageWidthLabelVar = tk.StringVar()
        self._outputImageWidthLabelVar.set(self._chaosMosaicAPI.getOutputImageSize()[0])
        self._outputImageWidthLabel = ttk.Entry(outputImageWidthFrame, textvariable=self._outputImageWidthLabelVar)
        self._outputImageWidthLabel.grid(row=0, column=1, sticky='nswe')

        outputImageHeightFrame = ttk.Frame(self._topFrame)
        outputImageHeightFrame.grid(row=7, column=0, sticky='nwe', pady=(10, 0))
        outputImageHeightFrame.rowconfigure(0, weight=1)
        outputImageHeightFrame.columnconfigure(0, weight=1)
        outputImageHeightFrame.columnconfigure(1, weight=1)

        outputImageHeightCaptionLabel = ttk.Label(outputImageHeightFrame, text="Height:",
                                                 anchor='center')
        outputImageHeightCaptionLabel.grid(row=0, column=0, sticky='nswe')

        self._outputImageHeightLabelVar = tk.StringVar()
        self._outputImageHeightLabelVar.set(self._chaosMosaicAPI.getOutputImageSize()[1])
        self._outputImageHeightLabel = ttk.Entry(outputImageHeightFrame, textvariable=self._outputImageHeightLabelVar)
        self._outputImageHeightLabel.grid(row=0, column=1, sticky='nswe')

        # left panel mid frame
        chaosMosaicLabel = ttk.Label(self._middleFrame, text="Chaos Mosaic Configuration",
                                                 anchor='center')
        chaosMosaicLabel.grid(row=0, column=0, sticky='nwe')

        # Iterations
        iterationsCountFrame = ttk.Frame(self._middleFrame)
        iterationsCountFrame.grid(row=1, column=0, sticky='nwe', pady=(10, 0))
        iterationsCountFrame.rowconfigure(0, weight=1)
        iterationsCountFrame.columnconfigure(0, weight=1)
        iterationsCountFrame.columnconfigure(1, weight=1)

        iterationsCountCaptionLabel = ttk.Label(iterationsCountFrame, text="Iterations Count:",
                                                  anchor='center')
        iterationsCountCaptionLabel.grid(row=0, column=0, sticky='nswe')

        self._iterationsCountLabelVar = tk.StringVar()
        self._iterationsCountLabelVar.set(self._chaosMosaicAPI.getIterationsCount())
        self._iterationsCountLabel = ttk.Entry(iterationsCountFrame, textvariable=self._iterationsCountLabelVar)
        self._iterationsCountLabel.grid(row=0, column=1, sticky='nswe')

        # Min tile patch size
        minPatchSizeFrame = ttk.Frame(self._middleFrame)
        minPatchSizeFrame.grid(row=2, column=0, sticky='nwe', pady=(10, 0))
        minPatchSizeFrame.rowconfigure(0, weight=1)
        minPatchSizeFrame.columnconfigure(0, weight=1)
        minPatchSizeFrame.columnconfigure(1, weight=1)

        minPatchSizeCaptionLabel = ttk.Label(minPatchSizeFrame, text="Min Tile Patch Size:",
                                                 anchor='center')
        minPatchSizeCaptionLabel.grid(row=0, column=0, sticky='nswe')

        self._minPatchSizeLabelVar = tk.StringVar()
        self._minPatchSizeLabelVar.set(self._chaosMosaicAPI.getMinTilePatchSize())
        self._minPatchSizeLabel = ttk.Entry(minPatchSizeFrame, textvariable=self._minPatchSizeLabelVar)
        self._minPatchSizeLabel.grid(row=0, column=1, sticky='nswe')



        # Max tile patch size
        maxPatchSizeFrame = ttk.Frame(self._middleFrame)
        maxPatchSizeFrame.grid(row=3, column=0, sticky='nwe', pady=(10, 0))
        maxPatchSizeFrame.rowconfigure(0, weight=1)
        maxPatchSizeFrame.columnconfigure(0, weight=1)
        maxPatchSizeFrame.columnconfigure(1, weight=1)

        maxPatchSizeCaptionLabel = ttk.Label(maxPatchSizeFrame, text="Max Tile Patch Size:",
                                             anchor='center')
        maxPatchSizeCaptionLabel.grid(row=0, column=0, sticky='nswe')

        self._maxPatchSizeLabelVar = tk.StringVar()
        self._maxPatchSizeLabelVar.set(self._chaosMosaicAPI.getMaxTilePatchSize())
        self._maxPatchSizeLabel = ttk.Entry(maxPatchSizeFrame, textvariable=self._maxPatchSizeLabelVar)
        self._maxPatchSizeLabel.grid(row=0, column=1, sticky='nswe')

        # left panel bottom frame
        self._saveToFileCheckboxState = tk.BooleanVar()
        self._saveToFileCheckboxState.set(self._chaosMosaicAPI.getSaveToFile())
        self._saveToFileCheckBox = ttk.Checkbutton(self._bottomFrame, text="Save Image", variable=self._saveToFileCheckboxState)
        self._saveToFileCheckBox.grid(row=0, column=0, sticky='we', pady=10)

        self._startButton = ttk.Button(self._bottomFrame, text="Start", command=self._onStartButtonClickHandler)
        self._startButton.grid(row=1, column=0, sticky='we', pady=5)


        # Right panel configuration
        self.columnconfigure(2, weight=5)

        paddingRightFrameX = 5
        paddingRightFrameY = 5
        self._rightPanel = ttk.Frame(self)
        self._rightPanel.grid(row=0, column=2, sticky='nswe')

        self._rightPanel.rowconfigure(1, weight=1)
        self._rightPanel.columnconfigure(0, weight=1)

        # Left panel information(top)
        self._outputInfoPanel = ttk.Frame(self._rightPanel)
        self._outputInfoPanel.grid(row=0, column=0, sticky='ns', padx=paddingRightFrameX, pady=paddingRightFrameY)

        self._outputImageLabel = ttk.Label(self._outputInfoPanel, text="Synthesized Texture preview")
        self._outputImageLabel.grid(row=0, column=0, sticky='nswe')

        # Left panel output image
        self._outputImagePanel = ttk.Frame(self._rightPanel)
        self._outputImagePanel.grid(row=1, column=0, sticky='nswe', padx=paddingRightFrameX, pady=paddingRightFrameY)

        self._outputImagePanel.rowconfigure(0, weight=1)
        self._outputImagePanel.columnconfigure(0, weight=1)

        self._outputImageCanvas = tk.Canvas(self._outputImagePanel, width=self._outputImageTargetWidth, height=self._outputImageTargetHeight)
        self._outputImageCanvas.grid(row=0, column=0)

        self._outputImagePlaceholderText = ttk.Label(self._outputImagePanel, text='Output texture', anchor='center')
        self._outputImagePlaceholderText.grid(row=0, column=0, sticky='nswe')

        self.pack(fill=tk.BOTH, expand=1)

    def _loadOutputImage(self):
        # Load synthesised texture and display it
        imgWidth, imgHeight = self._outputImage.size

        if self._outputImageTargetWidth < imgWidth or self._outputImageTargetHeight < imgHeight:
            self._outputImageCanvas.configure(width=self._outputImageTargetWidth, height=self._outputImageTargetHeight)
            resized = self._outputImage.resize((self._outputImageTargetWidth, self._outputImageTargetHeight), Image.ANTIALIAS)
            self._outputImageTk = ImageTk.PhotoImage(resized)
        else:
            self._outputImageCanvas.configure(width=imgWidth, height=imgHeight)
            self._outputImageTk = ImageTk.PhotoImage(self._outputImage)

        self._outputImageCanvas.create_image(0, 0, image=self._outputImageTk, anchor='nw')

    def _onStartButtonClickHandler(self):
        # Perform check if all parameters are valid
        if self._isConfigured() and self._readInputValues():
            self._chaosMosaicAPI.perform()
            self._outputImagePlaceholderText.grid_remove()
            self._outputImage = self._chaosMosaicAPI.getImage()
            print(self._outputImage.size)
            self._loadOutputImage()

    def _isConfigured(self):
        # Make sure that all user-specified values are correct

        if self._chaosMosaicAPI.getSampleImagePath() == '':
            tk.messagebox.showerror("Not configured!", "Sample image not provided!")
            return False
        elif self._chaosMosaicAPI.getOutputImagePath() == '':
            tk.messagebox.showerror("Not configured!", "Output image path is not configured!")
            return False

        return True

    def _readInputValues(self):
        # Make sure that all user-specified values are correct

        if not self._outputImageWidthLabelVar.get().isdigit():
            tk.messagebox.showerror("Incorrect value!", "Output image width must be a number!")
            return False
        outputImageWidth = int(self._outputImageWidthLabelVar.get())

        if not self._outputImageHeightLabelVar.get().isdigit():
            tk.messagebox.showerror("Incorrect value!", "Output image Height must be a number!")
            return False
        outputImageHeight = int(self._outputImageHeightLabelVar.get())

        if not self._iterationsCountLabelVar.get().isdigit():
            tk.messagebox.showerror("Incorrect value!", "Iterations count must be a number!")
            return False
        iterationsCount = int(self._iterationsCountLabelVar.get())

        if not self._minPatchSizeLabelVar.get().isdigit():
            tk.messagebox.showerror("Incorrect value!", "Min Patch size must be a number!")
            return False
        minPatchSize = int(self._minPatchSizeLabelVar.get())

        if not self._maxPatchSizeLabelVar.get().isdigit():
            tk.messagebox.showerror("Incorrect value!", "Max Patch size must be a number!")
            return False
        maxPatchSize = int(self._maxPatchSizeLabelVar.get())

        saveToFile = bool(self._saveToFileCheckboxState.get())

        # check bounds for output image width, height
        if outputImageWidth < self._inputImage.size[0] or outputImageHeight < self._inputImage.size[1]:
            tk.messagebox.showerror("Incorrect value!", "Output image size must be higher than sample image size!")
            return False

        # check bounds for patch size
        if minPatchSize > maxPatchSize:
            tk.messagebox.showerror("Incorrect value!", "Minimum patch size must be less than maximum patch size!")
            return False

        if minPatchSize > self._inputImageSize [0] or maxPatchSize > self._inputImageSize [0]:
            tk.messagebox.showerror("Incorrect value!", "Min and max patch size must be less than sample image size!")
            return False

        # At this point user-specified values are correct, algorithm instance can be set up
        self._chaosMosaicAPI.setOutputImageSize([outputImageWidth, outputImageHeight])
        self._chaosMosaicAPI.setIterationsCount(iterationsCount)
        self._chaosMosaicAPI.setMinTilePatchSize(minPatchSize)
        self._chaosMosaicAPI.setMaxTilePatchSize(maxPatchSize)
        self._chaosMosaicAPI.setSaveToFile(saveToFile)

        return True

    def _onUploadImageButtonClickHandler(self):
        # choose image from file selector and upload to input label
        fileNames = tk.filedialog.askopenfilenames(title='Please select an image...', filetypes=(("Image Files","*.jpg;*.png"),("All Files","*.*")))
        if fileNames:
            fileName = fileNames[0]
            img = Image.open(fileName)
            self._inputImageSize = img.size
            self._inputImage = img.resize((64, 64), Image.ANTIALIAS)
            self._inputImageTk = ImageTk.PhotoImage(self._inputImage)
            self._inputImageLabel['image'] = self._inputImageTk
            self._chaosMosaicAPI.setSampleImagePath(fileName)
            self._chaosMosaicAPI.loadSampleImage()
            self._minPatchSizeLabelVar.set(self._chaosMosaicAPI.getMinTilePatchSize())
            self._maxPatchSizeLabelVar.set(self._chaosMosaicAPI.getMaxTilePatchSize())

    def _onSelectOutputPathButtonClickHandler(self):
        dirName = tk.filedialog.askdirectory(title='Please select an output directory...')
        if dirName:
            self._selectOutputPathLabel.config(text=dirName)
            self._chaosMosaicAPI.setOutputImagePath(dirName)

    def show(self):
        self._root.mainloop()