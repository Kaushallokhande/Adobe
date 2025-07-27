# 📄 PDF Grabber (aka Outline Thingy)

Quick and dirty tool to pull out the title + headings (H1, H2, H3) from any PDF — offline, fast, and works with weird fonts.

---

##  What It Does

-  Finds **title + headings** using font size & clustering
-  Works with **English, Hindi, Japanese**, etc.
-  Super fast (under 10s per PDF)
-  Runs **offline** on **CPU only**
-  Saves output as nice clean **JSON**

---

## 📁 Folders & Files

```

pdf-outline-extractor/
├── input/         # drop your PDFs here
├── output/        # you’ll find JSONs here
├── extractor/
│   ├── **init**.py
│   ├── parser.py     # all the PDF parsing + logic
│   └── utils.py      # clustering helpers
├── main.py        # script to run the thing
├── requirements.txt
└── README.md      # you're here :)

````

---
##  How It Works

- **Font size clustering**: uses Agglomerative (or DBSCAN if needed) to group text sizes into H1/H2/H3
- **Language check**: uses `langdetect` to tweak heading rules (e.g. skips bold check in Japanese)
- **Title grab**: picks the biggest top-line as the doc title

---

##  How To Run

### 1. Clone it

```bash
git clone https://github.com/Kaushallokhande/pdf-outline-extractor.git
cd pdf-outline-extractor
````

### 2. Set up venv

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install stuff

```bash
pip install -r requirements.txt
```

### 4. Add PDFs

Drop `.pdf` files into the `input/` folder.

### 5. Run it

```bash
python main.py
```

Check the `output/` folder for JSON files.

---

##  Sample Input & Output

### Input (PDF content):

```
Title: ML Handbook

H1: Intro to ML
H2: Types of Learning
H3: Supervised Learning
```

### Output (JSON):

```json
{
  "title": "ML Handbook",
  "outline": [
    { "level": "H1", "text": "Intro to ML", "page": 1 },
    { "level": "H2", "text": "Types of Learning", "page": 1 },
    { "level": "H3", "text": "Supervised Learning", "page": 2 }
  ]
}
```

---

##  Limits & Stuff

| Thing       | Limit              |
| ----------- | ------------------ |
|  Pages    | Up to 50 per file  |
|  Time     | Under 10 sec / PDF |
|  Hardware | CPU-only           |
|  Internet | Not needed         |
|  Size     | <200MB total       |

---

## Languages It Gets

* English
* Hindi
* Japanese
  ...and more (auto-detects with `langdetect`)

---

##  Accuracy Things

* Avoids footers/headers using Y-pos
* Can handle mixed fonts/styles
* Bonus: heading visualizer (WIP)

---

##  Docker?

Yup, Dockerfile included. Run it anywhere. Setup docs coming soon.

---

##  Stuff Used

* `PyMuPDF` → for PDF parsing
* `scikit-learn` → for font clustering
* `langdetect` → for figuring out the language

---

## Built By

**Kaushal Lokhande**
[GitHub](https://github.com/Kaushallokhande) • [LinkedIn](https://linkedin.com/in/kaushal-lokhande-709432256)

---
