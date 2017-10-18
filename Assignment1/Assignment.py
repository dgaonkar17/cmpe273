#!/usr/bin/env python
from flask import Flask, request
import rocksdb
import uuid
import sys
import StringIO
import contextlib

app = Flask(_name_)
	
@app.route('/api/v1/scripts', methods = ['POST'])
def upload_file():
	f = request.files['data']
	db = rocksdb.DB("mydb.db", rocksdb.Options(create_if_missing=True))
	key = uuid.uuid4().hex
	db.put(key.encode('utf-8'),f.stream.read().encode('utf-8'))
	return 'script:-d:'+key, 201

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.route('/api/v1/scripts/<scriptid>', methods = ['GET'])
def retrieve_file(scriptid=None):

	db = rocksdb.DB("mydb.db", rocksdb.Options(create_if_missing=True))
	value = db.get(scriptid.encode('utf-8'))

	with stdoutIO() as s:
		exec(value)

	return s.getvalue()



if _name_ == '__main__':
   app.run(debug = True, port=8000)
