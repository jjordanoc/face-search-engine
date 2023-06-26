import pickle
from typing import Tuple, List
from rtree import index
import face_recognition
import numpy as np
from helpers import measure_execution_time


class RTreeQueryManager:
    def __init__(self, m: int, collection: List[Tuple[str, np.ndarray]]) -> None:
        p = index.Property()
        p.dimension = 128  # D
        p.buffering_capacity = m  # M
        self.collection_ = collection
        self.idx = index.Index(properties=p)
        for i in range(len(collection)):
            self.idx.insert(id=i, coordinates=collection[i][1])

    @measure_execution_time
    def knn_query(self, q: str, k: int) -> List[List[Tuple[str, float]]]:
        image_query = face_recognition.load_image_file(q)
        query_embeds = face_recognition.face_encodings(image_query)
        total_result = list()
        for face_embed in query_embeds:
            nearest = self.idx.nearest(coordinates=face_embed, num_results=k)
            partial_result = list()
            for item_id in nearest:
                obj = self.collection_[item_id]
                partial_result.append((obj[0], np.linalg.norm(obj[1] - face_embed)))
            total_result.append(partial_result)
        return total_result


if __name__ == "__main__":
    with open("out.embeds", mode="rb") as collection_file:
        collection = pickle.load(collection_file)
    rtree_query_manager = RTreeQueryManager(collection=collection, m=5)
    print(rtree_query_manager.knn_query(q="fotos_test/Martin Vizcarra/foto4.jpg", k=2))
