import numpy as np

def add_salt_and_pepper(img, prob=0.05):
    """Görüntüye rastgele tuz-biber gürültüsü ekler."""
    h, w, c = img.shape
    out = np.copy(img)
    # [0,1] aralığında rastgele matris üret
    rand = np.random.rand(h, w)
    # prob/2 altındaki pikseller beyaz (tuz)
    out[rand < (prob / 2)] = 255
    # 1-prob/2 üstündeki pikseller siyah (biber)
    out[rand > (1 - prob / 2)] = 0
    return out

def mean_filter(img, kernel_size=3):
    """Ortalama filtresi: komşu piksellerin aritmetik ortalamasını alır."""
    # Kernel boyutu tek sayı olmalı, çift gelirse bir artırıyoruz
    if kernel_size % 2 == 0:
        kernel_size += 1
    h, w, c = img.shape
    pad = kernel_size // 2
    # Kenar pikselleri için padding ekle (komşu değerlerle doldur)
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge').astype(np.float32)
    out = np.zeros_like(img, dtype=np.float32)
    
    # Sliding window: pencereyi her pozisyona kaydırarak topla
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            out += padded[dy:dy+h, dx:dx+w]
            
    # Toplam / eleman sayısı = ortalama
    out /= (kernel_size * kernel_size)
    return out.astype(np.uint8)

def median_filter(img, kernel_size=3):
    """Medyan filtresi: komşuların ortanca değerini alır. Salt&pepper'a karşı etkili."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    
    # Her komşu pozisyonu bir katman olarak topla
    layers = []
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            layers.append(padded[dy:dy+h, dx:dx+w])
    
    # Katmanları üst üste koyup medyanı hesapla
    stacked = np.stack(layers, axis=-1)
    out = np.median(stacked, axis=-1)
    return out.astype(np.uint8)

def motion_filter(img, kernel_size=9):
    """Hareket bulanıklığı efekti uygular (çapraz kernel ile)."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    h, w, c = img.shape
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='edge').astype(np.float32)
    out = np.zeros_like(img, dtype=np.float32)
    
    # Çapraz kernel: sadece köşegen elemanları 1/N, diğerleri 0
    # Bu 45 derecelik bir hareket bulanıklığı oluşturur
    kernel = np.eye(kernel_size) / kernel_size
    
    for dy in range(kernel_size):
        for dx in range(kernel_size):
            if kernel[dy, dx] > 0:
                out += padded[dy:dy+h, dx:dx+w] * kernel[dy, dx]
                
    return out.astype(np.uint8)
