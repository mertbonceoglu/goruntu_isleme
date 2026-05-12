import numpy as np

def dilate(img, kernel_size=3):
    """Genişleme: komşuların maksimumunu alır, parlak alanlar büyür."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    
    # Tüm komşu pozisyonları katman olarak topla
    layers = []
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            layers.append(padded[dy:dy+h, dx:dx+w])
    
    # Maksimum: en parlak komşu değeri seçilir
    stacked = np.stack(layers, axis=-1)
    out = np.max(stacked, axis=-1)
    return out.astype(np.uint8)

def erode(img, kernel_size=3):
    """Aşınma: komşuların minimumunu alır, parlak alanlar küçülür."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    
    layers = []
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            layers.append(padded[dy:dy+h, dx:dx+w])
    
    # Minimum: en karanlık komşu değeri seçilir
    stacked = np.stack(layers, axis=-1)
    out = np.min(stacked, axis=-1)
    return out.astype(np.uint8)

def open_morph(img, kernel_size=3):
    """Açma işlemi: önce aşındır, sonra genişlet. Küçük gürültüleri temizler."""
    eroded = erode(img, kernel_size)
    return dilate(eroded, kernel_size)

def close_morph(img, kernel_size=3):
    """Kapama işlemi: önce genişlet, sonra aşındır. Küçük boşlukları doldurur."""
    dilated = dilate(img, kernel_size)
    return erode(dilated, kernel_size)
