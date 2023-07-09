import os

from rtree_query_manager import RTreeQueryManager
from sequential_query_manager import *
from highd_query_manager import *
import pickle


def print_result(result):
    for i in result:
        for j in i:
            print(j)
        print("")
    print("\n")


def main() -> None:
    with open("out.embeds", mode="rb") as collection_file:
        collection = pickle.load(collection_file)

    sequential_query_manager = SequentialQueryManager(collection=collection)
    rtree_query_manager = RTreeQueryManager(collection=collection, m=3)
    high_d_query_manager = HighDQueryManager(collection=collection, num_bits=2000)

    query = os.path.join(os.getcwd(), "lfw/Abdullatif_Sener/Abdullatif_Sener_0002.jpg")

    print_result(sequential_query_manager.knn_query(q=query, k=4))
    print_result(rtree_query_manager.knn_query(q=query, k=4))
    print_result(high_d_query_manager.knn_query(q=query, k=4))


if __name__ == "__main__":
    main()
