import collections
import re

def get_dominant_style(sps):
    
    if not sps:
        return None, None
    c = collections.Counter((s['size'], s['font']) for s in sps)
    (sz, fn), _ = c.most_common(1)[0]
    return sz, fn

def same_style(a, b):
    return a['font'] == b['font'] and abs(a['size'] - b['size']) < 0.1

def spans_touch(a, b):
    return abs(a['bbox'][2] - b['bbox'][0]) < 10

def merge_spans(sps):
    
    out = []
    
    for s in sps:
        
        s['bold'] = (s.get('flags', 0) & 2) != 0
        
        if out and same_style(out[-1], s) and spans_touch(out[-1], s):
            out[-1]['text'] += s['text']
            
            out[-1]['bbox'] = [
                min(out[-1]['bbox'][0], s['bbox'][0]),
                min(out[-1]['bbox'][1], s['bbox'][1]),
                max(out[-1]['bbox'][2], s['bbox'][2]),
                max(out[-1]['bbox'][3], s['bbox'][3]),
            ]
            
            out[-1]['bold'] = out[-1]['bold'] or s['bold']
        else:
            out.append(s.copy())
    return out

def get_body_style(xs):
   
    c = collections.Counter(
        (x['font_size'], x['font_name']) for x in xs if x['font_size']
    )
    
    (sz, fn), _ = c.most_common(1)[0]
    
    return {'font_size': sz, 'font_name': fn}
