import os

from astrapy import DataAPIClient

from embedding_create import create_embeddings

# Fetching necessary environment variables for AstraDB configuration
ASTRA_DB_APPLICATION_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_API_ENDPOINT = os.environ["ASTRA_DB_API_ENDPOINT"]
ASTRA_DB_KEYSPACE = os.environ.get("ASTRA_DB_KEYSPACE")
COLLECTION_NAME = "town_content"

# Preparing a list of queries about the town Shadowfen
queries = [
    "What are the locations within Shadowfen?",
    "Who is Eldermarsh Thorne?",
    "Who is Brom Stoutfist?",
    "What is The Gloomwater Brewery?",
    "What is the terrain like surrounding Shadowfen?",
    "Who created Shadowfen?",
    "What is the climate of Shadowfen?",
    "What is the population of Shadowfen?",
    "What is the history of Shadowfen?",
    "Where can I get a drink in Shadowfen?",
]

# Generating embeddings for each query using a custom embedding creation function
embedding_list = create_embeddings(queries)

# Establishing a connection to Astra DB with the provided credentials and keyspace
client = DataAPIClient()
db = client.get_database(
    ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace=ASTRA_DB_KEYSPACE,
)

# Get (an astrapy reference to) the db collection
collection = db.get_collection(name=COLLECTION_NAME)

# Iterating through each query to perform a similarity search in the database
for embedding, query in zip(embedding_list, queries):
    # Executing the find operation on the collection with the specified parameters
    search_results = collection.find(
        sort={"$vector": embedding.tolist()},
        limit=2,
        projection={"text": True},
        include_similarity=True,
    )

    print("=" * 30)
    print(f"QUESTION: {query}")
    print("-" * 30)
    # Iterating through the retrieved documents to print their content
    for document in search_results:
        print(document["text"])
        print(f"    [Similarity: {document['$similarity']:.4f}]")
        print("\n")

    print("\n\n")
