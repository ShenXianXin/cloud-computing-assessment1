""" database """

import json
import boto3


def _get_service_resource():
    dynamodb = boto3.resource("dynamodb", endpoint_url="dynamodb")
    return dynamodb


def init_table(dynamodb=None):

    if not dynamodb:
        dynamodb = _get_service_resource()

    # check if table exists
    dynamodb_client = dynamodb.meta.client
    table_name = "Posts"
    existing_tables = dynamodb_client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "user", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "title", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "user", "AttributeType": "S"},
                {"AttributeName": "title", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        print("Table status:", table.table_status)
    else:
        print("Table exist. Skip table creating process.")

    # load sample posts
    load_posts(dynamodb)


def load_posts(dynamodb=None):
    """
    no error raised, even already existed.
    so what is the difference between put item and update item?
    It seems PutItem will replace the item, UpdateItem will just update it.
    """

    if not dynamodb:
        dynamodb = _get_service_resource()

    table = dynamodb.Table("Posts")

    # check if table is empty
    count = table.item_count
    if count == 0:
        with open("postdata.json") as json_file:
            posts = json.load(json_file)
        for post in posts:
            user = post["user"]
            title = post["title"]
            print("Adding post:", user, title)
            table.put_item(Item=post)
    else:
        print(f"Table has {count} item(s). Skip load sample posts process.")


def get_posts(dynamodb=None):

    if not dynamodb:
        dynamodb = _get_service_resource()

    table = dynamodb.Table("Posts")

    response = table.scan()
    items = response["Items"]
    return items


def put_post(title, text, dynamodb=None):

    if not dynamodb:
        dynamodb = _get_service_resource()

    table = dynamodb.Table("Posts")

    try:
        table.put_item(
            Item={"user": "xianxin shen", "title": title, "details": {"text": text}}
        )
    except Exception as e:
        print(e)
