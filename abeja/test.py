'''
Created on Jul 27, 2014

@author: vit
'''
import datetime
from random import getrandbits
import hashlib


def main():
    t = datetime.datetime.utcnow()
    rand = str(getrandbits(64))
    s = str(t) + str(rand)
    _id = hashlib.md5(s.encode("utf-8")).hexdigest()
    print(s)
    print(_id)
    print(type(_id))

if __name__ == '__main__':
    main()
