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

For help, run:

    readwise-apple-notes --help

You can also use:

    python -m readwise-apple-notes --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment using `poetry`:

    cd readwise-apple-notes
    poetry install

Now install the dependencies and test dependencies:

    poetry install --with=dev

To run the tests:

    pytest
