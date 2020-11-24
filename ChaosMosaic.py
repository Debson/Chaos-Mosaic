#########################################################################
# Author:               Michal Debski, Marcel Kowalczyk, Ivan Yanez     #
# Module:               Image Processing                                #
# College Programme:    DT211C (4th Year)                               #
# College:              TU Dublin                                       #
#########################################################################

import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from random import randint, choice
from PIL import Image
import cv2
from enum import Enum
import string


class TilePatchSelectMethodType(Enum):
    Random = 1,
    UserSpecified = 2

class ChaosMosaic:
    def __init__(self):
        self._keepTilePatchToSampleImageAspectRatio = False
        self._sampleImgPath = ""
        self._outputImagePath = "out/"
        self._outputImageTargetSize = [512, 512]
        self._tilePatchSelectMethodType = TilePatchSelectMethodType.Random
        self._minTilePatchSize = 0
        self._maxTilePatchSize = 0
        self._iterationsCount = 900
        self._saveOutputImageToFile = True

    def perform(self):
        # Perform the algorithm
        # First step: Generate an output image matrix, that is composed from
        #             sample images as tiles.
        #             Output image matrix size must be multiplication of sample
        #             image size, e.g. sample image size is [50, 50],
        #             target size is [512, 512], so output matrix size
        #             must be multiplication of the sample image size
        #             but cannot be smaller than the target size.
        #             It means that in this case output image matrix will have size
        #             [550, 550] => [11 * 50, 11 * 50]
        #
        self._outputImage = self._constructTileMatrix()

        for iteration in range(0, self._iterationsCount):
            # Second step: From output matrix, randomly select a tile.
            #              Tile is an image with its original position
            #              and size on the output matrix image.
            #              Tile is always the same size as sample image
            #              Simply because it's a one entry of output image matrix

            randomTile = self._getRandomTile()

            # Third step: From random tile select a random patch.
            #             Random patch is a rectangle selected from
            #             a tile, which has size based on user input,
            #             but never exceeds tile's size.
            randomTilePatch = self._getRandomTilePatch(randomTile)

            # Fourth Step: Insert random tile patch at random location
            #              on the output image matrix.

            self._insertTilePatchAtRandomLocation(randomTilePatch)

            # Repeat the process

        # Save image to file
        self._outputImage = self._outputImage[0:self._outputImageTargetSize[0], 0:self._outputImageTargetSize[1]]
        if self._saveOutputImageToFile:
            name = self.getRandomString()
            img = Image.fromarray(np.uint8(self._outputImage * 255))
            img.save(self._outputImagePath + name +'.jpg')

    def getRandomString(self):
        # generates random string for output name
        letters = string.ascii_lowercase
        name = ''.join(choice(letters) for i in range(10))
        return name

    def loadSampleImage(self):
        # Read sample image from file
        self._sampleImage = cv2.imread(self._sampleImgPath)
        self._sampleImage = cv2.cvtColor(self._sampleImage, cv2.COLOR_BGR2RGB)

        # Normalize the image
        self._sampleImage = self._sampleImage / 255.0

        # Extract height, width and channels of sample image
        self._sampleImageHeight, self._sampleImageWidth, self._sampleImageChannels = np.shape(self._sampleImage)

        self._minTilePatchSize = 0
        self._maxTilePatchSize = self._sampleImageWidth

    def _constructTileMatrix(self):
        # Construct matrix that will be composed from sample images
        # that will serve as base output image

        self._outputImageWidthMultiplier = ceil(self._outputImageTargetSize[0] / self._sampleImageWidth)
        self._outputImageHeightMultiplier = ceil(self._outputImageTargetSize[1] / self._sampleImageHeight)
        self._outputImageWidth = self._sampleImageHeight * self._outputImageWidthMultiplier
        self._outputImageHeight = self._sampleImageWidth * self._outputImageHeightMultiplier

        # Create an empty image with specified size and channels
        outputImg = np.zeros(
            (self._outputImageWidth,
             self._outputImageHeight, self._sampleImageChannels), dtype=np.float64)

        # Fill empty image with tiles(sample image as one tile)
        for rowIndex in range(0, self._outputImageHeightMultiplier, ):
            for colIndex in range(0, self._outputImageWidthMultiplier, ):
                outputImg[self._sampleImageWidth * colIndex: self._sampleImageWidth * (colIndex + 1),
                self._sampleImageHeight * rowIndex: self._sampleImageHeight * (rowIndex + 1)] = self._sampleImage

        return outputImg

    def _getRandomTile(self):
        # Randomly determine the position of tile
        maxTilesHorizontalCount = self._outputImageWidth / self._sampleImageWidth
        maxTilesVerticalCount = self._outputImageHeight / self._sampleImageHeight

        randomTileHorizontalIndex = randint(0, maxTilesHorizontalCount - 1)
        randomTileVerticalIndex = randint(0, maxTilesVerticalCount - 1)

        randomTileLeft = self._sampleImageWidth * randomTileHorizontalIndex
        randomTileRight = self._sampleImageWidth * (randomTileHorizontalIndex + 1)
        randomTileTop = self._sampleImageHeight * randomTileVerticalIndex
        randomTileBottom = self._sampleImageHeight * (randomTileVerticalIndex + 1)

        # Get tile from output image matrix
        randomTile = self._outputImage[randomTileLeft:randomTileRight, randomTileTop:randomTileBottom]

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

        randomTilePatch = tile[randomTileX:randomTileX + randomTileWidth, randomTileY:randomTileY + randomTileHeight]

        return randomTilePatch

    def _insertTilePatchAtRandomLocation(self, tilePatch):
        # Determine valid random location on the output image
        # and insert tile patch at that location

        tilePatchWidth, tilePatchHeight, tilePatchChannels = np.shape(tilePatch)

        randomOutputImageX = randint(0, self._outputImageWidth - tilePatchWidth)
        randomOutputImageY = randint(0, self._outputImageHeight - tilePatchHeight)

        self._outputImage[randomOutputImageX:randomOutputImageX + tilePatchWidth,
        randomOutputImageY:randomOutputImageY + tilePatchHeight] = tilePatch

    def _showImage(self, image):
        # Helper function to show the image
        plt.imshow(image)
        plt.show()

    # Getters and setters for class variable members
    def getSampleImagePath(self):
        return self._sampleImgPath

    def setSampleImagePath(self, sampleImagePath):
        self._sampleImgPath = sampleImagePath

    def setSampleImage(self, sampleImage):
        self._sampleImage = sampleImage

    def getOutputImagePath(self):
        return self._outputImagePath

    def setOutputImagePath(self, outputImagePath):
        self._outputImagePath = outputImagePath

    def getOutputImageSize(self):
        return self._outputImageTargetSize

    def setOutputImageSize(self, outputImageSize):
        self._outputImageTargetSize = outputImageSize

    def setKeepTilePatchToSampleImageAspectRatio(self, val):
        self._keepTilePatchToSampleImageAspectRatio = val

    def getMinTilePatchSize(self):
        return self._minTilePatchSize

    def setMinTilePatchSize(self, minTilePathSize):
        self._minTilePatchSize = minTilePathSize

    def getMaxTilePatchSize(self):
        return self._maxTilePatchSize

    def setMaxTilePatchSize(self, maxTilePathSize):
        self._maxTilePatchSize = maxTilePathSize

    def setTilePatchSizeFactor(self, factor):
        self._minTilePatchSizeFactor = factor

    def setTilePatchSelectMethodType(self, tilePatchSelectMethodType):
        self._tilePatchSelectMethodType = tilePatchSelectMethodType

    def getSaveToFile(self):
        return self._saveOutputImageToFile

    def setSaveToFile(self, val):
        self._saveOutputImageToFile = val

    def getIterationsCount(self):
        return self._iterationsCount

    def setIterationsCount(self, interationsCount):
        self._iterationsCount = interationsCount

    def getImage(self):
        return Image.fromarray(np.uint8(self._outputImage * 255))

        return 0
