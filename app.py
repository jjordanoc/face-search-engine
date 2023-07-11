import os
import pickle
import random

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
import json
from fastapi.middleware.cors import CORSMiddleware

from highd_query_manager import HighDQueryManager
from rtree_query_manager import RTreeQueryManager
from sequential_query_manager import SequentialQueryManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

managers = {

}


@app.on_event("startup")
async def startup_event():
    with open("out.embeds", mode="rb") as collection_file:
        collection = pickle.load(collection_file)

    managers["sequential"] = SequentialQueryManager(collection=collection)
    managers["rtree"] = RTreeQueryManager(collection=collection, m=3)
    managers["highd"] = HighDQueryManager(collection=collection, num_bits=2000)


@app.post('/sequential_range')
async def get_range_sequential(file: UploadFile = File(...), r: str = Form(...)) -> dict:
    r = float(r)
    data = await file.read()

    with open("sequential_query.jpg", 'wb') as f:
        f.write(data)

    result = managers["sequential"].range_query(q="sequential_query.jpg", r=r)
    os.remove("sequential_query.jpg")

    print(result)
    return {
        'result': json.dumps(result),
        'response': 200
    }


@app.post('/sequential')
async def get_knn_sequential(file: UploadFile = File(...), k: str = Form(...)) -> dict:
    k = int(k)
    data = await file.read()

    with open("sequential_query.jpg", 'wb') as f:
        f.write(data)

    result = managers["sequential"].knn_query(q="sequential_query.jpg", k=k)
    os.remove("sequential_query.jpg")

    print(result)
    return {
        'result': json.dumps(result),
        'response': 200
    }


@app.post('/rtree')
async def get_knn_tree(file: UploadFile = File(...), k: str = Form(...)) -> dict:
    k = int(k)
    data = await file.read()

    with open("rtree_query.jpg", 'wb') as f:
        f.write(data)

    result = managers["rtree"].knn_query(q="rtree_query.jpg", k=k)
    os.remove("rtree_query.jpg")

    return {
        'result': json.dumps(result),
        'response': 200
    }


@app.post('/highd')
async def get_knn_highd(file: UploadFile = File(...), k: str = Form(...)) -> dict:
    k = int(k)
    data = await file.read()

    with open("highd_query.jpg", 'wb') as f:
        f.write(data)

    result = managers["highd"].knn_query(q="highd_query.jpg", k=k)
    os.remove("highd_query.jpg")

    return {
        'result': json.dumps(result),
        'response': 200
    }


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000)
