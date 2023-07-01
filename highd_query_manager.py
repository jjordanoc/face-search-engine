from helpers import measure_execution_time
import face_recognition
from typing import List, Tuple
import numpy as np
import faiss


class HighDQueryManager:
    def __init__(self, m: int, collection: List[Tuple[str, np.ndarray]]) -> None:
        self.collection = collection

        d = 128
        self.index = faiss.IndexLSH(d, m)
        self.index.add(np.ascontiguousarray(np.asarray([i[0] for i in collection], "float32")))

    @measure_execution_time
    def knn_query(self, q: str, k: int) -> List[List[Tuple[str, float]]]:
        # process face of query path file
        image = face_recognition.load_image_file(q)
        query_embeds = face_recognition.face_encodings(image)

        result: List[List[Tuple[str, float]]] = []
        ranking, id_array = self.index.search(x=np.asarray([face_embed for face_embed in query_embeds], "float32"), k=k)

        ranking_iter = np.nditer(ranking, flags=['f_index'])

        for face_id in id_array:
            partial_result: List[Tuple[str, float]] = []

            for idx in face_id:
                obj = self.collection[idx]
                partial_result.append((obj[0], ranking_iter[0]))

                ranking_iter.iternext()

            result.append(partial_result)

        return result
