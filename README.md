RESTful File Manager
====================

## Running Server

Install the dependencies

    pip install -r requirements.txt

Export Flask variables

    export FLASK_APP=app.py
    export FLASK_DEBUG=1

Run the app

    flask run

## API

### File Management

Get file contents

    GET /files/<path>

Create a new file

    POST /files/<path>, { contents = <contents> }

Update existing file

    PUT /files/<path>, { contents = <contents> }

Delete a file

    DELETE /files/<path>

### Directory Statistics

(Subdirectories are included in the statistics below)

Get number of files in directory

    GET /stats/num_files/<path>

Get mean and standard deviation of alpha numeric characters in files in given directory

    GET /stats/avg_num_chars/<path>

Get mean and standard deviation of word lengths in files in given directory

    GET /stats/avg_word_length/<path>

Get total number of bytes in a directory

    GET /stats/total_bytes/<path>

## Tests

Tests can be found in tests.py. Run them with:

    python tests.py