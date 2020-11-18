import numpy as np
import matplotlib.pyplot as plt
from math import floor, ceil
from random import randint
from PIL import Image
import cv2
from enum import Enum
import tkinter


class TilePatchSelectMethodType(Enum):
    Random = 1,
    UserSpecified = 2

class ChaosMosaic:
    def __init__(self):
        self._keepTilePatchToSampleImageAspectRatio = False
        self._sampleImgPath = ""
        self._outputImagePath = ""
        self._outputImageSize = [512, 512]
        self._tilePatchSelectMethodType = TilePatchSelectMethodType.Random
        self._minTilePatchSize = 0
        self._maxTilePatchSize = 0

    def initialize(self):
        self._loadImage()

    def setSampleImagePath(self, sampleImagePath):
        self._sampleImgPath = sampleImagePath

    def setOutputImagePath(self, outputImagePath):
        self._outputImagePath = outputImagePath

    def setOutputImageSize(self, outputImageSize):
        self._outputImageSize = outputImageSize

    def setKeepTilePatchToSampleImageAspectRatio(self, val):
        self._keepTilePatchToSampleImageAspectRatio = val

    def setMinTilePatchSize(self, minTilePathSize):
        self._minTilePatchSize = minTilePathSize

    def setMaxTilePatchSize(self, maxTilePathSize):
        self._maxTilePatchSize = maxTilePathSize

    def setTilePatchSizeFactor(self, factor):
        self._minTilePatchSizeFactor = factor

    def setTilePatchSelectMethodType(self, tilePatchSelectMethodType):
        self._tilePatchSelectMethodType = tilePatchSelectMethodType

    def perform(self, iterations=1, saveToFile=True):
        self._outputImage = self._constructTileMatrix()

        for iteration in range(0, iterations):
            randomTile = self._getRandomTile()
            randomTilePatch = self._getRandomTilePatch(randomTile)
            self._insertTilePatchAtRandomLocation(randomTilePatch)

        self._outputImage = self._outputImage[0:self._outputImageTargetSize[0], 0:self._outputImageTargetSize[1]]
        if saveToFile:
            img = Image.fromarray(np.uint8(self._outputImage * 255))
            img.save(self._outputImagePath + 'out.jpg')

    def _loadImage(self):
        # Read sample image from file
        self._sampleImage = cv2.imread(self._sampleImgPath)
        self._sampleImage = cv2.cvtColor(self._sampleImage, cv2.COLOR_BGR2RGB);

        # Normalize the image
        self._sampleImage = self._sampleImage / 255.0

        # Extract height, width and channels of sample image
        self._sampleImageHeight, self._sampleImageWidth, self._sampleImageChannels = np.shape(self._sampleImage)

    def _constructTileMatrix(self):
        # Construct matrix that will be composed from sample images
        # that will serve as base output image

        self._outputImageWidthMultiplier = ceil(self._outputImageTargetSize[0] / self._sampleImageWidth)
        self._outputImageHeightMultiplier = ceil(self._outputImageTargetSize[1] / self._sampleImageHeight)
        self._outputImageWidth = self._sampleImageHeight * self._outputImageWidthMultiplier
        self._outputImageHeight = self._sampleImageWidth * self._outputImageHeightMultiplier

        outputImg = np.zeros(
            (self._outputImageWidth,
             self._outputImageHeight, self._sampleImageChannels), dtype=np.float64)

        for rowIndex in range(0, self._outputImageHeightMultiplier, ):
            for colIndex in range(0, self._outputImageWidthMultiplier, ):
                outputImg[self._sampleImageHeight * rowIndex: self._sampleImageHeight * (rowIndex + 1),
                self._sampleImageWidth * colIndex: self._sampleImageWidth * (colIndex + 1)] = self._sampleImage

        return outputImg

    def _getRandomTile(self):
        # Determine position of complete random tile and copy it

        maxTilesHorizontalCount = self._outputImageWidth / self._sampleImageWidth
        maxTilesVerticalCount = self._outputImageHeight / self._sampleImageHeight

        randomTileHorizontalIndex = randint(0, maxTilesHorizontalCount - 1)
        randomTileVerticalIndex = randint(0, maxTilesVerticalCount - 1)

        randomTileLeft = self._sampleImageHeight * randomTileHorizontalIndex
        randomTileRight = self._sampleImageHeight * (randomTileHorizontalIndex + 1)
        randomTileTop = self._sampleImageHeight * randomTileVerticalIndex
        randomTileBottom = self._sampleImageHeight * (randomTileVerticalIndex + 1)
        randomTile = self._outputImage[randomTileTop:randomTileBottom, randomTileLeft:randomTileRight]

        return randomTile

    def _getRandomTilePatch(self, tile):
        # Get a random rectangular shape within the tile
        # basing on specified parameters

        tileHeight, tileWidth, tileChannels = np.shape(tile)

        randomTileWidth = randint(self._minTilePatchSize, self._maxTilePatchSize)
        randomTileHeight = randint(self._minTilePatchSize, self._maxTilePatchSize)

        if self._keepTilePatchToSampleImageAspectRatio:
            randomTileHeight = randomTileWidth

        randomTileX = randint(0, tileWidth - randomTileWidth)
        randomTileY = randint(0, tileHeight - randomTileHeight)

        print("Random Tile Patch (X: %d, Y: %d) (W:%d, H: %d)"
              % (randomTileX, randomTileY, randomTileWidth, randomTileHeight))

        randomTilePatch = tile[randomTileY:randomTileY + randomTileHeight, randomTileX:randomTileX + randomTileHeight]

        return randomTilePatch

    def _insertTilePatchAtRandomLocation(self, tilePatch):
        # Determine valid random location on the output image
        # and insert tile patch at that location

        tilePatchHeight, tilePatchWidth, tilePatchChannels = np.shape(tilePatch)

        randomOutputImageX = randint(0, self._outputImageWidth - tilePatchWidth)
        randomOutputImageY = randint(0, self._outputImageHeight - tilePatchHeight)

        print("Tile inserted at: (%d, %d):" % (randomOutputImageX, randomOutputImageY))

        self._outputImage[randomOutputImageY:randomOutputImageY + tilePatchHeight,
        randomOutputImageX:randomOutputImageX + tilePatchWidth] = tilePatch

    def _showImage(self, image):
        # Helper function to show the image
        plt.imshow(image)
        plt.show()

        return 0


class ChaosMosaicGUI:
    def __init__(self):
        self.chaosMosaicAPI = ChaosMosaic()
        self.chaosMosaicAPI.setSampleImagePath('img/1.jpg')
        self.chaosMosaicAPI.setOutputImageSize('out/')
        self.chaosMosaicAPI.setOutputImageSize([512, 512])

    def show(self):
        self._window = tkinter.Tk()
        self._window.title("Chaos Mosaic")
        self._startButton =


        m.mainloop()


chaosMosaicGUI = ChaosMosaicGUI()
chaosMosaicGUI.show()
