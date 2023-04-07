# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from flask import Flask, jsonify, request, render_template
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb',region_name=os.environ['AWS_REGION'])
table = dynamodb.Table(os.environ['DDB_TABLE_LIV1'])



def get_user(id):
    try:
        response = table.get_item(Key={'Id': id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

#Home Page
@app.route('/')
def home():
  return render_template('index.html')


# PUT /api/user data: {name:}
@app.route('/api/user', methods=['PUT'])
def put_user():
    request_data = request.get_json()
    try:
      id = request_data['Id']
    except:
      plot = "NA"
    try:
      nome = request_data['info']['nome'] 
    except:
      nome = ["NA"]
    try:
      cognome = request_data['cognome']['cognome']
    except:
      cognome = "NA"
    try:
      attivo = request_data['info']['attivo']
    except:
      attivo = ["NA"]
    try:
      username = request_data['info']['username']
    except:
      username = "NA"
    try:
      password = request_data['info']['password'] 
    except:
      password = ["NA"]
    try:
      rank = request_data['info']['rank'] 
    except:
      rank = 0
    try:
      running_time_secs = request_data['info']['running_time_secs']
    except:
      running_time_secs = 0
    response = table.put_item(
       Item={
        'Id': request_data['Id'],
        'info': {
            'nome': nome,
            'cognome': cognome,
            'attivo': attivo,
            'username': username,
            'password': password,
            'rank': rank
        }
       }
    )
    return response

# GET /api/user?id=<string>
@app.route('/api/user')
def getuser():
    query_params = request.args.to_dict(flat=False)
    id = query_params['id'][0]
    response = get_user(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
       if ('Item' in response):
           return { 'Item': str(response['Item']) }
       return { 'msg' : 'Item not found!' }
    return { 
       'msg': 'error occurred',
       'response': response
    }

# GET /api/user
@app.route('/api/users')
def getusers():
    response = table.scan()
    return response


@app.route('/api/user', methods=['POST'])
def post_user():
    request_data = request.get_json()
    try:
      id = request_data['Id']
    except:
      plot = "NA"
    try:
      nome = request_data['info']['nome'] 
    except:
      nome = ["NA"]
    try:
      cognome = request_data['cognome']['cognome']
    except:
      cognome = "NA"
    try:
      attivo = request_data['info']['attivo']
    except:
      attivo = ["NA"]
    try:
      username = request_data['info']['username']
    except:
      username = "NA"
    try:
      password = request_data['info']['password'] 
    except:
      password = ["NA"]
    try:
      rank = request_data['info']['rank'] 
    except:
      rank = 0
    try:
      running_time_secs = request_data['info']['running_time_secs']
    except:
      running_time_secs = 0
    response = table.put_item(
        Item={
        'Id': request_data['Id'],
        'info': {
            'nome': nome,
            'cognome': cognome,
            'attivo': attivo,
            'username': username,
            'password': password,
            'rank': rank
        }
       }
    )
    return response



if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8080)
