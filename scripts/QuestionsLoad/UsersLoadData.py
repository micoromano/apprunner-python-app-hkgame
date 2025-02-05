from decimal import Decimal
import json
import boto3


def load_users(users):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('QuestionsHackerGame')
    for user in users:
        id = int(user['id'])
        title = user['info']
        print("Adding question:", id, title)
        table.put_item(Item=user)


if __name__ == '__main__':
    with open("userdata.json") as json_file:
        user_list = json.load(json_file, parse_float=Decimal)
    load_users(user_list)