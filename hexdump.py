#!/usr/bin/python3.5
#My much less code golf hexDump(). It is to be used in replacement of the hexdump() from the proxy.py script in the
#second chapter of Black Hat Python. It's 14 lines more than the book example, but it was a good exercise and it's more
#readable to me.

#codeDirtyToMe

import binascii

def hexDump(testByteString):
    testByteList = list(testByteString.decode())
    testHexString = binascii.hexlify(testByteString).decode()
    testHexList = list(testHexString)

    doubleHexList = []
    x = int(0)
    while x is not len(testHexList):  # Combine the list into pairs of integers.
        doubleHexList.insert(x, str(str(testHexList[x]) + str(testHexList[x + 1])))
        x = x + 2

    linesOfHex = float(len(doubleHexList) / int(16))
    y = int(0)
    z = int(0)
    hexPad = " "
    bitOffSet = int(0)
    while y < linesOfHex:
        bitOffSet = bitOffSet + len(doubleHexList[z:z + 16])
        hexBitOffSet = hex(bitOffSet)
        doubleHexString = " ".join(doubleHexList[z:z + 16])
        if len(doubleHexString) < 47 : hexPad = hexPad * (48 - len(doubleHexString))
        print(str(hexBitOffSet) + " | " + str(doubleHexString) + str(hexPad) + " | " + str("".join(testByteList[z:z + 16])))
        y += 1
        z += 16

    exit(0)

hexDump(b"This is a test sentence. How are you doing today?")