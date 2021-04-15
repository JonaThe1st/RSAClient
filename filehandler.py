from keyfactory import RSAPrivate, RSAPublic
import os
import json

def saveKey(key, destination, append=False):
  if not append:
    with open(destination, "w") as f:
      f.write(key.toString())
  else:
    with open(destination, "a") as f:
      f.write("\n\n")
      f.write(key.toString())

def saveKeyPair(keyPair, destination):
  saveKey(keyPair[0], destination)
  saveKey(keyPair[1], destination, append=True)

def loadKey(KeyType, destination):
  if (KeyType == RSAPrivate):
    startString = "PrivateKey\n"
  else:
    startString = "PublicKey\n"

  with open(destination, "r") as f:

    # go to Start String
    line = f.readline()
    
    while line != startString:
      line = f.readline()
      if not line:
        print("KeyNotFound")
        return False
      

    N = int(f.readline())
    e = int(f.readline())

    if (KeyType == RSAPrivate):
      return RSAPrivate(N, e)
    else:
      return RSAPublic(N, e)

def loadKeyPair(destination):
  return (loadKey(RSAPrivate, destination), loadKey(RSAPublic, destination))

def saveString(destination, content):
  with open(destination, "w") as f:
    f.write(content)

def loadString(destination):
  with open(destination, "r") as f:
    return f.read()

def saveBlocks(destination, blocks):
  saveString(destination, json.dumps(blocks))

def loadBlocks(destination):
  return json.loads(loadString(destination))