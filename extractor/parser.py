import fitz
import re
from .utils import merge_spans as msp, get_dominant_style as dom, get_body_style as bsty

def is_language_supported(text):
    hindi = any('\u0900' <= c <= '\u097F' for c in text)
    japanese = any('\u3040' <= c <= '\u30FF' or '\u4E00' <= c <= '\u9FAF' for c in text)
    english_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
    if hindi or japanese:
        return True
    return english_ratio >= 0.6

def extract_text_and_styles(p):
    doc = fitz.open(p)
    out = []
    for i, pg in enumerate(doc, start=1):
        w = pg.rect.width
        bs = pg.get_text("dict")['blocks']
        for b in bs:
            if b['type'] == 0:
                for l in b['lines']:
                    sps = msp(l['spans'])
                    txt = ''.join(s['text'] for s in sps).strip()
                    if not txt:
                        continue
                    sz, fn = dom(sps)
                    out.append({
                        'text': txt,
                        'font_size': sz,
                        'font_name': fn,
                        'page_num': i,
                        'bbox': l['bbox'],
                        'page_width': w,
                        'spans': sps
                    })
    doc.close()
    return out

def is_heading(x, bs):
    t = x['text'].strip()
    sz = x['font_size']
    fn = x['font_name']

    if not all([t, sz, fn]):
        return False
    
    if not is_language_supported(t):
        return False
    
    if len(t) < 10:
        return False
    
    if sum(c.isalpha() for c in t) / max(1, len(t)) < 0.6:
        return False
    
    if re.search(r'(\w)\1{2,}', t):
        return False
    
    if re.match(r'^[a-zA-Z]\)$', t.strip()) or re.match(r'^\(\d+\)$', t.strip()):
        return False
    
    if re.match(r'^\([a-zA-Z]\)[\s\S]*$', t) and len(t) < 50:
        return False
    
    if re.match(r'^\d+\.[\s\S]*$', t) and len(t) < 50:
        return False
    
    if t[-1] in '.۔؟' and not re.match(r'^\d+(\.\d+)*', t):
        return False
    
    if re.match(r'^((\d+\.)+\d*|[A-Z]\.|\([a-z]\)|\(?\d+\)?\.)\s+', t):
        return True
    
    big = sz > bs['font_size'] * 1.1
    
    bold = any(s.get('bold') for s in x.get('spans', []))
    
    tight = (x['bbox'][2] - x['bbox'][0]) < x['page_width'] * 0.9
    
    no_dot = not t.endswith('.')
    
    if big and bold and tight and no_dot:
        return True
    if sz > bs['font_size'] * 1.2 and tight and no_dot:
        return True
    return False

def extract_title(p, lst):
    doc = fitz.open(p)
    
    if doc.metadata and doc.metadata.get('title'):
        mt = doc.metadata['title']
        
        if len(mt.strip()) > 10 and "Microsoft Word" not in mt:
            return mt.strip()
    
    l1 = [x for x in lst if x['page_num'] == 1 and x['font_size']]
    
    for l in sorted(l1, key=lambda x: -x['font_size']):
        b = any(s.get('bold') for s in l.get('spans', []))
        
        c = abs((l['bbox'][0] + l['bbox'][2]) / 2 - l['page_width'] / 2) < l['page_width'] * 0.25
        
        if b and c and len(l['text']) > 10:
            return l['text'].strip()
        
    for l in l1:
        
        
        if len(l['text']) > 20 and sum(c.isalpha() for c in l['text']) / len(l['text']) > 0.5:
            return l['text'].strip()
    return ""

def assign_hierarchy(hs):
    
    if not hs:
        return []
    szs = sorted({h['font_size'] for h in hs}, reverse=True)
    m = {}
    for i, sz in enumerate(szs):
        
        if i == 0:
            m[sz] = "H1"
        
        elif i == 1:
            m[sz] = "H2"
        
        elif i == 2:
            m[sz] = "H3"
            
    for h in hs:
        
        if h['font_size'] in m:
            h['level'] = m[h['font_size']]
    for h in hs:
        
        m1 = re.match(r'^(\d+(\.\d+)*)\s+', h['text'])
        
        if m1:
            d = len(m1.group(1).split('.'))
            if d == 1:
                h['level'] = "H3"
            elif d == 2:
                h['level'] = "H4"
    return sorted([h for h in hs if 'level' in h], key=lambda h: (h['page_num'], h['bbox'][1]))
