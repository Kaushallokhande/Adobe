import os
import json
import time
from extractor.parser import extract_text_and_styles as get_txt, is_heading as is_h, assign_hierarchy as label_h, extract_title as get_title
from extractor.utils import get_body_style as body

def main():
    
    in_dir = os.environ.get("INPUT_DIR", "./app/input")
   
    out_dir = os.environ.get("OUTPUT_DIR", "./app/output")

    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    found = False

    for f in os.listdir(in_dir):
        
        if f.lower().endswith(".pdf"):
            found = True
            t0 = time.perf_counter()

            p = os.path.join(in_dir, f)
            
            stuff = get_txt(p)
            if not stuff:
                continue

            b = body(stuff)
            
            if not b:
                continue

            heads = [x for x in stuff if is_h(x, b)]
            labs = label_h(heads)

            out = [{"level": x["level"], "text": x["text"], "page": x["page_num"]} for x in labs]
            
            t = get_title(p, heads if heads else stuff)

            res = {"title": t, "outline": out}

            out_f = os.path.splitext(f)[0] + ".json"
            
            out_p = os.path.join(out_dir, out_f)
           
            with open(out_p, 'w', encoding='utf-8') as fh:
                json.dump(res, fh, ensure_ascii=False, indent=2)

            dt = time.perf_counter() - t0
            print(f"✅ Done {f} -> {out_f}")
            print(f"⏱ Time {dt:.2f}s")

    if not found:
        print(f"⚠️ No PDFs in '{in_dir}', add some and run again.")

if __name__ == "__main__":
    main()
