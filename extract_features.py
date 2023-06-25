import os
import numpy as np
from typing import Tuple, List
import pickle
import face_recognition

PATH_TO_IMAGES = os.path.join(os.getcwd(), "lfw")

"""
Compute the embeddings for all images in the dataset.
When an image has more than 1 face, two entries are created
containing the same file name with different embeddings.
The output will be given in the following format in a file called out.embeds:
[
(path_to_image_1, embeddings_face_1_image_1),
(path_to_image_1, embeddings_face_2_image_1),
(path_to_image_2, embeddings_face_1_image_2),
...
]
"""


def main():
    outfile = open("out.embeds", mode="wb")
    output: List[Tuple[str, np.ndarray]] = list()
    path = os.path.join(os.getcwd(), "fotos_test")
    for subdir, dirs, files in os.walk(path):
        for file in files:
            face_file = os.path.join(subdir, file)
            image = face_recognition.load_image_file(face_file)
            face_embedding_list = face_recognition.face_encodings(image)
            for face_embedding in face_embedding_list:
                output.append((face_file, face_embedding))
    pickle.dump(output, outfile)
    outfile.close()



if __name__ == "__main__":
    main()
