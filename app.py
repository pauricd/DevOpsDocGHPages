# app.py

import boto3

from flask import Flask, jsonify, request
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
dynamoTableName = 'musicTable'

def create_table(table_name):
    """
    A description of the function
    
    :param param1: explanation of param1
    :type param1: state the parameter type
    :param param2: explanation of param2
    :type param2: state the parameter type
    
    :return: state what is returned by the function
    :rtype: the type(s) of the return value(s)
    """

    if dynamoTableName not in client.list_tables()['TableNames']:
        table = client.create_table(
                TableName=table_name,
            KeySchema=[
                {'AttributeName': 'artist',
                 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'artist',
                 'AttributeType': 'S'}],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10})

        client.put_item(
        TableName=table_name,
        Item={
        'artist': {'S': 'The Beatles' },
        'song': {'S': 'Yesterday' }
        })

@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        """
        The main route

        :return: the welcome message
        :rtype: string
        """
        return {"hello": "world"}

@api.route("/get-items")
class GetItems(Resource):
	def get(self):
		"""
		Returns all of the items in the table, in JSON format

		:return: table contents in JSON format
		:rtype: Response object
		"""
		return jsonify(client.scan(TableName=dynamoTableName))
#
# @app.route("/add", methods=["POST"])
# def create_entry():
#     """
#     Add items with a POST request
#
#     :return: the new entry in JSON format
#     :rtype: Response object
#     """
#     artist = request.json.get('artist')
#     song = request.json.get('song')
#     if not artist or not song:
#         return jsonify({'error': 'Please provide Artist and Song'}), 400
#
#     resp = client.put_item(
#         TableName=dynamoTableName,
#         Item={
#             'artist': {'S': artist },
#             'song': {'S': song }
#         }
#     )
#
#     return jsonify({
#         'artist': artist,
#         'song': song
#     })
#
# @app.route("/get/<string:artist>")
# def get_artist(artist):
#     """
#     Search for an artist with a GET request
#
#     :param artist: the artist's name
#     :type artist: string
#
#     :return: artist-song pair in JSON format
#     :rtype: Response object
#     """
#     resp = client.get_item(
#         TableName=dynamoTableName,
#         Key={
#             'artist': {'S': artist }
#         }
#     )
#     item = resp.get('Item')
#     if not item:
#     	return jsonify({'error': 'Artist does not exist'}), 404
#
#     return jsonify({
#         'artist': item.get('artist').get('S'),
#         'song': item.get('song').get('S')
#     })

if __name__ == '__main__':
    create_table(dynamoTableName)
    app.run(threaded=True,host='0.0.0.0',port=5000)

