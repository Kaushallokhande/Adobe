from sklearn.cluster import AgglomerativeClustering
import numpy as np

def cluster_fonts(sizes):
    
    u = sorted(list(set(sizes)), reverse=True)
    arr = np.array(u).reshape(-1, 1)

    
    if len(u) <= 3:
        return {round(s, 1): i + 1 for i, s in enumerate(u)}

    model = AgglomerativeClustering(n_clusters=3)
    
    lbls = model.fit_predict(arr)

    z = sorted(zip(u, lbls), reverse=True)
    
    m = {}
    
    r = 1

    for s, l in z:
        
        if l not in m:
            m[l] = r
            r += 1

    return {round(s, 1): m[l] for s, l in z}
