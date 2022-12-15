from ocr_fr_detect import ocr_fr_detect_v1
import os

file_cache = set()

def pdf_path_extract(path: str):
    # Extract all pdf paths
    pdf_files = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files[file] = os.path.join(root, file)
    return pdf_files

dict_paths = pdf_path_extract("KPMG_data/")

# print(dictio)

for key, val in dict_paths.items():
    pdf_file = os.path.basename(os.path.splitext(val)[0])
    if pdf_file not in file_cache:
        ocr_fr_detect_v1(val)
        file_cache.add(pdf_file)