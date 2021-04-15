def getBlocks(number: int, blockLength: int):
  #print("{:08b}".format(number))
  blocks = list()

  blockCount = number.bit_length()//blockLength+1
  if (number.bit_length() % blockLength == 0):
    blockCount -= 1

  for i in range(blockCount):
    block = 0
    for j in range(blockLength):
      block += (number % 2) * 2**j
      number >>= 1

    blocks.append(block)

  #print(blocks)
  blocks.reverse()
  return blocks

def fromBlocks(blocks, blockLength):
  number = 0
  blocks.reverse()

  base = 2**blockLength
  for i in range(len(blocks)):
    number += blocks[i] * base**i
  
  return number
