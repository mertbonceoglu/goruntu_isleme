import numpy as np
from renk_format import to_grayscale

def double_threshold(img, low_thresh=50, high_thresh=150):
    """Çift eşikleme: pikselleri alt ve üst eşik değerine göre 3 sınıfa ayırır."""
    gray = to_grayscale(img)[:,:,0]
    out = np.zeros_like(gray)
    strong = 255   # güçlü kenar
    weak = 75      # zayıf kenar
    
    # üst eşiğin üstündeki pikseller kesinlikle kenar
    out[gray >= high_thresh] = strong
    # iki eşik arasındakiler muhtemel kenar
    out[(gray <= high_thresh) & (gray >= low_thresh)] = weak
    
    # 3 kanala kopyalayarak BGR formatında döndürüyoruz
    return np.stack([out, out, out], axis=2).astype(np.uint8)

def canny_edge_detection(img):
    """
    Canny kenar bulma algoritması.
    Adımlar: Gri dönüşüm -> Sobel gradyanları -> NMS -> Çift eşikleme
    """
    gray = to_grayscale(img)[:,:,0].astype(np.float32)
    
    # Kenar pikselleri için padding ekliyoruz (komşu değerlerle doldur)
    padded = np.pad(gray, 1, mode='edge')
    
    # --- ADIM 1: Sobel filtresi ile gradyan hesaplama ---
    # Yatay gradyan (Ix): sol-sağ farkları, [-1 0 +1; -2 0 +2; -1 0 +1] kerneline karşılık gelir
    Ix = (padded[0:-2, 2:] - padded[0:-2, 0:-2]) + \
         2*(padded[1:-1, 2:] - padded[1:-1, 0:-2]) + \
         (padded[2:, 2:] - padded[2:, 0:-2])
    
    # Dikey gradyan (Iy): üst-alt farkları, [+1 +2 +1; 0 0 0; -1 -2 -1] kerneline karşılık gelir
    Iy = (padded[0:-2, 0:-2] + 2*padded[0:-2, 1:-1] + padded[0:-2, 2:]) - \
         (padded[2:, 0:-2] + 2*padded[2:, 1:-1] + padded[2:, 2:])
            
    # Gradyan büyüklüğü: G = √(Ix² + Iy²)
    G = np.hypot(Ix, Iy)
    G_max = G.max()
    if G_max > 0:
        G = G / G_max * 255  # 0-255 aralığına normalize et
    
    # Gradyan yönü (derece cinsinden, 0-180 arası)
    theta = np.arctan2(Iy, Ix)
    angle = theta * 180. / np.pi
    angle[angle < 0] += 180  # negatif açıları pozitife çevir
    
    # --- ADIM 2: Maksimum olmayan pikselleri bastırma (NMS) ---
    # Kalın kenarları inceltmek için her pikseli gradyan yönündeki 2 komşusuyla karşılaştırıyoruz
    Z = np.zeros_like(G)
    h, w = G.shape
    
    # q ve r: gradyan yönündeki ileri ve geri komşu değerleri
    q = np.zeros_like(G)
    r = np.zeros_like(G)
    
    # Yatay kenarlar (açı ~0° veya ~180°): sağ ve sol komşuya bak
    m0 = ((angle >= 0) & (angle < 22.5)) | ((angle >= 157.5) & (angle <= 180))
    q[m0] = np.pad(G, ((0,0),(0,1)), mode='constant')[0:h, 1:w+1][m0]
    r[m0] = np.pad(G, ((0,0),(1,0)), mode='constant')[0:h, 0:w][m0]
    
    # Çapraz kenarlar (~45°): sağ-alt ve sol-üst komşuya bak
    m45 = (angle >= 22.5) & (angle < 67.5)
    q[m45] = np.pad(G, ((0,1),(1,0)), mode='constant')[1:h+1, 0:w][m45]
    r[m45] = np.pad(G, ((1,0),(0,1)), mode='constant')[0:h, 1:w+1][m45]
    
    # Dikey kenarlar (~90°): alt ve üst komşuya bak
    m90 = (angle >= 67.5) & (angle < 112.5)
    q[m90] = np.pad(G, ((0,1),(0,0)), mode='constant')[1:h+1, 0:w][m90]
    r[m90] = np.pad(G, ((1,0),(0,0)), mode='constant')[0:h, 0:w][m90]
    
    # Ters çapraz kenarlar (~135°): sol-alt ve sağ-üst komşuya bak
    m135 = (angle >= 112.5) & (angle < 157.5)
    q[m135] = np.pad(G, ((1,0),(1,0)), mode='constant')[0:h, 0:w][m135]
    r[m135] = np.pad(G, ((0,1),(0,1)), mode='constant')[1:h+1, 1:w+1][m135]
    
    # Piksel her iki komşusundan da büyükse kenar olarak kal, değilse bastır
    max_mask = (G >= q) & (G >= r)
    Z[max_mask] = G[max_mask]
                
    # --- ADIM 3: Çift eşikleme ---
    # Üst eşik: gradyan büyüklüğünün %15'i, alt eşik: üst eşiğin %5'i
    highThreshold = Z.max() * 0.15
    lowThreshold = highThreshold * 0.05
    
    res = np.zeros_like(Z)
    res[Z >= highThreshold] = 255    # güçlü kenar (beyaz)
    res[(Z <= highThreshold) & (Z >= lowThreshold)] = 75   # zayıf kenar (gri)
    # alt eşiğin altındakiler zaten 0 kalıyor (kenar değil)
    
    res = res.astype(np.uint8)
    return np.stack([res, res, res], axis=2)
