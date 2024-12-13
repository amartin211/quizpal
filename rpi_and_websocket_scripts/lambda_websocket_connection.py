import json
import boto3
import os
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("WebSocketConnections")


def get_client_id(connection_id):
    # Implement your logic to retrieve client_id from DynamoDB using connection_id
    # For example, you might query DynamoDB where connectionId equals the provided connection_id
    # and return the client_id field of the matching record.
    response = table.query(
        IndexName="connectionId-index",  # Assuming you have a GSI with connectionId as the key
        KeyConditionExpression=Key("connectionId").eq(connection_id),
    )
    items = response.get("Items", [])
    if items:
        return items[0].get("client_id")
    return None


def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    print(connection_id)
    route_key = event["requestContext"]["routeKey"]

    # Handling client_id for the $connect route
    client_id = None
    if "queryStringParameters" in event and event["queryStringParameters"] is not None:
        client_id = event["queryStringParameters"].get("client_id")

    if route_key == "$connect":
        if client_id is not None:
            handle_connect(connection_id, client_id)
        else:
            print("Client ID not provided in connection request.")
            return {"statusCode": 400, "body": "Client ID not provided"}
    elif route_key == "$disconnect":
        handle_disconnect(connection_id)
    elif route_key == "$send_message":
        body = json.loads(event["body"])
        message = body["message"]
        handle_send_message(message, connection_id)

    return {"statusCode": 200}


def handle_connect(connection_id, client_id):
    # Add connection_id to DynamoDB
    table.put_item(Item={"connectionId": connection_id, "client_id": client_id})


def handle_disconnect(connection_id):
    # Retrieve the client_id using connection_id
    client_id = get_client_id(connection_id)
    print(client_id)
    if client_id is not None:
        # Scan for all records with the specific client_id and delete them
        response = table.scan(FilterExpression=Attr("client_id").eq(client_id))

        # Iterate over the items and delete each one
        for item in response["Items"]:
            table.delete_item(Key={"client_id": item["client_id"], "connectionId": item["connectionId"]})
    else:
        print(f"No client_id found for connection_id: {connection_id}")


def handle_send_message(message, connection_id):
    # Retrieve all connection_ids from DynamoDB
    # (you might want to filter to select specific recipients)
    # response = table.scan()
    # connection_ids = [item['connectionId'] for item in response['Items']]

    # Send the message to all connected devices
    apigatewaymanagementapi = boto3.client("apigatewaymanagementapi", endpoint_url=os.environ["APIG_ENDPOINT"])
    apigatewaymanagementapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(
            {
                "message": message,
                #'sender_connection_id': connection_id
            }
        ),
    )

    # for conn_id in connection_ids:
    #    apigatewaymanagementapi.post_to_connection(
    #        ConnectionId=conn_id,
    #        Data=json.dumps({
    #            'message': message,
    #            'sender_connection_id': connection_id
    #        })
    #    )
