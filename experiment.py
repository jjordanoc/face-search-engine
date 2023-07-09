import os
import random

from rtree_query_manager import RTreeQueryManager
from sequential_query_manager import *
from highd_query_manager import *
import pickle


def print_result(result):
    for i in result:
        for j in i:
            print(j)
    print("\n\n")


def main() -> None:
    with open("out.embeds", mode="rb") as collection_file:
        collection = pickle.load(collection_file)
    k = 8
    for n in [100*(2**p) for p in range(0, 1)]:
        print("=" * 60)
        print(f"Extracting random sample of size {n}")
        sample = random.sample(collection, n)
        print("Building managers")
        sequential_query_manager = SequentialQueryManager(collection=sample)
        rtree_query_manager = RTreeQueryManager(collection=sample, m=3)
        high_d_query_manager = HighDQueryManager(collection=sample, num_bits=2000)
        print()
        query = os.path.join(os.getcwd(), "lfw/Adam_Sandler/Adam_Sandler_0002.jpg")
        print("Sequential query")
        print_result(sequential_query_manager.knn_query(q=query, k=k))
        print("RTree query")
        print_result(rtree_query_manager.knn_query(q=query, k=k))
        print("LSH query")
        print_result(high_d_query_manager.knn_query(q=query, k=k))
        print()


if __name__ == "__main__":
    main()
