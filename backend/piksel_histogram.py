import numpy as np

def histogram_stretch(img):
    """
    Histogram germe: piksel değerlerini 0-255 aralığına yayar.
    Kontrastı düşük görüntülerde detayları ortaya çıkarır.
    Formül: yeni = (piksel - min) / (max - min) * 255
    """
    out = np.zeros_like(img)
    # Her renk kanalını bağımsız olarak geriyoruz
    for c in range(3):
        channel = img[:,:,c]
        cmin = np.min(channel)
        cmax = np.max(channel)
        
        if cmax > cmin:
            stretched = ((channel - cmin) / (cmax - cmin) * 255).astype(np.uint8)
            out[:,:,c] = stretched
        else:
            # Tüm pikseller aynı değerdeyse germe yapılamaz
            out[:,:,c] = channel
            
    return out

def reduce_contrast(img, factor=0.5):
    """
    Kontrastı azaltır. Pikselleri 128 (orta gri) değerine doğru çeker.
    factor=1.0: değişiklik yok, factor=0.0: tamamen gri
    Formül: yeni = 128 + factor * (piksel - 128)
    """
    img_f = img.astype(np.float32)
    mean_val = 128.0  # 0-255 aralığının ortası
    reduced = mean_val + factor * (img_f - mean_val)
    reduced = np.clip(reduced, 0, 255).astype(np.uint8)
    return reduced
