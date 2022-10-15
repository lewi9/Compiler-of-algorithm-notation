from os import listdir
from os.path import isfile, join

def directories(mypath):
    #onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:] == '.txt']
    onlyfiles = [mypath + "/" + f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:] == '.txt']
    return onlyfiles

