import numpy as np
import matplotlib.pyplot as plt
from skimage import io, feature, transform

from math import floor, ceil
from random import randint, gauss
import cv2
from PIL import Image


class ChaosMosaic:
    def __init__(self, sampleImagePath, outputImagePath, outputImageSize):
        self.sampleImgPath = sampleImagePath
        self.outputImagePath = outputImagePath
        self.outputImageTargetSize = outputImageSize

        self._loadImage()

        self.minTilePatchSizeFactor = 0.5
        self.minTilePatchWidth = floor(self.sampleImageWidth * self.minTilePatchSizeFactor)
        self.minTilePatchHeight = floor(self.sampleImageHeight * self.minTilePatchSizeFactor)

        self.maxTilePatchSizeFactor = 0.8
        self.maxTilePatchWidth = floor(self.sampleImageWidth * self.maxTilePatchSizeFactor)
        self.maxTilePatchHeight = floor(self.sampleImageHeight * self.maxTilePatchSizeFactor)

        self.keepTilePatchToSampleImageAspectRatio = False

    def perform(self, iterations=1, saveToFile=True):
        self.outputImage = self._constructTileMatrix()

        for iteration in range(0, iterations):
            randomTile = self._getRandomTile()
            randomTilePatch = self._getRandomTilePatch(randomTile)
            self._insertTilePatchAtRandomLocation(randomTilePatch)

        self.outputImage = self.outputImage[0:self.outputImageTargetSize[0], 0:self.outputImageTargetSize[1]]
        if saveToFile:
            img = Image.fromarray(np.uint8(self.outputImage * 255))
            img.save(self.outputImagePath + 'out.jpg')

    def _loadImage(self):
        # Read sample image from file
        self.sampleImage = cv2.imread(self.sampleImgPath)
        self.sampleImage = cv2.cvtColor(self.sampleImage, cv2.COLOR_BGR2RGB);

        # Normalize the image
        self.sampleImage = self.sampleImage / 255.0

        # Extract height, width and channels of sample image
        self.sampleImageHeight, self.sampleImageWidth, self.sampleImageChannels = np.shape(self.sampleImage)

    def _constructTileMatrix(self):
        # Construct matrix that will be composed from sample images
        # that will serve as base output image

        self.outputImageWidthMultiplier = ceil(self.outputImageTargetSize[0] / self.sampleImageWidth)
        self.outputImageHeightMultiplier = ceil(self.outputImageTargetSize[1] / self.sampleImageHeight)
        self.outputImageWidth = self.sampleImageHeight * self.outputImageWidthMultiplier
        self.outputImageHeight = self.sampleImageWidth *  self.outputImageHeightMultiplier

        outputImg = np.zeros(
            (self.outputImageWidth,
             self.outputImageHeight, self.sampleImageChannels), dtype=np.float64)

        for rowIndex in range(0, self.outputImageHeightMultiplier, ):
            for colIndex in range(0,  self.outputImageWidthMultiplier, ):
                outputImg[self.sampleImageHeight * rowIndex: self.sampleImageHeight * (rowIndex + 1),
                self.sampleImageWidth * colIndex: self.sampleImageWidth * (colIndex + 1)] = self.sampleImage

        return outputImg

    def _getRandomTile(self):
        # Determine position of complete random tile and copy it

        maxTilesHorizontalCount = self.outputImageWidth / self.sampleImageWidth
        maxTilesVerticalCount = self.outputImageHeight / self.sampleImageHeight

        randomTileHorizontalIndex = randint(0, maxTilesHorizontalCount - 1)
        randomTileVerticalIndex = randint(0, maxTilesVerticalCount - 1)

        randomTileLeft = self.sampleImageHeight * randomTileHorizontalIndex
        randomTileRight = self.sampleImageHeight * (randomTileHorizontalIndex + 1)
        randomTileTop = self.sampleImageHeight * randomTileVerticalIndex
        randomTileBottom = self.sampleImageHeight * (randomTileVerticalIndex + 1)
        randomTile = self.outputImage[randomTileTop:randomTileBottom, randomTileLeft:randomTileRight]

        return randomTile

    def _getRandomTilePatch(self, tile):
        # Get a random rectangular shape within the tile
        # basing on specified parameters

        tileHeight, tileWidth, tileChannels = np.shape(tile)

        randomTileWidth = randint(self.minTilePatchWidth, self.maxTilePatchWidth)
        if self.keepTilePatchToSampleImageAspectRatio:
            randomTileHeight = randomTileWidth
        else:
            randomTileHeight = randint(self.minTilePatchHeight, self.maxTilePatchHeight)

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

        randomOutputImageX = randint(0, self.outputImageWidth - tilePatchWidth)
        randomOutputImageY = randint(0, self.outputImageHeight - tilePatchHeight)

        print("Tile inserted at: (%d, %d):" % (randomOutputImageX, randomOutputImageY))

        self.outputImage[randomOutputImageY:randomOutputImageY + tilePatchHeight,
        randomOutputImageX:randomOutputImageX + tilePatchWidth] = tilePatch

    def _showImage(self, image):
        # Helper function to show the image
        plt.imshow(image)
        plt.show()

        return 0

chaosMosaic = ChaosMosaic('img/1.jpg', 'out/', [512, 512])
chaosMosaic.perform(900)
