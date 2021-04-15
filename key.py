from bitOperations import getBlocks, fromBlocks

standardBlockLength = 21

class RSAKey():

    def __init__(self, N, e):
        self.N = N
        self.e = e
        
    def applyToInt(self, c):
        return pow(c, self.e, self.N)

    def applyToBits(self, c, blockLength=standardBlockLength):
      bitValue = int.from_bytes(c, "big")

      blocks = getBlocks(bitValue, blockLength=standardBlockLength)
      print(blocks)
      

      return self.applyToBlocks(blocks, blockLength=standardBlockLength)

    def applyToBlocks(self, blocks, blockLength=standardBlockLength):
      appliedBlocks = list()

      for block in blocks:
        appliedBlocks.append(self.applyToInt(block))

      return appliedBlocks

    def getStringFromBlocks(self, blocks, blockLength=standardBlockLength, encoding="utf-8"):
      value = fromBlocks(blocks, blockLength)
      return value.to_bytes(value.bit_length(), "big").decode(encoding)

    def toString(self):
      return str(self.N) + "\n" + str(self.e)

