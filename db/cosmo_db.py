import os
from azure.cosmos import CosmosClient

def CosmoDBConnection(container_name, database_name="spinnaker-client"):
    try:
        COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
        COSMOS_KEY = os.getenv("COSMOS_KEY")
        
        client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        return client, database, container
    except Exception as e:
        print(f"Error connecting Cosmo DB: {str(e)}")
        return None, None, None
    
    