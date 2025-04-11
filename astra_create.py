import os

from astrapy import DataAPIClient
from astrapy.info import CollectionDefinition

ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_KEYSPACE = os.environ.get("ASTRA_DB_KEYSPACE")
COLLECTION_NAME = "town_content"

# Initialize connection to Astra DB
client = DataAPIClient()
db = client.get_database(
    ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace=ASTRA_DB_KEYSPACE,
)

# Create collection
db.create_collection(
    COLLECTION_NAME,
    definition=(
        CollectionDefinition.builder()
        .set_vector_dimension(768)
        .build()
    )
)
