import uvicorn
# from preprocessing.cleaning_data import Property, preprocess
# from predict.prediction import predict_price
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pandas as pd

import API.azure as azure

app = FastAPI()

class CLA(BaseModel):
    id_pdf: str
    text: str
    cla_class: str
    related_pdf: int
    upload_date: datetime
    url: str
    summary: str

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return "Alive"

@app.get("/filter/{CLA_class}", status_code=status.HTTP_200_OK, response_model=list[CLA])
async def filter_get(CLA_class: str):
    # get CLAs
    # store in panda table
    # filter panda table on given class
    # return filtered CLAs

    df: pd.DataFrame = azure.download_csv_files_to_dataframe()

    if df == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unable to fetch data")
    
    # DO STUFF with df
    CLA_list = []

    return CLA_list

@app.get("/urls", status_code=status.HTTP_200_OK)
async def urls_get():
        # get CLAs
        # store in panda table
        # get urls ?
        # return urls

    df: pd.DataFrame = azure.download_csv_files_to_dataframe()

    if df == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unable to fetch data")
    
    # DO STUFF with df
    urls = []

    return urls

@app.get("/statistics/{CLA_class}", status_code=status.HTTP_200_OK)
async def statistics_get(CLA_class: str):
    # get CLAs
    # store in panda table
    # look for or do arithamtics for statistics
    # which statitistics yet to be decided ?

    df: pd.DataFrame = azure.download_csv_files_to_dataframe()

    if df == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unable to fetch data")
    
    # DO STUFF with df
    statistics = df

    return statistics

@app.get("/summary/{id}", status_code=status.HTTP_200_OK)
async def summary_get(id: str):
    
    df: pd.DataFrame = azure.download_csv_files_to_dataframe()

    if df == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unable to fetch data")
    
    # DO STUFF with df
    summary = df

    return summary

@app.get("/related/{id}", status_code=status.HTTP_200_OK)
async def related_get(id: str):
    # get cla for id
    # get related clas based of cla we got id for 

    df: pd.DataFrame = azure.download_csv_files_to_dataframe()

    if df == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unable to fetch data")
    
    # DO STUFF with df
    related = df

    return related


@app.post("/new-CLA")
async def run_post(new_CLA_data: CLA):
    processed_data = process(new_CLA_data)
    # prediction = predict_price(preprocessed_data)



    return processed_data



@app.get("/new-CLA", status_code=status.HTTP_200_OK, response_model=CLA)
async def CLA_get():
    # get information from csv store

    
    # return dats in expected format 

    return ('Expected format:\
{"data":\
{"id_pdf": str,\
"text": str,\
"cla_class": str,\
"related_pdf": int,\
"upload_date": datetime,\
"url": str,\
"summary": str,\
},}')