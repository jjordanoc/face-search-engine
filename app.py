from fastapi import FastAPI, File, UploadFile, Form
from PIL import Image

import os
import io
import uvicorn
import pickle

from fastapi.middleware.cors import CORSMiddleware
from rtree_query_manager import RTreeQueryManager
from sequential_query_manager import SequentialQueryManager
from highd_query_manager import HighDQueryManager


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("out.embeds", mode="rb") as collection_file:
    collection = pickle.load(collection_file)

sequential_query_manager = SequentialQueryManager(collection=collection)
rtree_query_manager = RTreeQueryManager(collection=collection, m=3)
high_d_query_manager = HighDQueryManager(collection=collection, num_bits=2000)
temporary_query_path1 = "query1.jpg"
temporary_query_path2 = "query2.jpg"
temporary_query_path3 = "query3.jpg"


@app.post('/sequential_range')
async def get_knn_sequential(file: UploadFile = File(...), r: str = Form(...)) -> dict:
    r = float(r)
    data = await file.read()

    with open(temporary_query_path1, 'wb') as f:
        f.write(data)

    result = sequential_query_manager.range_query(q=temporary_query_path1, r=r)
    os.remove(temporary_query_path1)

    print(result)
    return {
        'result': result,
        'response': 200
        }


@app.post('/sequential')
async def get_knn_sequential(file: UploadFile = File(...), k: str = Form(...)) -> dict:
    k = int(k)
    data = await file.read()

    with open(temporary_query_path1, 'wb') as f:
        f.write(data)

    result = sequential_query_manager.knn_query(q=temporary_query_path1, k=k)
    os.remove(temporary_query_path1)

    print(result)
    return {
        'result': result,
        'response': 200
        }


@app.post('/rtree')
async def get_knn_tree(file: UploadFile = File(...), k: str = Form(...)) -> dict:
    k = int(k)
    data = await file.read()

    with open(temporary_query_path1, 'wb') as f:
        f.write(data)

    result = rtree_query_manager.knn_query(q=temporary_query_path2, k=k)
    os.remove(temporary_query_path2)

    return {
        'result': result,
        'response': 200
        }


@app.post('/highd')
async def get_knn_highd(file: UploadFile = File(...), k: str = Form(...)) -> dict:
    k = int(k)
    data = await file.read()

    with open(temporary_query_path1, 'wb') as f:
        f.write(data)

    result = high_d_query_manager.knn_query(q=temporary_query_path3, k=k)
    os.remove(temporary_query_path3)

    return {
            'result': result,
            'response': 200
        }


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', reload=True, port=8000)
