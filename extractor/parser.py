import fitz
from extractor.utils import cluster_fonts
from langdetect import detect


def find_title(blocks):
    
    blocks = sorted(blocks, key=lambda b: (-b["size"], b["y"]))
    for b in blocks:
        
        if len(b["text"]) > 4 and b["y"] < 200:
            return b["text"]
    return "Untitled"


def assign_heading_levels(blocks, sizes, lang="en"):
    
    clusters = cluster_fonts(sizes)
    
    out = []

    for b in blocks:
        
        lvl = clusters.get(b["size"])
       
        if lvl not in [1, 2, 3]:
            continue

        if lang == "en":
            if lvl == 3 and len(b["text"].strip()) < 4:
                continue
            if lvl in [1, 2] and len(b["text"].split()) > 15:
                continue
        else:
            if b["y"] > 600:
                continue
            
            if len(b["text"]) < 3:
                continue
           
            if b["width"] < 50:
                continue
           
            if b["size"] < 8.0:
                continue

        out.append({
            "level": f"H{lvl}",
            "text": b["text"],
            "page": b["page"]
        })

    return out


def extract_outline(path):
    doc = fitz.open(path)
   
    blocks = []
    
    sizes = []
    texts = []

    for i in range(len(doc)):
        pg = doc[i]
        blks = pg.get_text("dict")["blocks"]

        for blk in blks:
            
            for ln in blk.get("lines", []):
                
                for sp in ln.get("spans", []):
                    txt = sp["text"].strip()
                    if not txt:
                        continue

                    s = round(sp["size"], 1)
                    f = sp.get("font", "").lower()
                    bb = sp["bbox"]

                    bold = (
                        "bold" in f or
                        "black" in f or
                        "semibold" in f
                    )

                    blocks.append({
                        "text": txt,
                        "size": s,
                        "font": f,
                        "bold": bold,
                        "page": i + 1,
                        "y": bb[1],
                        "x": bb[0],
                        "width": bb[2] - bb[0]
                    })

                    sizes.append(s)
                    texts.append(txt)

    try:
        lang = detect(" ".join(texts[:100]))
    except:
        lang = "en"

    print(f"Detected Language: {lang}")

    
    title = find_title(blocks)
   
    outline = assign_heading_levels(blocks, sizes, lang=lang)

    return {
        "title": title,
        "outline": outline
    }
