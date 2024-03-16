# readwise-apple-notes

[![PyPI](https://img.shields.io/pypi/v/readwise-apple-notes.svg)](https://pypi.org/project/readwise-apple-notes/)
[![Changelog](https://img.shields.io/github/v/release/Scarvy/readwise-apple-notes?include_prereleases&label=changelog)](https://github.com/Scarvy/readwise-apple-notes/releases)
[![Tests](https://github.com/Scarvy/readwise-apple-notes/actions/workflows/test.yml/badge.svg)](https://github.com/Scarvy/readwise-apple-notes/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Scarvy/readwise-apple-notes/blob/master/LICENSE)

Export Readwise highlights to Apple Notes.

## Installation

Install this tool using `pip`:

    pip install readwise-apple-notes

## Usage

> [!NOTE]
> First, obtain a Readwise access token. Then, the token has to be stored, either into an .env file or an environment variable using export READWISE_TOKEN=<your_token>.

For help, run:

    readwise-apple-notes --help

You can also use:

    python -m readwise-apple-notes --help

### Export

Export all highlights:

    readwise-apple-notes export

Export after a specific date:

    readwise-apple-notes export --updated-after 2024-03-15

Export a single books highlights:

    readwise-apple-notes export --book-id=<user_book_id>

Or a list of books:

    readwise-apple-notes export --book-id=<user_book_id>,<another_book_id>

### Additional Commands

When you need to look a `book_id`, run:

    readwise-apple-notes books
    
    {
        "id": 29932193,
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "category": "books",
        "num_highlights": 2,
        "source": "kindle",
        "document_note": "",
        "document_tag": ""
    }
    ...
    {
        "id": 29931089,
        "title": "How to Use Readwise",
        "author": "Readwise Team",
        "category": "books",
        "num_highlights": 62,
        "source": "native",
        "document_note": "",
        "document_tag": "readwise"
    }

If you know the `book_id` and want to check a book's details, run:

    readwise-apple-notes book <book_id>

    {
        "id": 29932193,
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "category": "books",
        "source": "kindle",
        "num_highlights": 2,
        "last_highlight_at": "2016-08-03T04:56:00.000000Z",
        "updated": "2023-07-10T00:56:27.463529Z",
        "cover_image_url": "https://images-na.ssl-images-amazon.com/images/I/41shZGS-G%2BL._SL200_.jpg",
        "highlights_url": "https://readwise.io/bookreview/29932193",
        "source_url": null,
        "asin": "B00555X8OA",
        "tags": [],
        "document_note": ""
    }

### Reference

    Usage: readwise-apple-notes [OPTIONS] COMMAND [ARGS]...

    Export Readwise Highlights to Apple Notes.

    Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

    Commands:
    book
    books
    export

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment using `poetry`:

    cd readwise-apple-notes
    poetry install

Now install the dependencies and test dependencies:

    poetry install --with=dev

To run the tests:

    pytest
