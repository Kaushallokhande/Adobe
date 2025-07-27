import os
import json
import time
from extractor.parser import extract_outline

in_dir = 'input'

out_dir = 'output'

os.makedirs(out_dir, exist_ok=True)

for f in os.listdir(in_dir):
    
    if f.endswith('.pdf'):
        
        in_path = os.path.join(in_dir, f)
        
        out_path = os.path.join(out_dir, f.replace('.pdf', '.json'))

        t1 = time.time()

        data = extract_outline(in_path)

        with open(out_path, 'w', encoding='utf-8') as out:
            json.dump(data, out, indent=2, ensure_ascii=False)

        t2 = time.time()
        
        dur = t2 - t1

        
        print(f"→ Saved to {out_path}")
        print(f"⏱ Time taken: {dur:.2f} seconds")
