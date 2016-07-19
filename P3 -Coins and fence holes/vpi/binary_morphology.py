import scipy.ndimage as mm
import numpy as np

############# Utils  #############################
def sub_with_saturation(f1, f2):
    return np.clip(f1 - f2, 0,1)

def binary_image_union(f1, f2):
    return np.maximum(f1, f2)

#function adpated from http://adessowiki.fee.unicamp.br/adesso-1/wiki/ia870/iaisequal/view/
def is_binary_image_equal(f1, f2):
    if f1.shape != f2.shape:
        return False
    return np.all(f1 == f2)

def calculate_connected_components_area(f, conectivity=None):
    result = np.zeros(f.shape)
    labeled_array, num_ccs  = mm.label(f, structure=conectivity)
    area = np.bincount(labeled_array.ravel())
    
    for i in range(1, num_ccs+1):
        result[labeled_array == i] = area[i]
    return result

#function based on iaNLut from adesso
def neighbourhood_lut(s, offset):
    H,W = s
    n = H*W
    hi = np.arange(H).reshape(-1,1)
    wi = np.arange(W).reshape(1,-1)
    hoff = offset[:,0]
    woff = offset[:,1]
    h = hi + hoff.reshape(-1,1,1)
    w = wi + woff.reshape(-1,1,1)
    h[(h < 0) | (h >= H)] = n
    w[(w < 0) | (w >= W)] = n
    nlut = np.clip(h * W + w, 0, n)
    return nlut.reshape(offset.shape[0], -1).transpose()

############# Structure elements creation  #############################
def create_structure_element_disk(r=3):
    v = np.arange(-r, r+1)
    x = np.resize(v, (len(v), len(v)))
    y = np.transpose(x)
    be = np.sqrt(x*x + y*y)<=(r+0.5)
    return be >= 1
    
def create_structure_element_cross(r=1):
    cross = np.array([[0,1,0],[1,1,1],[0,1,0]])
    if r > 1:
        shape = (3*r-(r-1), 3*r-(r-1))
        se  = np.zeros(shape)
        center = (shape[0] // 2, shape[1] // 2)
        indices = np.arange(-1, 2)

        for i in np.arange(3):
            for j in np.arange(3):
                se[indices[i]+center[0], indices[j]+center[1]] = cross[i,j]

        return dilation(se, cross, r-1)
    
    return cross

def create_structure_element_box(r=1):
    if r == 1:
        return np.ones((3,3), np.bool)
    else:
        return np.ones((3*r-(r-1), 3*r-(r-1)), np.bool)

############# Morphology operators  #############################
def dilation(f, b=create_structure_element_cross(), iterations=1):
    return mm.binary_dilation(f, b, iterations)

def erosion(f, b=create_structure_element_cross(), iterations=1):
    return mm.binary_erosion(f, b, iterations)

# function adpated from http://adessowiki.fee.unicamp.br/adesso-1/wiki/ia870/iacero/view/
#def conditional_erosion(f, g, b=create_structure_element_cross(), n=1):
#   y = binary_image_union(f, g)     #union
#    for i in range(n):
#        aux = y
#        y = binary_image_union(erosion(y,b), g) # erosion(y,b) union g
#        if is_binary_image_equal(y, aux):
#            break
#    return y

def opening(f, b=create_structure_element_cross()):
    return mm.binary_opening(f, b)

def closing(f, b=create_structure_element_cross()):
    return mm.binary_closing(f,b)

def closing_holes(f, b=create_structure_element_cross()):
    return mm.binary_fill_holes(f, b)

def opening_top_hat(f, b=create_structure_element_cross()):
    return sub_with_saturation(f, opening(f,b))

def morphological_external_boundary(f, b=create_structure_element_cross()):
    return dilation(f,b) - f

def morphological_internal_boundary(f, b=create_structure_element_cross()):
    return f - erosion(f, b)

def morphological_gradient(f, b=create_structure_element_cross()):
    return dilation(f, b) - erosion(f, b)
    #return mm.morphological_gradient(f, structure=b)

def area_opening(f, thres_area, conectivity=None):
    area = calculate_connected_components_area(f, conectivity)
    return area >= thres_area


#function extracted from iainfrec of the ia870 library
#available in http://adessowiki.fee.unicamp.br/adesso-1/wiki/ia870/iainfrec/view/
def inf_reconstruction(markers, f, bc=create_structure_element_cross()):
    h, w = bc.shape
    hc, wc = h//2, w//2
    b = bc.copy()
    off = np.transpose(b.nonzero()) - np.array([hc, wc])
    i = off[:,0] * w + off[:,1]
    Nids = neighbourhood_lut(f.shape, off)
    x, y = np.where(Nids == f.size)
    Nids[x,y] = x
    Nids_pos = Nids[:,i < 0] #Following Vincent93 convention
    Nids_neg = Nids[:,i > 0] #Following Vincent93 convention

    I = f.flatten()
    J = markers.flatten()
    D = np.nonzero(J)[0]
    V = np.zeros(f.size, np.bool) #queue insertion control
    queue = []

    for p in D:
        Jq = J[p]
        for q in Nids_pos[p]:
            Jq = max(Jq,J[q])
            if (J[q] < J[p]) and (J[q] < I[q]) and ~V[p]:
                queue.append(p)
                V[p] = True
            J[p] = min(Jq, I[p])

    for p in D[::-1]:
        Jq = J[p]
        for q in Nids_neg[p]:
            Jq = max(Jq, J[q])
            if (J[q] < J[p]) and (J[q] < I[q]) and ~V[p]:
                queue.append(p)
                V[p] = True
            J[p] = min(Jq, I[p])

    while queue:
        p = queue.pop(0)
        for q in Nids[p]:
            if J[q] < J[p] and I[q] != J[q]:
                J[q] = min(J[p], I[q])
                queue.append(q)
            
    return J.reshape(f.shape)


#function adpated from http://adessowiki.fee.unicamp.br/adesso-1/wiki/ia870/iasuprec/view/
#def sup_reconstruction(f, g, bc=create_structure_element_cross()):
#    n = np.product(f.shape)
#    y = conditional_erosion(f, g, bc, n)

#    return y
