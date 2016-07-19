import numpy as np

def read_image(filename):
    import PIL.Image
    return pil2array(PIL.Image.open(filename))

def read_gray_image(filename):
    import PIL.Image
    return pil2array(PIL.Image.open(filename).convert('L'))

def pil2array(pil):
    w, h = pil.size
    shape = (h, w)
    image_dtype = np.uint8
    if pil.mode == '1':
        image_dtype = np.bool
    elif pil.mode == 'L':
        image_dtype = np.uint8
    elif pil.mode == 'I;16B':
        image_dtype = np.uint16
    elif pil.mode  in ('F', 'I'):
        image_dtype = np.uint32
    elif pil.mode == 'P':
        pil = pil.convert('RGB')
        shape = (h,w,3)
    elif pil.mode in ('RGB', 'YCbCr'):
        shape = (h,w,3)
        image_dtype = np.uint8
    elif pil.mode in ('RGBA', 'CMYK'):
        shape = (h,w,4)
        image_dtype = np.uint8
    else:
        raise TypeError("Invalid or unimplemented PIL image mode '%s'" % pil.mode)

    return np.array(pil.getdata(), image_dtype).reshape(shape)

def display_image(ima, width=None, height=None):
    from io import BytesIO
    import PIL.Image
    from IPython.display import display, Image

    im = PIL.Image.fromarray(np.uint8(ima))
    bio = BytesIO()
    im.save(bio, format='png')

    if width is None and height is None:
        display(Image(bio.getvalue(),  format='png'))
    elif width is None:
        display(Image(bio.getvalue(), height=height,  format='png'))
    elif height is None:
        display(Image(bio.getvalue(), width=width,  format='png'))
    else:
        display(Image(bio.getvalue(), width=width, height=height,  format='png'))
