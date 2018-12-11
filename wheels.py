from os import listdir
from os.path import isfile, join
import numpy as np
from PIL import Image
import sys

def flush(*args):
    # this function clears current line of the console and write something,
    # which helps tracking the progress
    CLEAR = " " * 100 + "\r"
    sys.stdout.write(CLEAR)
    for a in args:
        sys.stdout.write(str(a))  # write() only accepts string
    sys.stdout.flush()


def justfilenames(dir):  # search all files in the dir
    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    return onlyfiles


supported = True


try:    # to run safe on Pythonista 3, iOS
    from termcolor import colored
except ImportError:
    print("Warning: without termcolor module, there is no support for colored console output.")
    supported = False


def err(text):  # to print something red
    if supported:
        cont = colored(text, "red")
        print(cont)
    else:
        print(text)



def blue(text):  # to print something blue
    if supported:
        cont = colored(text, "blue")
        print(cont)
    else:
        print(text)


def green(text):  # to print something green
    if supported:
        cont = colored(text, "green")
        print(cont)
    else:
        print(text)


def disablesslvarification():
    ssl._create_default_https_context = ssl._create_unverified_context


def rgb_to_grey_rgbdata(img, size=(64, 64)):
    # PLEASE RESHAPE THE RETURN VALUE TO 1, X, X, 3
    img = img.resize(size, Image.ANTIALIAS)
    grey_scale = img.convert('L')
    one_channel = np.asarray(grey_scale).reshape(64, 64, 1)
    imgdat = np.concatenate((one_channel, one_channel, one_channel), axis=2)
    return imgdat


def main():

    import h5py, numpy as np
    # default: 'a', which means read or write if exists; create otherwise
    f = h5py.File('datasets/train_catvnoncat.h5')
    trainsetx = f['train_set_x']
    print(trainsetx)
    a = np.array(trainsetx)
    print()
    f.close()




if __name__=="__main__":
    main()
