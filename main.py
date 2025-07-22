import time
from extractor.parser import process_pdf
import os

input_dir = "input"
output_dir = "output"

def main():
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))

            print(f"\n⏳ Processing {filename}...")
            start_time = time.time()

            process_pdf(input_path, output_path)

            elapsed = time.time() - start_time
            print(f"✅ Done in {elapsed:.2f} seconds\n")

if __name__ == "__main__":
    main()
