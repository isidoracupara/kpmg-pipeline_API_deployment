from langdetect import detect
import camelot
import os
from utils.upload_file import upload_file

def ocr_fr_detect_v2(file):
    """ 
    This function takes a pdf file as an input and outputs a txt file with the same name.
    The txt file contains only the french text contained in the pdf document.
    Takes approximatly 20 seconds for 6 pages
    """
    # define vowels
    vowels = ['a','e','i','o','u']
    # initialize text list 
    fr = []
    # languages that are labelled as duch
    duch = {'da', 'sl', 'de', 'nl', 'et' ,'no', 'af','fi', 'tl', 'sv', 'so'}
    # languages that are labelled as duch
    french = {'hr', 'ca', 'fr','ro', 'it', 'lv', 'en', 'es', 'cy'}
    # check the file extension
    if file.endswith(".pdf"):
        #print(file) # debug, prints filename
        tables = camelot.read_pdf(file, flavor='stream' , pages= 'all', edge_tol=0)
        # for every detected table (page and text structure)
        for i in range(len(tables)):
            # create an empty language list
            col_lang = []
            # make a df
            data = tables[i].df
            # replace new line (\n) with space
            data.replace('\\n',' ',regex=True, inplace = True)
            # for every column detected
            for j in range(len(data.columns)):
                # put all the text of that column in a list # this takes also out empty rows and lone numbers (as pagenumber)
                text_list = [x for x in tables[i].df[j].values if x != '' if not x.isdigit()] 
                # convert the list to text
                col_text = (' '.join(text_list))
                # if there is at least one vowel (we cannot detect language for numbers)
                if any(char in vowels for char in col_text):
                    # detect language
                    try:
                        language = detect(col_text)
                        # update languages list
                        col_lang.append(language)
                    except:
                        col_lang.append('Error')
                        #print("This row throws and error:", i, j, col_text) # debug, prints table, column and text
                    
                else:
                    col_lang.append('None')
            for k in range(len(data)):
                # put all the text of that column in a list # this takes also out empty rows and lone numbers (as pagenumber)
                #text_list = [x for x in tables[i].df[j].values if x != '' if not x.isdigit()] 
                # for every columns in the row 
                for g in range(len(data.columns)): 
                    text = tables[i].df[g].values[k] 
                    language = col_lang[g]
                    if text == '':
                        pass
                    elif language in french:
                        #print(language,': ', text)
                        fr.append(text)
                    elif language in duch or language == 'None':
                        #print(language,': ', text) # debug, print duch text and columns with no vowels
                        pass
                    else: 
                        
                        if len(text)>1:
                            #print(i, g, language ,text ) # debug, print unexpected languages or errors 
                            # add rows that contains unexpected languages or errors, longer than one digit to the french version
                            fr.append(text)
                         
        # Outputs the french text in a text file
        text_file = os.path.basename(os.path.splitext(file)[0] + "_fr.txt")
        # print(os.path.basename(text_file))
        filepath = os.path.join("dags/kpmg-pipeline/text_extractor/fr_text", text_file)
        with open(filepath, "w") as output:
            for row in fr:
                output.write(row)
                # add a space between words
                output.write(' ')
            # little feedback
            upload_file(filepath, text_file)
            print(f'french extracted into: {filepath}')
    else:
        print('not a pdf')
        pass