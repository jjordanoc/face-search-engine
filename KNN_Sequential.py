import numpy as np
from typing import Tuple, List
import face_recognition

from Heap import MaxHeap


class KNNSequentialQueryManager:

    def __init__(self, collection: List[Tuple[str, np.ndarray]]) -> None:
        self.collection = collection

    def range_search(self, q: str, r: float) -> List[List[Tuple[str, float]]]:
        # process face of query path file
        image = face_recognition.load_image_file(q)
        query = face_recognition.face_encodings(image)

        result: List[List[Tuple[str, float]]] = []

        for face_embed in query:
            result_tmp: List[Tuple[str, float]] = []
            for c in self.collection:
                dist: float = np.linalg.norm(c[1] - face_embed)
                if dist < r:
                    result_tmp.append((c[0], dist))
            result_tmp = sorted(result_tmp, key=lambda x: x[1], reverse=False)
            result.append(result_tmp)

        return result

    def linear_search(self, q: str, k: int) -> List[List[Tuple[str, float]]]:
        class DistWrapper:
            def __init__(self, d: float, embed: np.ndarray, file_name: str):
                self.dist = d
                self.embed = embed
                self.file_name = file_name

            def __lt__(self, other):
                return self.dist < other.dist

            def __gt__(self, other):
                return self.dist > other.dist

            def __eq__(self, other):
                return self.dist == other.dist

        # process face of query path file
        image = face_recognition.load_image_file(q)
        query = face_recognition.face_encodings(image)

        result: List[List[Tuple[str, float]]] = []

        for face_embed in query:
            result_tmp = MaxHeap[DistWrapper]()
            for c in self.collection:
                dist: float = np.linalg.norm(c[1] - face_embed)
                if result_tmp.size() < k:
                    result_tmp.push(DistWrapper(d=dist, embed=c[1], file_name=c[0]))
                elif result_tmp.top().dist > dist:
                    result_tmp.pop()
                    result_tmp.push(DistWrapper(d=dist, embed=c[1], file_name=c[0]))
            result_tmp2: List[Tuple[str, float]] = []

            while result_tmp.size() != 0:
                result_tmp2.append((result_tmp.top().file_name, result_tmp.top().dist))
                result_tmp.pop()
            result_tmp2 = sorted(result_tmp2, key=lambda x: x[1], reverse=False)
            result.append(result_tmp2)

        return result
