from decimal import Decimal
import json
import boto3


def load_users(users):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Items')
    for movie in movies:
        id = int(movie['id'])
        title = movie['info']
        print("Adding user:", id, title)
        table.put_item(Item=movie)


if __name__ == '__main__':
    with open("userdata.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    load_users(movie_list)