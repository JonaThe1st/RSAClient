from random import randrange
from primes import getRandomPrimeByBitLength
from key import RSAKey, standardBlockLength

class RSAPrivate(RSAKey):
    
    def decryptBlocks(self, blocks, blockLength=standardBlockLength, encoding="utf-8"):
        return self.getStringFromBlocks(self.applyToBlocks(blocks, blockLength), encoding=encoding)

    def toString(self):
        return "PrivateKey\n" + super().toString()
        
class RSAPublic(RSAKey):
    
    def encryptString(self, s, blockLength=standardBlockLength, encoding="utf-8"):
        return self.applyToBits(s.encode(encoding), blockLength)

    def toString(self):
        return "PublicKey\n"+ super().toString()
        

        
def randomE(phiN):
    e = randrange(3, phiN)
    while ggT(e, phiN) != 1:
        e = randrange(3, min(phiN, pow(2, 64)))
    return e
    
def getD(e, phiN):
    euklid = extended(e, phiN)
    if euklid[1] < 0:
        return euklid[1] + phiN
    return euklid[1]
    
def ggT(a, b):
    while b != 0:
        h = a % b
        a = b
        b = h
    return a

def extended(a, b):
	if b == 0:
		return (a, 1, 0)
	ds, ss, ts = extended(b, a % b)
	d, s, t = (ds, ts, ss - (a // b)*ts)
	return (d, s, t)
    
def powModN(base, exp, mod):
    res = base
    for i in range(exp-1):
        res *= base
        res %= mod
    return res
    
def getRandomKeyPair(length):
    p = getRandomPrimeByBitLength(length/2)
    q = getRandomPrimeByBitLength(length/2, isnot=p)

    N = p*q
    phiN = (p-1)*(q-1)
    
    e = randomE(phiN)
    d = getD(e, phiN)

    #print(N, e, d)

    return (RSAPrivate(N, d), RSAPublic(N, e))