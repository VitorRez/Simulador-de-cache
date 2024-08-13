from cache import *

def readFile(c):
    arq = open("trace2.txt", "r")
    vetArq = arq.readlines()

    x = 10
    for i in vetArq:
        c.ReadWrite(i)
        x -= 1
        if x <= 0:
            break #tirar depois esse break test