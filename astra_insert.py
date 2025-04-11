import os
import uuid

from astrapy import DataAPIClient

from doc_chunker import chunk_file
from embedding_create import create_embeddings

# Fetching necessary environment variables for AstraDB configuration
ASTRA_DB_APPLICATION_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_API_ENDPOINT = os.environ["ASTRA_DB_API_ENDPOINT"]
ASTRA_DB_KEYSPACE = os.environ.get("ASTRA_DB_KEYSPACE")
COLLECTION_NAME = "town_content"


# Initialize connection to Astra DB
client = DataAPIClient()
db = client.get_database(
    ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace=ASTRA_DB_KEYSPACE,
)

# Chunk the sample file into paragraphs
paragraphs = chunk_file("./towns/shadowfen.txt")

# Create embeddings for each paragraph
embeddings_list = create_embeddings(paragraphs)

documents = []  # Initialize an empty list to hold document dictionaries

for embeddings, paragraph in zip(embeddings_list, paragraphs):
    # Create a dictionary for the current document
    document = {
        "_id": uuid.uuid4(),
        "text": paragraph,
        "$vector": embeddings.tolist(),
    }

    # Append the document dictionary to the list
    documents.append(document)

# Get (an astrapy reference to) the db collection
collection = db.get_collection(name=COLLECTION_NAME)

# Insert the documents
res = collection.insert_many(documents=documents)

print(f"Inserted {len(res.inserted_ids)} chunks.")
