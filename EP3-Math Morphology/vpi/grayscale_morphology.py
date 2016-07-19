import scipy.ndimage as mm
from . import binary_morphology as bm

def dilation(f, b):
    return mm.grey_dilation(f,structure=b)

def erosion(f, b):
    return mm.grey_erosion(f,structure=b)

def closing(f, b):
    return mm.grey_closing(f, structure=b)

def opening(f, b):
    return mm.grey_opening(f, struture=b)



