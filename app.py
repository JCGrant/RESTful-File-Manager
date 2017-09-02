"""
Write a rest webservice in python that allows to operate over text files as resources. The minimum requirements for the service is:
Create a text file with some contents stored in a given path.
Retrieve the contents of a text file under the given path.
Replace the contents of a text file.
Delete the resource that is stored under a given path.
 
We would also need to get some statistics per folder basis and retrieve them through another entry point. These statistics are:
Total number of files in that folder.
Average number of alphanumeric characters per text file (and standard deviation) in that folder.
Average word length (and standard deviation) in that folder. 
Total number of bytes stored in that folder.
Note: All these computations must be calculated recursively from the provided path to the entry point.
"""
from flask import Flask, jsonify
from flask_restful import reqparse, Resource, Api

import errors
import file_utils


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('contents')


class TextFile(Resource):
    def get(self, path):
        contents, error = file_utils.get_file(path)
        return {
            'path': path,
            'contents': contents,
            'error': error,
        }
    
    def post(self, path):
        contents = parser.parse_args()['contents']
        try:
            contents, error = file_utils.create_file(path, contents)
        except TypeError:
            contents, error = errors.CONTENTS_MUST_BE_STRING, True
        return {
            'path': path,
            'contents': contents,
            'error': error,
        }
    
    def put(self, path):
        contents = parser.parse_args()['contents']
        try:
            contents, error = file_utils.update_file(path, contents)
        except TypeError:
            contents, error = errors.CONTENTS_MUST_BE_STRING, True
        return {
            'path': path,
            'contents': contents,
            'error': error,
        }
    
    def delete(self, path):
        contents, error = file_utils.delete_file(path)
        return {
            'path': path,
            'contents': contents,
            'error': error,
        }


api.add_resource(TextFile, '/files/<path:path>')

@app.route('/stats/num_files/<path:path>')
def num_files(path):
    return jsonify({
        'num_files': file_utils.num_files(path),
    })

@app.route('/stats/avg_num_chars/<path:path>')
def avg_num_chars(path):
    return jsonify({
        'avg_num_chars': file_utils.avg_num_chars(path),
    })

@app.route('/stats/total_bytes/<path:path>')
def total_bytes(path):
    return jsonify({
        'total_bytes': file_utils.total_bytes(path),
    })
