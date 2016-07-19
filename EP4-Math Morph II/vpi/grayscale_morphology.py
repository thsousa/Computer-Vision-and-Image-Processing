import scipy.ndimage as mm
from . import binary_morphology as bm

def dilation(f, b=bm.create_structure_element_cross(), iterations=1):
    return mm.grey_dilation(f,structure=b)

def erosion(f, b=bm.create_structure_element_cross(), iterations=1):
    return mm.grey_erosion(f,structure=b)

def closing(f, b=bm.create_structure_element_cross()):
    return mm.grey_closing(f, structure=b)

def opening(f, b=bm.create_structure_element_cross()):
    return mm.grey_opening(f, structure=b)

def morphological_external_boundary(f, b=bm.create_structure_element_cross()):
    return f - erosion(f, b)

def morphological_internal_boundary(f, b=bm.create_structure_element_cross()):
    return dilation(f, b) - f

def morphological_gradient(f, b=bm.create_structure_element_cross()):
    return dilation(f, b) - erosion(f, b)

def opening_top_hat(f, b=bm.create_structure_element_cross()):
    return f - opening(f, b)

def closing_top_hat(f, b=bm.create_structure_element_cross()):
    return closing(f, b) - f

def inf_reconstruction(markers, f, bc=bm.create_structure_element_cross()):
    return bm.inf_reconstruction(markers, f, bc)
