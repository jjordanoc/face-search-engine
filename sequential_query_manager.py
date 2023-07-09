import numpy as np
from typing import Tuple, List
import face_recognition
from helpers import measure_execution_time

from heap import MaxHeap


class SequentialQueryManager:

    @measure_execution_time
    def __init__(self, collection: List[Tuple[str, np.ndarray]]) -> None:
        self.collection = collection

    @measure_execution_time
    def range_query(self, q: str, r: float) -> List[List[Tuple[str, float]]]:
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

    @measure_execution_time
    def knn_query(self, q: str, k: int) -> List[List[Tuple[str, float]]]:
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

            def __repr__(self) -> str:
                return str((self.file_name, self.dist))

        # process face of query path file
        image = face_recognition.load_image_file(q)
        query = face_recognition.face_encodings(image)

        result: List[List[Tuple[str, float]]] = []

        for face_embed in query:
            result_heap = MaxHeap[DistWrapper]()
            for c in self.collection:
                dist: float = np.linalg.norm(c[1] - face_embed)
                if result_heap.size() < k:
                    result_heap.push(DistWrapper(d=dist, embed=c[1], file_name=c[0]))
                elif result_heap.top().dist > dist:
                    result_heap.pop()
                    result_heap.push(DistWrapper(d=dist, embed=c[1], file_name=c[0]))
            result.append([(wrapper.file_name, wrapper.dist) for wrapper in result_heap.heapsort()])
        return result
