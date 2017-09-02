import json
import os
import unittest
import shutil

import app
import errors

TEST_FILES_DIR = 'test_files/'


class FileManagingTests(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        os.makedirs(TEST_FILES_DIR)
    
    def tearDown(self):
        shutil.rmtree(TEST_FILES_DIR)


class GetFileTests(FileManagingTests):

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

    def test_get_directory(self):
        filename = TEST_FILES_DIR + 'new_dir'

        os.makedirs(filename)

        r = self.app.get('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.IS_A_DIRECTORY,
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


class PostFileTests(FileManagingTests):

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

    def test_post_directory(self):
        filename = TEST_FILES_DIR + 'new_dir'

        os.makedirs(filename)

        r = self.app.post('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.IS_A_DIRECTORY,
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


class PutFileTests(FileManagingTests):

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

    def test_put_directory(self):
        filename = TEST_FILES_DIR + 'new_dir'

        os.makedirs(filename)

        r = self.app.put('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.IS_A_DIRECTORY,
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

class DeleteFileTests(FileManagingTests):

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

    def test_delete_directory(self):
        filename = TEST_FILES_DIR + 'new_dir'

        os.makedirs(filename)

        r = self.app.delete('/files/' + filename)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "error": True,
            "path": filename,
            "contents": errors.IS_A_DIRECTORY,
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



def make_file_tree(tree, root='.'):
    for key, value in tree.items():
        if type(value) is str:
            with open(root + '/' + key, 'w') as f:
                f.write(value)
        if type(value) is dict:
            new_root = root + '/' + key
            os.makedirs(new_root)
            make_file_tree(value, root=new_root)


STATS_TEST_FILES_DIR = TEST_FILES_DIR.rstrip('/')

def make_test_files(tree):
    return make_file_tree({
        STATS_TEST_FILES_DIR: tree
    })


class StatsTests(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
    
    def tearDown(self):
        shutil.rmtree(STATS_TEST_FILES_DIR)

    def test_num_files(self):
        dir_name = STATS_TEST_FILES_DIR
        make_test_files({
            'file1': '12abC',
            'file2': '12abC',
            'dir': {
                'file3': '12ab',
                'file4': '12abCD',
            },
        })

        r = self.app.get('/stats/num_files/' + dir_name)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            "num_files": 4,
        })
    
    def test_avg_num_chars(self):
        dir_name = STATS_TEST_FILES_DIR
        make_test_files({
            'file1': '12abC',
            'file2': '12abC',
            'dir': {
                'file3': '12ab',
                'file4': '12abCD',
            },
        })

        r = self.app.get('/stats/avg_num_chars/' + dir_name)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            'avg_num_chars': {
                'mean': 5.0,
                'sd': 0.816496580927726,
            },
        })
    
    def test_avg_word_length(self):
        dir_name = STATS_TEST_FILES_DIR
        make_test_files({
            'file1': '12abC 12abCD',
            'file2': '12abC',
            'dir': {
                'file3': '12ab',
                'file4': '12abCD',
            },
        })

        r = self.app.get('/stats/avg_word_length/' + dir_name)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            'avg_word_length': {
                'mean': 5.2,
                'sd': 0.8366600265340756,
            },
        })
    
    def test_total_bytes(self):
        dir_name = STATS_TEST_FILES_DIR
        make_test_files({
            'file1': '12abC',
            'file2': '12abC',
            'dir': {
                'file3': '12ab',
                'file4': '12abCD',
            },
        })

        r = self.app.get('/stats/total_bytes/' + dir_name)
        data = json.loads(r.get_data().decode())
        self.assertEqual(data, {
            'total_bytes': 20,
        })



if __name__ == '__main__':
    unittest.main()
