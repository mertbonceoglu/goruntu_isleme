import numpy as np

def dilate(img, kernel_size=3):
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    
    layers = []
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            layers.append(padded[dy:dy+h, dx:dx+w])
            
    stacked = np.stack(layers, axis=-1)
    out = np.max(stacked, axis=-1)
    return out.astype(np.uint8)

def erode(img, kernel_size=3):
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    
    layers = []
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            layers.append(padded[dy:dy+h, dx:dx+w])
            
    stacked = np.stack(layers, axis=-1)
    out = np.min(stacked, axis=-1)
    return out.astype(np.uint8)

def open_morph(img, kernel_size=3):
    eroded = erode(img, kernel_size)
    return dilate(eroded, kernel_size)

def close_morph(img, kernel_size=3):
    dilated = dilate(img, kernel_size)
    return erode(dilated, kernel_size)
