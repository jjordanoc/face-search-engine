import os
from sequential_query_manager import *
import pickle


def main() -> None:
    with open("out.embeds", mode="rb") as collection_file:
        collection = pickle.load(collection_file)
    sequential_query_manager = SequentialQueryManager(collection)
    query = os.path.join(os.getcwd(), "lfw/Adam_Sandler/Adam_Sandler_0002.jpg")
    print(sequential_query_manager.knn_query(q=query, k=4))


if __name__ == "__main__":
    main()
