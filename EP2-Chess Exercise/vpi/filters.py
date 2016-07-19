import numpy as np

#code from adesso library (function iaconv)
#http://adessowiki.fee.unicamp.br/adesso-1/wiki/ia636/iaconv/view/
def convolve(image, kernel):
    image, kernel = np.asarray(image), np.asarray(kernel, float)
    if len(image.shape) == 1: image = image[np.newaxis,:]
    if len(image.shape) == 1: kernel = kernel[np.newaxis,:]

    if image.size < kernel.size:
        image, kernel = kernel, image

    g = np.zeros(np.array(image.shape) + np.array(kernel.shape) - 1)
    if kernel.ndim == 2:
        H, W = image.shape
        for (r, c) in np.transpose(np.nonzero(kernel)):
            g[r:r+H, c:c+W] += image * kernel[r,c]

    if kernel.ndim == 3:
        D, H, W = image.shape
        for (D, H, W) in np.transpose(np.nonzero(kernel)):
            g[d:d+D, r:r+H, c:c+W] += image * kernel[d,r,c]

    additional_size = kernel.shape[0]//2, kernel.shape[1]//2
    image_size = g.shape
    return g[additional_size[0]:image_size[0]-additional_size[0],
             additional_size[1]:image_size[1]-additional_size[1]]


def normalize(f, lmin=0.0, lmax=255.0):
    fmin, fmax  = f.min(), f.max()
    return ((lmax - lmin)/(fmax-fmin)) * (f - fmin) + lmin
