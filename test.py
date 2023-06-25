from KNN_Sequential import *
import pickle


def main() -> None:
    with open("out.embeds", mode="rb") as collection_file:
        collection = pickle.load(collection_file)
    google = KNNSequentialQueryManager(collection)
    print(google.linear_search(q="C:/Users/Jose/Desktop/db2-project-3/lfw/Adam_Sandler/Adam_Sandler_0002.jpg", k=4))


if __name__ == "__main__":
    main()
