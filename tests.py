import json
import os
import unittest
import shutil

import app
import errors

TEST_FILES_DIR = 'test_files/'

class EmotechTaskTests(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        os.makedirs(TEST_FILES_DIR)
    
    def tearDown(self):
        shutil.rmtree(TEST_FILES_DIR)


    def test_get_existing_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        with open(filename, 'w') as f:
            f.write(contents)

        r = self.app.get('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": False,
            "path": filename,
            "contents": contents,
        })
    
    def test_get_nonexisting_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        r = self.app.get('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.FILE_NOT_EXIST,
        })
    
    def test_get_nonexisting_dir(self):
        filename = TEST_FILES_DIR + 'new_dir/test'
        contents = 'hello'

        r = self.app.get('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.FILE_NOT_EXIST,
        })


    def test_post_nonexisting_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        r = self.app.post('/files/' + filename, data=dict(
            contents=contents
        ))
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": False,
            "path": filename,
            "contents": contents,
        })

        with open(filename, 'r') as f:
            self.assertEqual(contents, f.read())

    def test_post_existing_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        with open(filename, 'w') as f:
            f.write(contents)

        r = self.app.post('/files/' + filename, data=dict(
            contents=contents
        ))
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.FILE_EXISTS,
        })

    def test_post_nonexisting_dir(self):
        filename = TEST_FILES_DIR + 'new_dir/test'
        contents = 'hello'

        r = self.app.post('/files/' + filename, data=dict(
            contents=contents
        ))
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": False,
            "path": filename,
            "contents": contents,
        })
    
    def test_post_without_contents_data(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        r = self.app.post('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.CONTENTS_MUST_BE_STRING,
        })


    def test_put_existing_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'
        new_contents = 'goodbye'

        with open(filename, 'w') as f:
            f.write(contents)

        r = self.app.put('/files/' + filename, data=dict(
            contents=new_contents
        ))
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": False,
            "path": filename,
            "contents": new_contents,
        })

        with open(filename, 'r') as f:
            self.assertEqual(new_contents, f.read())

    def test_put_nonexisting_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'
        new_contents = 'goodbye'

        r = self.app.put('/files/' + filename, data=dict(
            contents=new_contents
        ))
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.FILE_NOT_EXIST,
        })

    def test_put_nonexisting_dir(self):
        filename = TEST_FILES_DIR + 'new_dir/test'
        contents = 'hello'
        new_contents = 'goodbye'

        r = self.app.put('/files/' + filename, data=dict(
            contents=new_contents
        ))
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.FILE_NOT_EXIST,
        })
    
    def test_put_without_contents_data(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        r = self.app.post('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.CONTENTS_MUST_BE_STRING,
        })


    def test_delete_existing_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        with open(filename, 'w') as f:
            f.write(contents)

        r = self.app.delete('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": False,
            "path": filename,
            "contents": '',
        })

        self.assertTrue(not os.path.isfile(filename))

    def test_delete_nonexisting_file(self):
        filename = TEST_FILES_DIR + 'test'
        contents = 'hello'

        r = self.app.delete('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.FILE_NOT_EXIST,
        })

    def test_delete_nonexisting_dir(self):
        filename = TEST_FILES_DIR + 'new_dir/test'
        contents = 'hello'

        r = self.app.delete('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.FILE_NOT_EXIST,
        })



if __name__ == '__main__':
    unittest.main()