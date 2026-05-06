import numpy as np
from renk_format import to_grayscale

def double_threshold(img, low_thresh=50, high_thresh=150):
    gray = to_grayscale(img)[:,:,0]
    out = np.zeros_like(gray)
    strong = 255
    weak = 75
    
    out[gray >= high_thresh] = strong
    out[(gray <= high_thresh) & (gray >= low_thresh)] = weak
    
    return np.stack([out, out, out], axis=2).astype(np.uint8)

def canny_edge_detection(img):
    gray = to_grayscale(img)[:,:,0].astype(np.float32)
    
    padded = np.pad(gray, 1, mode='edge')
    
    # Vectorized Sobel convolution
    Ix = (padded[0:-2, 2:] - padded[0:-2, 0:-2]) + \
         2*(padded[1:-1, 2:] - padded[1:-1, 0:-2]) + \
         (padded[2:, 2:] - padded[2:, 0:-2])
         
    Iy = (padded[0:-2, 0:-2] + 2*padded[0:-2, 1:-1] + padded[0:-2, 2:]) - \
         (padded[2:, 0:-2] + 2*padded[2:, 1:-1] + padded[2:, 2:])
            
    G = np.hypot(Ix, Iy)
    G_max = G.max()
    if G_max > 0:
        G = G / G_max * 255
    
    theta = np.arctan2(Iy, Ix)
    angle = theta * 180. / np.pi
    angle[angle < 0] += 180
    
    # Vectorized Non-maximum suppression
    Z = np.zeros_like(G)
    h, w = G.shape
    
    q = np.zeros_like(G)
    r = np.zeros_like(G)
    
    # Angle 0
    m0 = ((angle >= 0) & (angle < 22.5)) | ((angle >= 157.5) & (angle <= 180))
    q[m0] = np.pad(G, ((0,0),(0,1)), mode='constant')[0:h, 1:w+1][m0]
    r[m0] = np.pad(G, ((0,0),(1,0)), mode='constant')[0:h, 0:w][m0]
    
    # Angle 45
    m45 = (angle >= 22.5) & (angle < 67.5)
    q[m45] = np.pad(G, ((0,1),(1,0)), mode='constant')[1:h+1, 0:w][m45]
    r[m45] = np.pad(G, ((1,0),(0,1)), mode='constant')[0:h, 1:w+1][m45]
    
    # Angle 90
    m90 = (angle >= 67.5) & (angle < 112.5)
    q[m90] = np.pad(G, ((0,1),(0,0)), mode='constant')[1:h+1, 0:w][m90]
    r[m90] = np.pad(G, ((1,0),(0,0)), mode='constant')[0:h, 0:w][m90]
    
    # Angle 135
    m135 = (angle >= 112.5) & (angle < 157.5)
    q[m135] = np.pad(G, ((1,0),(1,0)), mode='constant')[0:h, 0:w][m135]
    r[m135] = np.pad(G, ((0,1),(0,1)), mode='constant')[1:h+1, 1:w+1][m135]
    
    # Maksimum değerlerin olduğu yerleri işaretle
    max_mask = (G >= q) & (G >= r)
    Z[max_mask] = G[max_mask]
                
    # Çift Eşikleme (Double Threshold)
    highThreshold = Z.max() * 0.15
    lowThreshold = highThreshold * 0.05
    
    res = np.zeros_like(Z)
    res[Z >= highThreshold] = 255
    res[(Z <= highThreshold) & (Z >= lowThreshold)] = 75
    
    res = res.astype(np.uint8)
    return np.stack([res, res, res], axis=2)
