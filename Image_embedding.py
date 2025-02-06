from transformers import CLIPProcessor, TFCLIPModel
from PIL import Image
import tensorflow as tf
import os
import numpy as np
import re
from qdrant_client.http.models import Filter, FieldCondition, MatchValue


# Load the CLIP model and processor
model_name = "openai/clip-vit-base-patch32"  # Pretrained CLIP model
model = TFCLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

# Give your folder path to extract the image files.
folder = r"D:\Animal_dataset_image_project" 

# Get a list of all image files
image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
print()
print("Managing Image Files.")
print()
image_files = [f for f in os.listdir(folder) if f.lower().endswith(image_extensions)]


from qdrant_client import QdrantClient , models
from qdrant_client.models import Filter, VectorParams, Distance
client = QdrantClient(url = "http://localhost:6333")


def create_collection():
     client.delete_collection(collection_name="Animal_information_images")
     print()
     print("Creating Collection.")
     print()
     client.create_collection(
         collection_name="Animal_information_images",
         vectors_config={
             "animal_image": models.VectorParams(size=512, distance=models.Distance.COSINE),
         },
     )


def store_embeddings():
          print()
          print("Storing Embeddings.")
          print()
          # Load and preprocess the image
          for i in range(len(image_files)):
               image_path = os.path.join(folder, image_files[i])  
               image = Image.open(image_path).convert("RGB")
               inputs = processor(images=image, return_tensors="tf", padding=True)

          # Generate semantic embeddings
               image_features = model.get_image_features(**inputs)
          # Generating name of image      
               base_name = image_files[i]
               base_name = re.sub(r'\.[a-zA-Z0-9]+$', '', base_name)
               # Remove all non-alphabetic characters
               base_name = re.sub(r'[^a-zA-Z]', '', base_name)
               name_of_animal = base_name.capitalize()
          # Normalize the embeddings for cosine similarity
               image_embeddings = tf.linalg.l2_normalize(image_features, axis=-1)
               client.upsert(
                  collection_name="Animal_information_images",
                  points=[
                     models.PointStruct(
                        id=i,
                        payload={
                          "name": name_of_animal,
                        },
                        vector={"animal_image" : image_embeddings[0]},
                                        ),
                         ],
                             )
               
# create_collection()
# store_embeddings()               
 
def get_images(img , no_of_images):
           image_path = img
           image = Image.open(image_path).convert("RGB")
           inputs = processor(images=image, return_tensors="tf", padding=True)

           # Generate semantic embeddings
           image_features = model.get_image_features(**inputs)

           # Normalize the embeddings for cosine similarity
           image_embeddings = tf.linalg.l2_normalize(image_features, axis=-1)

           # Save or use the embeddings
           embedding_list = image_embeddings[0].numpy().tolist()

           points = list(client.query_points(
               collection_name="Animal_information_images",
               query=embedding_list,
               using="animal_image",
               limit = no_of_images,
           ))

           ids = []
           for i in range(no_of_images):
               ids.append(points[0][1][i].id)

           return ids , image_files[ids[0]]


def get_images_by_text(name , no_of_images =1):
    payload_filter = Filter(
    must=[
        FieldCondition(
            key="name",  # Replace 'name' with your payload field key
            match=MatchValue(value=name)  # Replace with the value you're searching for
        )
    ]
  )

# Use query_points to search based on the filter
    points = list(client.query_points(
      collection_name="Animal_information_images",  # Replace with your collection name
      query_filter=payload_filter,   # Apply the filter
      with_payload=True,       # Include payload in the result
      with_vectors=False,      # Exclude vectors (embeddings) in the result
      limit=no_of_images              # Limit the number of results
 ))
    ids = []
    for i in range(no_of_images):
               ids.append(points[0][1][i].id)

    return ids , image_files[ids[0]]