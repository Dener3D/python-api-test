from asyncio.log import logger
from http.client import HTTPException
from select import select
import shutil
import string
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from numpy import byte, save
from pydantic import BaseModel
#from os import curdir
#import mysql.connector
import json
import requests
#import os
#import time
import PyPDF2
from PyPDF2 import PdfFileMerger, pdf
from starlette.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

files = []

@app.on_event("startup")
async def startup():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

#@app.get('/files')
#async def get_all():
    #return files

@app.get("/file")
async def get_file(file_path: str):
    try:
        return FileResponse(path=file_path, filename=file_path, media_type='pdf')
    except Exception as ex:
        logger.exception("Error")
        raise HTTPException(status_code=500, detail=str(ex))
        return ({"status_code" : "500"})

@app.post("/upload")
async def create_file(file: List[UploadFile] = File(..., media_type='application/pdf')):
    merger = PdfFileMerger()
    for f in file:
        with open(f'{f.filename}', "wb") as image:
            shutil.copyfileobj(f.file, image)
            pdf_file = PyPDF2.PdfFileReader(f.file)
            files.append({'id' : len(files) + 1, 'nome' : f.filename}) 
            merger.append(pdf_file)

    merger.write("merged.pdf")
    merger.close()
        
        
    return {"download_file" : "http://127.0.0.1:8000/file?file_path=merged.pdf"}






