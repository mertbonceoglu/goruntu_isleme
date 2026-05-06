import numpy as np

def add_salt_and_pepper(img, prob=0.05):
    h, w, c = img.shape
    out = np.copy(img)
    rand = np.random.rand(h, w)
    out[rand < (prob / 2)] = 255
    out[rand > (1 - prob / 2)] = 0
    return out

def mean_filter(img, kernel_size=3):
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge').astype(np.float32)
    out = np.zeros_like(img, dtype=np.float32)
    
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            out += padded[dy:dy+h, dx:dx+w]
            
    out /= (kernel_size * kernel_size)
    return out.astype(np.uint8)

def median_filter(img, kernel_size=3):
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    
    layers = []
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            layers.append(padded[dy:dy+h, dx:dx+w])
            
    stacked = np.stack(layers, axis=-1)
    out = np.median(stacked, axis=-1)
    return out.astype(np.uint8)

def motion_filter(img, kernel_size=9):
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge').astype(np.float32)
    out = np.zeros_like(img, dtype=np.float32)
    
    kernel = np.eye(kernel_size) / kernel_size
    
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            if kernel[dy, dx] > 0:
                out += padded[dy:dy+h, dx:dx+w] * kernel[dy, dx]
                
    return out.astype(np.uint8)
