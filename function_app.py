import logging
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions

app = func.FunctionApp()

# Cosmos DB Configuration
ENDPOINT = "https://resumevisitorcount.documents.azure.com:443/"
KEY = "9d2DMjb6b7EgNr2IaXBtJB4Np6MmU1cNT1i6SDsWt5kghNH3OsWGTaOc1ApKuOO1mgyFzpW2JpcqACDb5fk9yQ=="
DATABASE_NAME = "VisitorCounterDB"
CONTAINER_NAME = "VisitorCount"

@app.function_name(name="HttpTrigger1")
@app.route(route="req")
def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {"Access-Control-Allow-Origin": "*"}  #  Enable CORS
    try:
        # Connect to Cosmos DB
        client = CosmosClient(ENDPOINT, KEY)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # Retrieve and update visitor count
        visitor = container.read_item(item="visitorCount", partition_key="visitorCount")
        visitor["count"] += 1
        container.upsert_item(visitor)

        #  Return JSON response
        return func.HttpResponse(
            json.dumps({"count": visitor["count"]}),
            status_code=200,
            headers=headers,
            mimetype="application/json"
        )
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Error updating visitor count.", status_code=500, headers=headers)
