# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from flask import Flask, jsonify, request, render_template
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os
from fastapi import FastAPI


#app = Flask(__name__)
app = FastAPI()

dynamodb = boto3.resource('dynamodb',region_name=os.environ['AWS_REGION'])
table = dynamodb.Table(os.environ['DDB_TABLE_LIV1'])
tableQuestions = dynamodb.Table(os.environ['DDB_QUESTIONS'])
tableUserdata = dynamodb.Table(os.environ['DDB_UDATA'])




def get_user(id):
    try:
        response = table.get_item(Key={'Id': id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

#Home Page
#@app.route('/')
@app.get("/")
def home():
  return render_template('index.html')


# PUT /api/user data: {name:}
@app.put("/api/user")
#@app.route('/api/user', methods=['PUT'])
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
@app.post("/api/user")
#@app.route('/api/user')
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
@app.get("/api/users")
#@app.route('/api/users')
def getusers():
    response = table.scan()
    return response


@app.post("/api/user")
#@app.route('/api/user', methods=['POST'])
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

def get_questions(id):
    try:
        response = tableQuestions.get_item(Key={'id': id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

@app.post("/api/udata")
#@app.route('/api/udata')
def putUserData():
    query_params = request.args.to_dict(flat=False)
    request_data = request.get_json()
    response = setuserdata(request_data)
    return response


@app.get("/api/levelQ6R")
#@app.route('/api/levelQ6R')
def getquestions():
    query_params = request.args.to_dict(flat=False)
    id = query_params['id'][0]
    iduser = query_params['idu'][0]

    if(id==0):
     idTpl = random.randint(0, 5)
        Item={
            'iduser': iduser,
            'type' : 'template'
            'info': {
                'id': nome
            }
           }
       Udata={
            'iduser': iduser,
            'type' : 'template'
           }
    userTplInfo = setuserdata(Udata)
    response = get_questions(userTplInfo['info']['id'] )
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
       if ('Item' in response):
           return { 'Item': str(response['Item']) }
       return { 'msg' : 'Item not found!' }
    return {
       'msg': 'error occurred',
       'response': response
    }

def setuserdata(userdata):

    response = tableUserdata.put_item(
            Item={
            'iduser': userdata['iduser'],
            'type': userdata['type'],
            'info': userdata['info']
           }
        )
        return response

def getuserdata(userdata):
    try:
        response = tableUserdata.get_item(Key={'id': userdata['info']['id'],'type':userdata['type']})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8080)
