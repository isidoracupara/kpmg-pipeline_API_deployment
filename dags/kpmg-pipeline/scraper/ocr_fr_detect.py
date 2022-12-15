from langdetect import detect
import camelot
import os

def init_set():
    file_cache = set()

def ocr_fr_detect_v1(file):
    """ 
    This function takes a pdf file as an input and outputs a txt file with the same name.
    The txt file contains only the french text contained in the pdf document.
    Takes approximatly 20 seconds for 6 pages
    """
    vowels = ['a','e','i','o','u']
    fr = []
    # check the file extension
    if file.endswith(".pdf"):
        #print(file) # debug, prints filename
        tables = camelot.read_pdf(file, flavor='stream' , pages= 'all', edge_tol=0)
        # for every detected table (page and text structure)
        for i in range(len(tables)):
            # make a df
            data = tables[i].df
            # replace new line (\n) with space
            data.replace('\\n',' ',regex=True, inplace = True)
            # for every column detected
            for j in range(len(data.columns)):
                # put all the text of that column in a list # this takes also out empty rows and lone numbers (as pagenumber)
                text_list = [x for x in tables[i].df[j].values if x != '' if not x.isdigit()] 
                # convert the list to text
                text = (' '.join(text_list))
                # if there is at least one vowel (we cannot detect language for numbers)
                if any(char in vowels for char in text):
                    # detect language
                    try:
                        language = detect(text)
                        if language == 'fr':
                            fr.append(text)
                    except Exception as e:
                        print(e)
                        print(os.path.basename(os.path.splitext(file)[0]))
                else:
                    # print(i,j, ': ',text ) # used for debug
                    if len(text)>1:
                        # add rows that contains no vowels, longer than one digit to the french version
                        fr.append(text)
        # Outputs the french text in a text file
        text_file = os.path.basename(os.path.splitext(file)[0] + "_fr.txt")
        # print(os.path.basename(text_file))
        filepath = os.path.join("dags/kpmg-pipeline/scraper/fr_text", text_file)
        print(filepath)
        with open(filepath, "w") as output:
            for row in fr:
                output.write(row)
            # little feedback
            print(f'french extracted into: {filepath}')
